import zmq
import json
from library.clases import *

def buscarUsuario(usuarios, nombreUsuario):
    for usuario in usuarios:
        if(usuario.getNombreUsuario() == nombreUsuario):
            return usuario
    print("Usuario no encontrado, saliendo del programa")
    exit()


def enviarArchivo(clients, usuario, nombreArchivo):
    sha1Partes = json.dumps(usuario.getShas(nombreArchivo))
    aux = usuario.getListaServidores(nombreArchivo)
    print(type(aux))
    listaServidores = json.dumps(aux)
    print("Sha1: {}".format(sha1Partes))
    print("servidores: {}".format(listaServidores))

    clients.send_multipart([bytes(sha1Partes,'ascii'),bytes(listaServidores,'ascii')])

def enviarArchivoSha(clients, archivo, nombreArchivo):
    sha1Partes = json.dumps(archivo.getShaPartes())
    listaServidores = json.dumps(archivo.getListaServidores())
    print("Sha1: {}".format(sha1Partes))
    print("servidores: {}".format(listaServidores))

    clients.send_multipart([bytes(sha1Partes,'ascii'),bytes(listaServidores,'ascii'),bytes(nombreArchivo, 'ascii')])

def buscarSha(sha1, usuarios):
    for usuario in usuarios:
        archivosUsuario = usuario.getArchivos()
        for archivo in archivosUsuario:
            if(archivo.getSha() == sha1):
                return archivo

def listar(usuarios, usuario):
    for i in usuarios:
        print("Usuario: {}".format(usuario))
        if(i.getNombreUsuario() == usuario):
            print("usuario: {}".format(i.getNombreUsuario()))
            print("Archivos: {}".format(i.getNombresArchivos()))
            return i.getNombresArchivos()

def main():
    # Address for each server to receive files
    servAddresses = []

    context = zmq.Context()
    servers = context.socket(zmq.REP)
    servers.bind("tcp://*:5555")

    clients = context.socket(zmq.REP)
    clients.bind("tcp://*:6666")

    poller = zmq.Poller()
    poller.register(servers, zmq.POLLIN)
    poller.register(clients, zmq.POLLIN)

    usuarios = []

    while True:
        socks = dict(poller.poll())
        if clients in socks:
            print("Message from client")
            operation, nombreUsuarioBytes, *msg = clients.recv_multipart()
            usuario = Usuario(nombreUsuarioBytes.decode('ascii'))
            usuarios.append(usuario)
            if operation == b"availableServers":
                clients.send_multipart(servAddresses)

            if(operation == b"uploadShas"):
                nombreArchivoBytes, shasBytes, servidoresBytes = msg

                nombreUsuario = nombreUsuarioBytes.decode('ascii')
                nombreArchivo = nombreArchivoBytes.decode('ascii')
                listaShas = json.loads(shasBytes.decode('ascii'))
                listaServidores = json.loads(servidoresBytes.decode('ascii'))
                
                print(type(listaServidores))
                print("Reporte de Shas del usuario <{}> archivo <{}>".format(nombreUsuario,nombreArchivo))

                shaCompleto = listaShas[0]
                listaShas.pop(0)

                archivo = Archivo(nombreArchivo, shaCompleto, listaShas, listaServidores)

                usuarioBuscado = buscarUsuario(usuarios, nombreUsuario)

                usuarioBuscado.agregarArchivo(archivo)
                
                print("Reporte Terminado")
                clients.send(b"ok")
            
            if(operation == b"download"):
                nombreArchivoBytes = msg[0]
                nombreUsuario = nombreUsuarioBytes.decode('ascii')
                nombreArchivo = nombreArchivoBytes.decode('ascii')

                usuarioBuscado = buscarUsuario(usuarios, nombreUsuario)

                enviarArchivo(clients, usuarioBuscado, nombreArchivo)
            
            if(operation == b"share"):
                shaArchivoBytes = msg[0]
                shaArchivo = shaArchivoBytes.decode('ascii')

                shaBuscado = buscarSha(shaArchivo, usuarios)

                nombreArchivo = shaBuscado.getNombreArchivo()

                enviarArchivoSha(clients, shaBuscado, nombreArchivo)

            if(operation == b"list"):
                aux = nombreUsuarioBytes.decode('ascii')
                listarArchivos = listar(usuarios, aux)
                print(listarArchivos)
                clients.send_json(listarArchivos)                

        if servers in socks:
            print("Message from server")
            operation, *rest = servers.recv_multipart()
            if operation == b"newServer":
                servAddresses.append(rest[0])
                print(servAddresses)
                servers.send(b"Ok")


if __name__ == '__main__':
    main()
