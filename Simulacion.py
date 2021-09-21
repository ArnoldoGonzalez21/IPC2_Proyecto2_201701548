class Simulacion():
    def __init__(self, nombre_simulacion, nombre_producto, cantidad_componentes_elaborar):
        self.nombre_simulacion = nombre_simulacion
        self.nombre_producto = nombre_producto
        self.cantidad_componentes_elaborar = cantidad_componentes_elaborar
        self.siguiente = None 
    
    def get_nombre_simulacion(self):
        return self.nombre_simulacion
    
    def get_nombre_producto(self):
        return self.nombre_producto    
    
    def get_cantidad_componentes_elaborar(self):
        return self.cantidad_componentes_elaborar
    
    def set_cantidad_componentes_elaborar(self, cantidad_componentes_elaborar):
        self.cantidad_componentes_elaborar = cantidad_componentes_elaborar