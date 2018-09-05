import pygame, sys, random, zmq, json
from pygame.locals import *

class Conexion:
    def __init__(self, identidad):
        contexto = zmq.Context()
        self.socket = contexto.socket(zmq.DEALER)
        self.identidad = identidad
        self.poller = zmq.Poller()
     
    def iniciarConexion(self, direccion):
        conexion = "tcp://" + direccion + ":5555"
        self.socket.identity = self.identidad.encode('ascii')
        self.socket.connect(conexion)
        print("Conexion Iniciada con la Identidad <" + self.identidad + ">")

    def iniciarPoller(self):
        self.poller.register(sys.stdin, zmq.POLLIN)
        self.poller.register(self.socket, zmq.POLLIN)
        print("Poller Iniciado Correctamente")
    
    def enviarSolicitud(self, solicitud):
        operacion, contenido = solicitud
        canal = self.socket
        canal.send_multipart([bytes(operacion,'ascii'), bytes(contenido,'ascii')])
        print("Enviado el mensaje <" + self.identidad +">" + " <" + operacion + ">" + " <" + contenido + ">")
    
    def mensajesPendientes(self):
        pendientes = dict(self.poller.poll())
        if(self.socket in pendientes):
            return True
        if(sys.stdin.fileno() in pendientes):
            return False

    def obtenerEstructura(self):
        estructura = self.socket.recv_multipart()
        mensaje = estructura[0].decode('ascii')
        mensajeJson = json.loads(mensaje)
        return mensajeJson
    
    def obtenerMensaje(self):
        mensaje = self.socket.recv_multipart()
        respuesta = mensaje[0]
        return (respuesta.decode('ascii'))

class Tablero:
    def __init__(self, ancho=18, alto=21):
        self.tablero = alto*[ancho*["#"]]
        self.anchura = ancho
        self.altura = alto

    def cargarTablero(self):
        archivo = open("laberintos/laberinto.c",'r')
        contenidoLaberinto = archivo.read()
        vectorLaberinto = contenidoLaberinto.split('\n')
        matrizLaberinto = []
        for i in range(len(vectorLaberinto)):
            vectorActual = vectorLaberinto[i].split(',')
            matrizLaberinto.append(vectorActual)
        self.tablero = matrizLaberinto

    def hayObstaculo(self, posicionActual, jugadores):
        hayPacman = False
        hayPared = False
        for i in jugadores:
            if(i.getPosicionLogica() == posicionActual):
                hayPacman = True
                if(i.getRol() == 1):
                    indice = jugadores.index(i)
                    jugadores.pop(indice)
        hayPared = self.hayPared(posicionActual)
        if(hayPared or hayPacman):
            return True
        else:
            return False

    def hayPared(self, posicionActual):
        x = posicionActual[0]
        y = posicionActual[1]
        actual = self.tablero[y][x]
        if(actual == '#'):
            return True
        if(actual == ""):
            return False
    
    def hayGalletaGrande(self, posicionActual):
        x = posicionActual[0]
        y = posicionActual[1]
        actual = self.tablero[y][x]
        if(actual == 'O'):
            return True
        else:
            return False

    def hayGalletaPequena(self, posicionActual):
        x = posicionActual[0]
        y = posicionActual[1]
        actual = self.tablero[y][x]
        if(actual == '0'):
            return True
        else:
            return False
    
    def contenidoMapa(self, posicion):
        x = posicion[0]
        y = posicion[1]
        return self.tablero[y][x]

    def cambioCasilla(self,posicion):
        x = posicion[0]
        y = posicion[1]
        self.tablero[y][x] = ""

    def imprimirTablero(self):
        print(self.tablero)

    def getTablero(self):
        return self.tablero
    def getAnchura(self):
        return len(self.tablero[0])
    def getAltura(self):
        return len(self.tablero)


