class Producto():
    def __init__(self, nombre, tiempo_total, estado):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.estado = estado #No hacer nada, moviendose o ensamblando  0 , 1 , 2
        self.siguiente = None
        #validar que si puedan venir iguales 
    def get_nombre(self):
        return self.nombre  
    
    def get_tiempo_total(self):
        return self.tiempo_total   
    
    def get_estado(self):
        return self.estado    
    
    def set_estado(self, estado):
        self.estado = estado      