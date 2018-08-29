class Archivo:
    def __init__(self, name, sha1C):
        self.nombreArchivo = name
        self.sha1Complete = sha1C
        self.sha1Parts = []
        