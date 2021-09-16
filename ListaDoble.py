from Linea import Linea

class ListaDoble():
    
    def __init__(self):
        self.inicio_linea = None
        self.final_linea = None
        self.size_linea = 0
     
    def insertar_linea(self, numero, cantidad_componentes,tiempo_ensamblaje, estado):
        nueva_linea = Linea(numero, cantidad_componentes, tiempo_ensamblaje, estado)
        self.size_linea += 1
        if self.inicio_linea is None:
            self.inicio_linea = nueva_linea
            self.final_linea = nueva_linea
        else:
            tmp = self.inicio_linea
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nueva_linea
            nueva_linea.anterior = tmp
            self.final_linea = nueva_linea 