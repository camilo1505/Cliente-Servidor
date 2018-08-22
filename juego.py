import pygame, sys, random, time
from pygame.locals import *
from librerias.tableroLibreria import *


def imprimirTablero():
    paredPosicionActual = (0,0)
    for y in range(tablero.getAltura()):
        for x in range(tablero.getAnchura()):
            paredPosicionActual = (x,y)
            if(tablero.hayPared(paredPosicionActual)):
                ventana.blit(pared.getImagen(), pared.posicionImprimir(paredPosicionActual))

def imprimirJugador(jugador):
    ventana.blit(jugador.imagenJugador(), jugador.posicionImprimirJugador())

def moverJugador(tipo, jugador, tablero):
    x,y = jugador.getPosicionLogica()
    if(tipo == "U"):
        casillaFutura = tablero.hayPared((x,y-1))
    if(tipo == "R"):
        casillaFutura = tablero.hayPared((x+1,y))
    if(tipo == "D"):
        casillaFutura = tablero.hayPared((x,y+1))
    if(tipo == "L"):
        casillaFutura = tablero.hayPared((x-1,y))
    print(casillaFutura)
    jugador.movimiento(tipo, casillaFutura)



pared = Pared("sprites/laberinto/ladrillos2.png")
tablero = Tablero()
tablero.cargarTablero()
pygame.init()
ventana = pygame.display.set_mode((pared.getAncho()*tablero.getAnchura(),pared.getAlto()*tablero.getAltura()))
pygame.display.set_caption("Pacman")
negro = (0,0,0)

jugador1 = Jugador("prueba", (1,1))



while True:
    ventana.fill(negro)
    imprimirTablero()
    imprimirJugador(jugador1)

    for evento in pygame.event.get():
        if evento.type == QUIT:
            pygame.quit()
            sys.exit()
        if(evento.type == pygame.KEYDOWN):
            if(evento.key == K_UP):
                moverJugador("U", jugador1, tablero)
            if(evento.key == K_RIGHT):
                moverJugador("R", jugador1, tablero)
            if(evento.key == K_DOWN):
                moverJugador("D", jugador1, tablero)
            if(evento.key == K_LEFT):
                moverJugador("L", jugador1, tablero)
    pygame.display.update()   