import zmq
import sys
import hashlib
import json

partSize = 1024 * 1024 * 10

def computeHashFile(filename):
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def computeHash(bytes):
    sha1 = hashlib.sha1()
    sha1.update(bytes)
    return sha1.hexdigest()

def uploadFile(context, filename, servers, proxy, username):
    sockets = []
    for ad in servers:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ ad.decode("ascii"))
        sockets.append(s)

    with open(filename, "rb") as f:
        completeSha1= bytes(computeHashFile(filename), "ascii")
        finished = False
        part = 0
        sha1File = open("temp/temporal.txt", "ab")

        #Escribir en la primer linea del archivo el sha1 de todo el archivo
        sha1File.write(completeSha1 + b'\n')

        while not finished:
            print("Uploading part {}".format(part))
            f.seek(part*partSize)
            bt = f.read(partSize)

            #Creando Sha1 de cada parte
            sha1bt = bytes(computeHash(bt), "ascii")
            #Escribe los Sha1 de cada parte del archivo en un archivo txt
            sha1File.write(sha1bt + b'\n')

            s = sockets[part % len(sockets)]
            s.send_multipart([b"upload", bt, sha1bt])
            response = s.recv()
            print("Received reply for part {} ".format(part))
            part = part + 1
            if len(bt) < partSize:
                finished = True
        sha1File.close()
        reportarProxyUpload(filename, username, servers, proxy)

def reportarProxyUpload(nombreArchivo, nombreUsuario, servidores, proxy):
    archivoSha1 = open("temp/temporal.txt", 'r')
    stringSha1 = archivoSha1.read()
    listaSha1 = stringSha1.split("\n")

    listaSha1Json = json.dumps(listaSha1)
    listaTemporal = []
    for servidor in servidores:
        listaTemporal.append(servidor.decode('ascii'))
    servidoresJson = json.dumps(listaTemporal)
    
    proxy.send_multipart([b'uploadShas', nombreUsuario, nombreArchivo, bytes(listaSha1Json,'ascii'), bytes(servidoresJson, 'ascii')])
    respuesta = proxy.recv()
    print(respuesta.decode('ascii'))

def download(context, nombreArchivo, proxy, nombreUsuario):
    proxy.send_multipart([b"download", nombreUsuario, nombreArchivo])
    sha1PartesBytes, listaServidoresBytes = proxy.recv_multipart()
    
    sha1Partes = json.loads(sha1PartesBytes.decode('ascii'))

    sha1Partes.pop()

    listaServidores = json.loads(listaServidoresBytes.decode('ascii'))


    print("Sha1Partes: {}".format(sha1Partes))
    print("listaServidores: {}".format(listaServidores))

    sockets = []
    for servidor in listaServidores:
        print("Servidor: {}".format(servidor))
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ str(servidor))
        sockets.append(s)

    with open(nombreArchivo.decode("ascii"), 'ab') as archivo:
        part = 0
        for sha1 in sha1Partes:
            s = sockets[part % len(sockets)]
            s.send_multipart([b"download", bytes(sha1, 'ascii')])
            parteArchivo = s.recv()
            archivo.write(parteArchivo)
            part += 1
        print("Succesfull download <{}>".format(nombreArchivo.decode('ascii')))
        response = s.recv()


    


def main():
    if len(sys.argv) != 4:
        print("Must be called with a filename")
        print("Sample call: python ftclient <username> <operation> <filename>")
        exit()


    username = sys.argv[1].encode('ascii')
    operation = sys.argv[2]
    filename = sys.argv[3].encode('ascii')

    context = zmq.Context()
    proxy = context.socket(zmq.REQ)
    proxy.connect("tcp://localhost:6666")
    proxy.identity = username

    print("Operation: {}".format(operation))
    if operation == "upload":
        proxy.send_multipart([b"availableServers", username])
        servers = proxy.recv_multipart()
        print("There are {} available servers".format(len(servers)))
        uploadFile(context, filename, servers, proxy, username)
        print("File {} was uploaded.".format(filename))
    elif operation == "download":
        download(context, filename, proxy, username)

    elif operation == "share":
        print("Not implemented yet")
    else:
        print("Operation not found!!!")

if __name__ == '__main__':
    main()
