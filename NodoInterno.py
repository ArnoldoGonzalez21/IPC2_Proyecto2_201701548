class NodoInterno(): 
    def __init__(self, x, y, tiempo):
        self.tiempo = tiempo
        self.coordenadaX = x  # fila
        self.coordenadaY = y  # columna
        self.arriba = None
        self.abajo = None
        self.derecha = None  # self.siguiente
        self.izquierda = None  # self.anterior