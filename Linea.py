class Linea():
    def __init__(self, numero, cantidad_componentes, tiempo_ensamblaje, estado):
        self.numero = numero
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.estado = estado 
        self.siguiente = None
        self.anterior = None 