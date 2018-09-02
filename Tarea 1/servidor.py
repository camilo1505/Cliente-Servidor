import zmq
import sys

def recibidor(identidad, operacion, contenido, cantidadJugadores, jugadoresRegistrados):
    if(operacion == 'solicitudJugar'):
        if(len(jugadoresRegistrados) == cantidadJugadores):
            mensaje = bytes("cupoCompleto",'ascii')
            socket.send_mutipart([identidad, mensaje])

def decodificador(variable):
    return variable.decode('ascii')

def main():
    if len(sys.argv) != 2:
        print("Faltan Argumentos: <cantidadJugadores>")
        exit()
    
    cantidadJugadores = sys.argv[1]
    jugadoresRegistrados = []
    
    contexto = zmq.Context()
    socket = contexto.socket(zmq.ROUTER)

    socket.bind("tcp://*:5555")
    print("Servidor Operacional, cantidad de jugadores: " + str(cantidadJugadores))

    while(True):
        byteIdentidad, byteOperacion, byteContenido = socket.recv_multipart()
        identidad = decodificador(byteIdentidad)
        operacion = decodificador(byteOperacion)
        contenido = decodificador(byteContenido)
        
        print("Operacion <" + operacion + "> recibida de <" + identidad + ">")
        recibidor(identidad, operacion, contenido, cantidadJugadores, jugadoresRegistrados)

        
            





if __name__ == '__main__':
    main()