class Simulacion():
    def __init__(self, nombre_simulacion, nombre_producto):
        self.nombre_simulacion = nombre_simulacion
        self.nombre_producto = nombre_producto
        self.siguiente = None 
    
    def get_nombre_simulacion(self):
        return self.nombre_simulacion
    
    def get_nombre_producto(self):
        return self.nombre_producto    