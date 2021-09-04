from ListaDoble import ListaDoble

class Linea():
    def __init__(self, numero, tiempo_componente, estado):
        self.numero = numero
        self.tiempo_componente = tiempo_componente
        self.estado = estado 
        self.lista_productos = ListaDoble()
        self.siguiente = None
        self.anterior = None