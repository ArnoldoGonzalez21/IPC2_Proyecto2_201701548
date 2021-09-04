from Linea import Linea

class ListaDoble():
    
    def __init__(self):
        self.inicio = None
        self.final = None
        self.size = 0
     
    def insertar_linea(self, numero, tiempo_componente, estado):
        nueva_linea = Linea(numero, tiempo_componente, estado)
        self.size += 1
        if self.inicio is None:
            self.inicio = nueva_linea
            self.final = nueva_linea
        else:
            tmp = self.inicio
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nueva_linea
            nueva_linea.anterior = tmp
            self.final = nueva_linea 