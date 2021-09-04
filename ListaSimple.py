from Trabajo import Trabajo

class ListaSimple():
    def __init__(self):
        self.inicio = None
        self.final = None
        self.size = 0
     
    def insertar_trabajo(self, linea, componente):
        nuevo = Trabajo(linea, componente,)
        self.size += 1
        if self.inicio is None:
            self.inicio = nuevo
            self.final = nuevo
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            self.final = nuevo 