class Pared:
    def __init__(self, imagenPared, anchoImagen = 30, largoImagen = 23):
        pygame.init()
        self.imagen = pygame.image.load(imagenPared)
        self.ancho = anchoImagen
        self.largo = largoImagen

    def getAncho(self):
        return self.ancho
    def getAlto(self):
        return self.largo
    
    def getImagen(self):
        return self.imagen
    
    def posicionImprimir(self, posicionAnterior):
        return (posicionAnterior[0] * self.ancho, posicionAnterior[1] * self.largo)

class Jugador:
    def __init__(self, identificacion, posicionInicial, anchoImagen=30, largoImagen=23):
        pygame.init()
        self.imagenDerecha = [pygame.image.load("sprites/pacman/R.png"), pygame.image.load("sprites/ghost/R.png")]
        self.imagenArriba = [pygame.image.load("sprites/pacman/U.png"), pygame.image.load("sprites/ghost/R.png")]
        self.imagenIzquierda = [pygame.image.load("sprites/pacman/L.png"), pygame.image.load("sprites/ghost/L.png")]
        self.imagenAbajo = [pygame.image.load("sprites/pacman/D.png"), pygame.image.load("sprites/ghost/L.png")]
        self.ancho=anchoImagen
        self.largo=largoImagen
        self.identidad = identificacion
        self.posicionLogica = posicionInicial
        self.ultimoMovimiento = "L"
        self.rol = 0
        self.puntaje = 0
    
    def posicionImprimirJugador(self):
        x = self.posicionLogica[0]
        y = self.posicionLogica[1]
        return (x * self.ancho, y  * self.largo)


    def movimiento(self,tipoMovimiento, casillaFutura):
        if(casillaFutura != True):
            if(tipoMovimiento == "U"):
                self.posicionLogica = (self.posicionLogica[0], self.posicionLogica[1]-1)
                self.ultimoMovimiento = "U"
            if(tipoMovimiento == "R"):
                self.posicionLogica = (self.posicionLogica[0]+1, self.posicionLogica[1])
                self.ultimoMovimiento = "R"
            if(tipoMovimiento == "D"):
                self.posicionLogica = (self.posicionLogica[0], self.posicionLogica[1]+1)
                self.ultimoMovimiento = "D"
            if(tipoMovimiento == "L"):
                self.posicionLogica = (self.posicionLogica[0]-1, self.posicionLogica[1])
                self.ultimoMovimiento = "L"
    
    def imagenJugador(self):
        if(self.ultimoMovimiento == "U"):
            return self.imagenArriba[self.rol]
        if(self.ultimoMovimiento == "R"):
            return self.imagenDerecha[self.rol]
        if(self.ultimoMovimiento == "D"):
            return self.imagenAbajo[self.rol]
        if(self.ultimoMovimiento == "L"):
            return self.imagenIzquierda[self.rol]


    def getPosicionLogica(self):
        return self.posicionLogica
    def getRol(self):
        return self.rol

    def setRol(self, cambioRol):
        self.rol = cambioRol

    def cazarPacmans(self, jugadores):
        for i in range(1, len(jugadores)):
            jugador = jugadores[i]
            jugador.setRol(1)

    def setPuntaje(self, casilla, jugadores):
        if(casilla == 'O' and self.rol == 0):
            self.puntaje += 2
            self.cazarPacmans(jugadores)
        if(casilla == '0' and self.rol == 0):
            self.puntaje += 1


    def getPuntaje(self):
        return self.puntaje

    def getIdentidad(self):
        return self.identidad

    def setPosicion(self, posicion):
        self.posicionLogica = posicion

class Galleta:
    
    def __init__(self, galleta,  anchoImagen=30, largoImagen=23):
        self.imagenGalleta = [pygame.image.load("sprites/cookie/cb.png"), pygame.image.load("sprites/cookie/cs.png")]
        self.tipoGalleta = galleta
        self.ancho = anchoImagen
        self.largo = largoImagen

    def posicionImprimirGalleta(self, posicion):
        x = posicion[0]
        y = posicion[1]
        return (self.ancho * x, self.largo * y)
    
    def getImagenImprimir(self):
        return self.imagenGalleta[self.tipoGalleta]
