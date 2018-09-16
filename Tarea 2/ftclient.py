import zmq
import sys
import hashlib
import json
import os
import time

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
        partAux = 1
        sha1File = open("temp/temporal.txt", "wb")

        totalFileSize = os.path.getsize(filename)

        #Escribir en la primer linea del archivo el sha1 de todo el archivo
        sha1File.write(completeSha1 + b'\n')

        while not finished:
            f.seek(part*partSize)
            bt = f.read(partSize)

            #Creando Sha1 de cada parte
            sha1bt = bytes(computeHash(bt), "ascii")
            #Escribe los Sha1 de cada parte del archivo en un archivo txt
            sha1File.write(sha1bt + b'\n')

            s = sockets[part % len(sockets)]
            s.send_multipart([b"upload", bt, sha1bt])
            response = s.recv()

            currentPart = partAux * partSize
            hashtag = (60 * currentPart) // totalFileSize
            void = 60 - hashtag
            percent = (100 * hashtag) // 60
            print("Uploading: [{}{}] {}%".format('#' * hashtag, ' ' * void, percent - 1), end='\r')
            time.sleep(0.05)
            
            partAux += 1
            part = part + 1
            if len(bt) < partSize:
                finished = True
        sha1File.close()
        print('\n')
        print("Succesfull Upload <{}>".format(filename.decode('ascii')))
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
    print("Report: {}".format(respuesta.decode('ascii')))

def download(context, nombreArchivo, proxy, nombreUsuario):
    proxy.send_multipart([b"download", nombreUsuario, nombreArchivo])
    sha1PartesBytes, listaServidoresBytes = proxy.recv_multipart()
    
    sha1Partes = json.loads(sha1PartesBytes.decode('ascii'))

    sha1Partes.pop()

    listaServidores = json.loads(listaServidoresBytes.decode('ascii'))

    sockets = []
    for servidor in listaServidores:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ str(servidor))
        sockets.append(s)

    with open(nombreArchivo.decode("ascii"), 'ab') as archivo:
        part = 0
        partAux = 1
        totalPartsFile = len(sha1Partes)
        for sha1 in sha1Partes:
            s = sockets[part % len(sockets)]
            s.send_multipart([b"download", bytes(sha1, 'ascii')])
            parteArchivo = s.recv()
            archivo.write(parteArchivo)

            hashtag = (60 * partAux ) // totalPartsFile
            void = 60 - hashtag
            percent = (100 * hashtag) // 60 
            print("Downloading: [{}{}] {}%".format('#' * hashtag, ' ' * void, percent), end='\r')
            time.sleep(0.05)
            partAux += 1
            part += 1
        print('\n')
        print("Succesfull Download <{}>".format(nombreArchivo.decode('ascii')))

def share(context, sha1Archivo, proxy, nombreUsuario):
    proxy.send_multipart([b'share', nombreUsuario, sha1Archivo])

    sha1PartesBytes, listaServidoresBytes, nombreArchivoBytes = proxy.recv_multipart()

    sha1Partes = json.loads(sha1PartesBytes.decode('ascii'))
    nombreArchivo = nombreArchivoBytes.decode('ascii')

    sha1Partes.pop()

    listaServidores = json.loads(listaServidoresBytes.decode('ascii'))

    sockets = []
    for servidor in listaServidores:
        s = context.socket(zmq.REQ)
        s.connect("tcp://"+ str(servidor))
        sockets.append(s)

    with open(nombreArchivo, 'ab') as archivo:
        part = 0
        partAux = 1
        totalPartsFile = len(sha1Partes)
        for sha1 in sha1Partes:
            s = sockets[part % len(sockets)]
            s.send_multipart([b"download", bytes(sha1, 'ascii')])
            parteArchivo = s.recv()
            archivo.write(parteArchivo)

            hashtag = (60 * partAux) // totalPartsFile
            void = 60 - hashtag
            percent = (100 * hashtag) // 60 
            print("Downloading: [{}{}] {}%".format('#' * hashtag, ' ' * void, percent))
            time.sleep(0.05)
            partAux +=1
            part += 1
        print("Succesfull Share <{}>".format(nombreArchivo))    
    
def listar(context, proxy, nombreUsuario):
    proxy.send_multipart([b"list", nombreUsuario])

    archivos = proxy.recv_json()

    print(archivos)

def main():
    menu = ''
    username = input("Username: <").encode('ascii')
    while(menu != b'exit'):
        fileMenu = open("menu.dot", 'r')
        menu = fileMenu.read()
        print(menu)
        operation = input('Operation: <')
        if(operation != "list" and operation != "exit"):
            filename = input('File Name: <').encode('ascii')
        if(operation == "exit"):
            exit()

        context = zmq.Context()
        proxy = context.socket(zmq.REQ)
        proxy.connect("tcp://localhost:6666")
        proxy.identity = username

        if(not os.path.exists("temp/")):
            os.mkdir("temp")

        print("Operation: {}".format(operation))
        if operation == "upload":
            proxy.send_multipart([b"availableServers", username])
            servers = proxy.recv_multipart()
            uploadFile(context, filename, servers, proxy, username)
            os.remove("temp/temporal.txt")

        elif operation == "download":
            download(context, filename, proxy, username)

        elif operation == "share":
            share(context, filename, proxy, username)

        elif operation == "list":
            listar(context, proxy, username)
        else:
            print("Operation not found!!!")

if __name__ == '__main__':
    main()
