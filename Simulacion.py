class Simulacion():
    def __init__(self, nombre_simulacion, nombre_producto, cantidad_componentes_elaborar, componentes_terminados, cantidad_productos_simular, entro):
        self.nombre_simulacion = nombre_simulacion
        self.nombre_producto = nombre_producto
        self.cantidad_componentes_elaborar = cantidad_componentes_elaborar
        self.componentes_terminados = componentes_terminados
        self.cantidad_productos_simular = cantidad_productos_simular
        self.entro = entro
        self.siguiente = None 
    
    def get_nombre_simulacion(self):
        return self.nombre_simulacion
    
    def get_nombre_producto(self):
        return self.nombre_producto    
    
    def get_cantidad_componentes_elaborar(self):
        return self.cantidad_componentes_elaborar
    
    def set_cantidad_componentes_elaborar(self, cantidad_componentes_elaborar):
        self.cantidad_componentes_elaborar = cantidad_componentes_elaborar
        
    def get_componentes_terminados(self):
        return self.componentes_terminados 
    
    def set_componentes_terminados(self, componentes_terminados):
        self.componentes_terminados = componentes_terminados   
    
    def get_cantidad_productos_simular(self):
        return self.cantidad_productos_simular
    
    def set_cantidad_productos_simular(self, cantidad_productos_simular):
        self.cantidad_productos_simular = cantidad_productos_simular 
    
    def get_entro(self):
        return self.entro
    
    def set_entro(self, entro):
        self.entro = entro    