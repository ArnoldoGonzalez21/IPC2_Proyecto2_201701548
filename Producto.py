class Producto():
    def __init__(self, nombre, tiempo_total, estado):
        self.nombre = nombre
        self.tiempo_total = tiempo_total
        self.estado = estado 
        self.siguiente = None
        
    def get_nombre(self):
        return self.nombre  
    
    def get_tiempo_total(self):
        return self.tiempo_total   
    
    def get_estado(self):
        return self.estado    
    
    def set_estado(self, estado):
        self.estado = estado   
        
    def set_tiempo_total(self, tiempo_total):
        self.tiempo_total = tiempo_total