import sys
from librerias.tableroLibreria import *

def main():
    if len(sys.argv) != 4:
        print("Faltan Argumentos: <identidad> <operacion> <mensaje>")
        exit()
    
    identidad = sys.argv[1]
    operacion = sys.argv[2]
    mensaje = sys.argv[3]

    servidor = Conexion(identidad)
    servidor.iniciarConexion("localhost")
    servidor.iniciarPoller()

    solicitud = ("solicitudJugar", "")
    servidor.enviarSolicitud(solicitud)
    identidad, operacion = servidor.obtenerMensaje()
    
    """if(servidor.mensajesPendientes() == False):
        solicitud = ("solicitudJugar", "")
        servidor.enviarSolicitud(solicitud)
    if(servidor.mensajesPendientes() == True):
        print(identidad)
        print(operacion)"""

if __name__=='__main__':
    main()