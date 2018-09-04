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
                posicionInicialCliente = servidor.posicionCliente(identidad)
                servidor.enviarMensajeA(identidad, posicionInicialCliente)
            else:
                print("Usuario Invalido")
                servidor.enviarMensajeA(identidad, "usuarioInvalido")        
        else:
            print("solicitud para Jugar sin Cupo")
            servidor.enviarMensajeA(identidad, "cupoCompleto")
    if(operacion == "listoJugar"):
        servidor.jugadorListo()
        print(servidor.getJugadoresListos())
        if(servidor.getJugadoresListos() == servidor.getCantidadMaximaJugadores()):
            mensaje = servidor.listaJugadores()
            servidor.broadCast(mensaje)
        print(servidor.getJugadoresListos())

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