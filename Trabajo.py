class Trabajo():
    def __init__(self, numero_linea, numero_componente, indice_producto):
        self.numero_linea = numero_linea
        self.numero_componente = numero_componente
        self.indice_producto = indice_producto
        self.siguiente = None
    
    def get_numero_linea(self):
        return self.numero_linea
    
    def get_numero_componente(self):
        return self.numero_componente
    
    def get_indice_producto(self):
        return self.indice_producto  
