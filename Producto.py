class Producto():
    def __init__(self, nombre, tiempo, estado):
        self.nombre = nombre
        self.tiempo = tiempo
        self.estado = estado #No hacer nada, moviendose o ensamblando  0 , 1 , 2
        self.siguiente = None
        self.anterior = None