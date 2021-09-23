class Linea():
    def __init__(self, numero, cantidad_componentes, tiempo_ensamblaje, cantidad_mov, ultima_posicion):
        self.numero = numero
        self.cantidad_componentes = cantidad_componentes
        self.tiempo_ensamblaje = tiempo_ensamblaje
        self.cantidad_mov = cantidad_mov 
        self.ultima_posicion = ultima_posicion
        self.siguiente = None
        self.anterior = None 
    
    def get_cantidad_mov(self):
        return self.cantidad_mov
    
    def set_cantidad_mov(self, cantidad_mov):
        self.cantidad_mov = cantidad_mov
    
    def get_ultima_posicion(self):
        return self.ultima_posicion
        
    def set_ultima_posicion(self, ultima_posicion):
        self.ultima_posicion = ultima_posicion