import sys, time
from librerias.tableroLibreria import *

def main():
    if len(sys.argv) != 2:
        print("Faltan Argumentos: <identidad>")
        exit()
    
    identidad = sys.argv[1]

    servidor = Conexion(identidad)
    servidor.iniciarConexion("localhost")
    servidor.iniciarPoller()

    solicitud = ("solicitudJugar", "")
    servidor.enviarSolicitud(solicitud)
    respuesta = servidor.obtenerMensaje()
    print(respuesta)

    while(respuesta != 'ok'):
        solicitud = ("empezarJugar", "")
        servidor.enviarSolicitud(solicitud)
        respuesta = servidor.obtenerMensaje()
        print(respuesta)
        time.sleep(4)
    
    solicitud = ("listaJugadores", "")
    servidor.enviarSolicitud(solicitud)
    respuesta = servidor.obtenerMensaje()
    print(respuesta)

    
    """if(servidor.mensajesPendientes() == False):
        solicitud = ("solicitudJugar", "")
        servidor.enviarSolicitud(solicitud)
    if(servidor.mensajesPendientes() == True):
        print(identidad)
        print(operacion)"""

if __name__=='__main__':
    main()