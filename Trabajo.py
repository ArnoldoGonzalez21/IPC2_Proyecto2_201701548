class Trabajo():
    def __init__(self, numero_linea, numero_componente, tiempo, indice_producto, nombre_producto, tiempo_total, estado):
        self.numero_linea = numero_linea
        self.numero_componente = numero_componente
        self.indice_producto = indice_producto
        self.tiempo = tiempo
        self.nombre_producto = nombre_producto
        self.tiempo_total = tiempo_total #tiempo que tardo en este producto
        self.estado = estado #No hacer nada, moviendose o ensamblando  0 , 1 , 2
        self.siguiente = None
        self.anterior = None
    
    def get_numero_linea(self):
        return self.numero_linea
    
    def get_numero_componente(self):
        return self.numero_componente
    
    def get_indice_producto(self):
        return self.indice_producto  
    
    def get_nombre_producto(self):
        return self.nombre_producto  
    
    def get_tiempo(self):
        return self.tiempo

    def set_tiempo(self, nuevo_tiempo):
        self.tiempo = nuevo_tiempo
        
    def get_tiempo_total(self):
        return self.tiempo_total 
        
    def set_tiempo_total(self, tiempo_total):
        self.tiempo_total = tiempo_total     