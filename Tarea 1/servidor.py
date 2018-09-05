import zmq, time
import sys
from librerias.libreriaServidor import *

def recibidor(servidor, identidad, operacion, contenido):
    if(operacion == "solicitudJugar"):
        if(servidor.hayCupo()):
            print("hay Cupo Disponible")
            if(servidor.usuarioValido(identidad)):
                print("Usuario Valido")
                servidor.registrarNuevoJugador(identidad)
                posicionInicial = servidor.posicionCliente(identidad)
                mensaje = servidor.descomponerJson(posicionInicial)
                servidor.enviarMensajeA(identidad, mensaje)
            else:
                print("Usuario Invalido")
                servidor.enviarMensajeA(identidad, "errorUsuario")        
        else:
            print("solicitud para Jugar sin Cupo")
            servidor.enviarMensajeA(identidad, "errorCompleto")
    if(operacion == "listoJugar"):
        servidor.jugadorListo()
        if(servidor.getJugadoresListos() == servidor.getCantidadMaximaJugadores()):
            servidor.enviarPosiciones()
        print("Jugadores Listos: " + str(servidor.getJugadoresListos()))
    if(operacion == "cambiarPosicion"):
        print("Contenido: " + contenido)
        servidor.cambiarPosicion(identidad, contenido)
        servidor.enviarPosiciones()

def decodificador(variable):
    return variable.decode('ascii')

def main():
    if len(sys.argv) != 2:
        print("Faltan Argumentos: <cantidadJugadores>")
        exit()

    servidor = Servidor(int(sys.argv[1]))
    servidor.iniciarServidor()
    print("Servidor Operacional, cantidad de jugadores: " + str(servidor.getCantidadMaximaJugadores()))

    while(True):
        identidad, operacion, contenido = servidor.recibirMensajeCliente()

        print("Operacion <" + operacion + "> recibida de <" + identidad + ">")
        recibidor(servidor, identidad, operacion, contenido)

        
            





if __name__ == '__main__':
    main()