class Archivo:
    def __init__(self, nombreArchivo, shaArchivo, shaPartes, listaServidores):
        self.nombre = {shaArchivo:nombreArchivo}
        self.partes = shaPartes
        self.servidores =  listaServidores
    
    def getNombreArchivo(self):
        for name in self.nombre.values():
            return name
    
    def getListaServidores(self):
        return self.servidores

    def getShaPartes(self):
        return self.partes
    
    def getSha(self):
        for sha in self.nombre.keys():
            return sha

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
        else:
            print("No se encontro el archivo {}".format(nombreArchivo))
            exit()
    
    def getListaServidores(self, nombreArchivo):
        for archivo in self.archivos:
            if(archivo.getNombreArchivo() == nombreArchivo):
                return archivo.getListaServidores()

    def getArchivos(self):
        return self.archivos

    def getNombresArchivos(self):
        listAux = []
        for archivo in self.archivos:
            listAux.append(archivo.getNombreArchivo())
        return listAux

    def agregarArchivo(self, archivo):
        self.archivos.append(archivo)        