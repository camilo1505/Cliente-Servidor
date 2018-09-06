import pygame, sys, random, zmq, json, time
from librerias.tableroLibreria import *


class Servidor:
    def __init__(self, cantidad):
        contexto = zmq.Context()
        self.socket = contexto.socket(zmq.ROUTER)
        self.clientesRegistrados = {}
        self.cantidadMaximaJugadores = cantidad
        self.jugadoresListos = 0
        self.posicionesIniciales = [[8,5],[3,11],[16,10],[10,1]]

    def iniciarServidor(self):
        self.socket.bind("tcp://*:5555")

    def decodificarMensaje(self, mensaje):
        mensajeDecodificado = []
        for i in range(len(mensaje)):
            mensajeDecodificado.append(mensaje[i].decode('ascii'))
        return mensajeDecodificado

    def recibirMensajeCliente(self):
        canal = self.socket
        mensaje = self.decodificarMensaje(canal.recv_multipart())
        return mensaje


    def hayCupo(self):
        if(self.jugadoresListos == self.cantidadMaximaJugadores):
            return False
        else:
            return True

    def enviarMensajeA(self, destinatario, mensaje):
        self.socket.send_multipart([bytes(destinatario, 'ascii'), bytes(mensaje, 'ascii')])

    def registrarNuevoJugador(self, identidad):
        posicion = random.choice(self.posicionesIniciales)
        self.posicionesIniciales.remove(posicion)
        nuevoJugador = {identidad:posicion}
        self.clientesRegistrados.update(nuevoJugador)

    def usuarioValido(self, identidad):
        usuarios = self.clientesRegistrados.keys()
        if(identidad in usuarios):
            return False
        else:
            return True

    def getCantidadMaximaJugadores(self):
        return self.cantidadMaximaJugadores

    def imprimirRegistrado(self):
        print(self.clientesRegistrados)

    def posicionCliente(self, identidad):
        return str(self.clientesRegistrados[identidad])

    def descomponerJson(self, mensaje):
        return json.dumps(mensaje)

    def broadcast(self, identidad):
        for usuario in self.clientesRegistrados.keys():
            enviarMensajeA(usuario, identidad)

    def enviarPosiciones(self):
        posiciones = self.clientesRegistrados
        print("clientes Registrados {}".format(posiciones))
        mensajeJson = self.descomponerJson(posiciones)
        print("mensaje {}".format(mensajeJson))
        for usuario in self.clientesRegistrados.keys():
            print("mensaje bytes {}".format(bytes(mensajeJson, 'ascii')))
            self.socket.send_multipart([bytes(usuario,'ascii'), bytes(mensajeJson, 'ascii')])
    def eliminarJugador(self, identidad):
        self.clientesRegistrados.pop(identidad)
        mensaje = "perdiste"
        self.enviarMensajeA(identidad, mensaje)

    def jugadorListo(self):
        self.jugadoresListos += 1

    def getJugadoresListos(self):
        return self.jugadoresListos

    def cambiarPosicion(self, identidad, posicion):
        self.clientesRegistrados.pop(identidad)
        nuevaPosicion = json.loads(posicion)
        nuevaPosicion = {identidad:nuevaPosicion}
        self.clientesRegistrados.update(nuevaPosicion)
