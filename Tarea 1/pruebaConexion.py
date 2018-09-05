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

    solicitud = ("listoJugar", "")
    servidor.enviarSolicitud(solicitud)
    respuesta = servidor.obtenerEstructura()
    print(respuesta)
    print(respuesta['ba'])

    solicitud = ("cambiarPosicion","[4,3]")
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