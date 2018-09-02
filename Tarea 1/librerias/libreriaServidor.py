import pygame, sys, random, zmq
from librerias.tableroLibreria import *


class Servidor:
    def __init__(self, cantidad):
        contexto = zmq.Context()
        self.socket = contexto.socket(zmq.ROUTER)
        self.clientesRegistrados = {}
        self.cantidadMaximaJugadores = cantidad
        self.posicionesIniciales = [(7,10),(11,3), (19,5)]
    
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

    def jugadoresRegistrados(self):
        return len(self.clientesRegistrados)

    def hayCupo(self):
        if(self.jugadoresRegistrados() == self.cantidadMaximaJugadores):
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
            print("Usuario esta en usuarios")
            return False
        else:
            print("Usuario no esta en usuarios")
            return True

    def getCantidadMaximaJugadores(self):
        return self.cantidadMaximaJugadores
    
    def imprimirRegistrado(self):
        print(self.clientesRegistrados)

    def posicionCliente(self, identidad):
        return str(self.clientesRegistrados[identidad])

    def broadCast(self, mensaje):
        for usuario in self.clientesRegistrados:
            self.enviarMensajeA(usuario, mensaje)

    def listaJugadores(self):
        mensaje = ""
        for i in self.clientesRegistrados.keys():
            aux = str(i) + ":" + str(self.clientesRegistrados[i])
            mensaje = mensaje + aux + ","
        return(mensaje)
