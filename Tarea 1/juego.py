import pygame, sys, random, time
from pygame.locals import *
from librerias.tableroLibreria import *


def imprimirTablero(tablero, pared, ventana):
    posicionActual = (0,0)
    for y in range(tablero.getAltura()):
        for x in range(tablero.getAnchura()):
           posicionActual = (x,y)
           if(tablero.hayPared(posicionActual)):
               ventana.blit(pared.getImagen(), pared.posicionImprimir(posicionActual))
           if(tablero.hayGalletaGrande(posicionActual)):
               galleta = Galleta(0)
               ventana.blit(galleta.getImagenImprimir(), galleta.posicionImprimirGalleta(posicionActual))
           if(tablero.hayGalletaPequena(posicionActual)):
               galleta = Galleta(1)
               ventana.blit(galleta.getImagenImprimir(), galleta.posicionImprimirGalleta(posicionActual))

def imprimirJugador(jugadores, ventana, tablero):
    for jugador in jugadores:
        tablero.cambioCasilla(jugador.getPosicionLogica())
        ventana.blit(jugador.imagenJugador(), jugador.posicionImprimirJugador())

def imprimirPuntaje(jugador, ventana, fuente):
    puntos = jugador.getPuntaje()
    texto = fuente.render("Puntos: " + str(puntos), False,(255,255,255))
    ventana.blit(texto,(540, 10))


def moverJugador(tipo, jugadores, tablero, servidor):
    jugador = jugadores[0]
    x,y = jugador.getPosicionLogica()
    siguienteCasilla = (0,0)
    if(tipo == "U"):
        casillaFutura = tablero.hayObstaculo((x,y-1), jugadores, servidor)
        siguienteCasilla = (x,y-1)
    if(tipo == "R"):
        casillaFutura = tablero.hayObstaculo((x+1,y), jugadores, servidor)
        siguienteCasilla = (x+1,y)
    if(tipo == "D"):
        casillaFutura = tablero.hayObstaculo((x,y+1), jugadores, servidor)
        siguienteCasilla = (x,y+1)
    if(tipo == "L"):
        casillaFutura = tablero.hayObstaculo((x-1,y), jugadores, servidor)
        siguienteCasilla = (x-1,y)
    print(casillaFutura)

    if(tablero.hayGalletaGrande(siguienteCasilla) or tablero.hayGalletaPequena(siguienteCasilla)):
        if(jugador.getRol() == 0):
            jugador.setPuntaje(tablero.contenidoMapa(siguienteCasilla), jugadores)
            tablero.cambioCasilla(siguienteCasilla)

    print(jugador.getPuntaje())

    jugador.movimiento(tipo, casillaFutura, servidor, siguienteCasilla)


def main():
    if len(sys.argv) != 2:
        print("Faltan Argumentos: <identidad>")
        exit()
    identidad = sys.argv[1]

    pared = Pared("sprites/laberinto/ladrillos2.png")
    tablero = Tablero()
    tablero.cargarTablero()
    pygame.init()
    ventana = pygame.display.set_mode(((pared.getAncho()*tablero.getAnchura()) + 150, (pared.getAlto()*tablero.getAltura())))
    pygame.display.set_caption("Pacman")
    negro = (0,0,0)
    pygame.font.init()
    fuente = pygame.font.SysFont('Comic Sans MS', 30)

    servidor = Conexion(identidad)
    servidor.iniciarConexion("localhost")
    servidor.iniciarPoller()

    solicitud = ("solicitudJugar", "")
    servidor.enviarSolicitud(solicitud)
    respuesta = servidor.obtenerMensaje()

    if(respuesta != "errorUsuario" or respuesta != "errorCompleto"):

        solicitud = ("listoJugar", "")
        servidor.enviarSolicitud(solicitud)
        respuesta = servidor.obtenerEstructura()

        jugadores = []
        posicion = respuesta[identidad]
        x = int(posicion[0])
        y = int(posicion[1])
        jugadorLocal = Jugador(identidad, (x,y))
        jugadores.append(jugadorLocal)

        for i in respuesta.keys():
            if(i != identidad):
                posicion = respuesta[i]
                x = int(posicion[0])
                y = int(posicion[1])
                jugadores.append( Jugador(i,(x,y)) )

        while True:
            ventana.fill(negro)
            imprimirTablero(tablero, pared, ventana)
            imprimirPuntaje(jugadorLocal, ventana, fuente)
            if(servidor.mensajesPendientes() == True):
                idJugadores = []
                for jugador in jugadores:
                    idJugadores.append(jugador.getIdentidad())
                respuesta = servidor.obtenerEstructura()
                if(respuesta != "sumaPuntos" or respuesta != "perdiste"):
                    if(respuesta in idJugadores):
                        tablero.eliminarJugador(respuesta, jugadores)
                    else:
                        for i in respuesta.keys():
                            if(i != identidad):
                                posicion = respuesta[i]
                                print("1: " + str(posicion))
                                x = int(posicion[0])
                                y = int(posicion[1])
                                for jugador in jugadores:
                                    if(jugador.getIdentidad() == i):
                                        jugador.setPosicion((x,y))
                else:
                    if(respuesta == "perdiste"):
                        exit()
                    if(respuesta == "sumaPuntos"):
                        jugadorLocal.setPuntaje("O", jugadores)

            imprimirJugador(jugadores, ventana, tablero)

            for evento in pygame.event.get():
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if(evento.type == pygame.KEYDOWN):
                    if(evento.key == K_UP):
                        moverJugador("U", jugadores, tablero, servidor)
                    if(evento.key == K_RIGHT):
                        moverJugador("R", jugadores, tablero, servidor)
                    if(evento.key == K_DOWN):
                        moverJugador("D", jugadores, tablero, servidor)
                    if(evento.key == K_LEFT):
                        moverJugador("L", jugadores, tablero, servidor)
            pygame.display.update()


if __name__=='__main__':
    main()
