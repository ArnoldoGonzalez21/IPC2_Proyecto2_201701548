class NodoEncabezado():
    def __init__(self, id):
        self.id = id #posicion de fila o columna
        self.siguiente = None
        self.anterior = None
        self.acceso = None #-- apuntador a los nodos de la matriz(nodos internos)
