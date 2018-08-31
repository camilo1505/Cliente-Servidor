import pygame, sys, random, time
from pygame.locals import *
from librerias.tableroLibreria import *


def imprimirTablero(tablero, pared):
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

def imprimirJugador(jugadores):
    for jugador in jugadores:
        ventana.blit(jugador.imagenJugador(), jugador.posicionImprimirJugador())

def moverJugador(tipo, jugadores, tablero):
    jugador = jugadores[0]
    x,y = jugador.getPosicionLogica()
    siguienteCasilla = (0,0)
    if(tipo == "U"):
        casillaFutura = tablero.hayObstaculo((x,y-1), jugadores)
        siguienteCasilla = (x,y-1)
    if(tipo == "R"):
        casillaFutura = tablero.hayObstaculo((x+1,y), jugadores)
        siguienteCasilla = (x+1,y)
    if(tipo == "D"):
        casillaFutura = tablero.hayObstaculo((x,y+1), jugadores)
        siguienteCasilla = (x,y+1)
    if(tipo == "L"):
        casillaFutura = tablero.hayObstaculo((x-1,y), jugadores)
        siguienteCasilla = (x-1,y)
    print(casillaFutura)
    
    if(tablero.hayGalletaGrande(siguienteCasilla) or tablero.hayGalletaPequena(siguienteCasilla)):
        if(jugador.getRol() == 0):
            jugador.setPuntaje(tablero.contenidoMapa(siguienteCasilla), jugadores)
            tablero.cambioCasilla(siguienteCasilla)
    
    print(jugador.getPuntaje())

    jugador.movimiento(tipo, casillaFutura)



pared = Pared("sprites/laberinto/ladrillos2.png")
tablero = Tablero()
tablero.cargarTablero()
pygame.init()
ventana = pygame.display.set_mode((pared.getAncho()*tablero.getAnchura(),pared.getAlto()*tablero.getAltura()))
pygame.display.set_caption("Pacman")
negro = (0,0,0)

jugadores = [Jugador("prueba", (1,1)), Jugador("prueba2", (1,2))]


while True:
    ventana.fill(negro)
    imprimirTablero(tablero, pared)
    imprimirJugador(jugadores)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        if(evento.type == pygame.KEYDOWN):
            if(evento.key == K_UP):
                moverJugador("U", jugadores, tablero)
            if(evento.key == K_RIGHT):
                moverJugador("R", jugadores, tablero)
            if(evento.key == K_DOWN):
                moverJugador("D", jugadores, tablero)
            if(evento.key == K_LEFT):
                moverJugador("L", jugadores, tablero)
    pygame.display.update()   