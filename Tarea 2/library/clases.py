class Archivo:
    def __init__(self, nombreArchivo, shaArchivo, shaPartes, listaServidores):
        self.nombre = {shaArchivo:nombreArchivo}
        self.partes = shaPartes
        self.servidores =  listaServidores
    
    def getNombreArchivo(self):
        print("Valores: {}".format(self.nombre.values()))
        for name in self.nombre.values():
            print("Name: {}".format(name))
            return name
    
    def getListaServidores(self):
        return self.servidores

    def getShaPartes(self):
        return self.partes

class Usuario:
    def __init__(self, usuario):
        self.nombreUsuario = usuario
        self.archivos = []

    def getNombreUsuario(self):
        return self.nombreUsuario
    
    def getShas(self, nombreArchivo):
        for archivo in self.archivos:
            print("Archivo: {} NombreArchivo {}".format(archivo, nombreArchivo))
            if(archivo.getNombreArchivo() == nombreArchivo):
                print("archivo get nombre {}".format(archivo.getNombreArchivo()))
                return archivo.getShaPartes()
    
    def getListaServidores(self, nombreArchivo):
        for archivo in self.archivos:
            if(archivo.getNombreArchivo() == nombreArchivo):
                return archivo.getListaServidores()

    def agregarArchivo(self, archivo):
        self.archivos.append(archivo)        