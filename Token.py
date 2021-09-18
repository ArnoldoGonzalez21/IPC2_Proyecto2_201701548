class Token():
    lexema_valido = ''
    tipo = 0
    LETRA = 1
    DIGITO = 2
    SEPARADOR = 3
    ESPACIO = 4
    
    def __init__(self, lexema, tipo, id, indice_elaboracion, nombre_producto):
        self.lexema_valido = lexema
        self.tipo = tipo
        self.id = id
        self.indice_elaboracion = indice_elaboracion
        self.nombre_producto = nombre_producto
        self.siguiente = None
    
    def get_tipo(self):
        if self.tipo == self.LETRA:
            return 'Letra'
        elif self.tipo == self.DIGITO:
            return 'Digito'
        elif self.tipo == self.SEPARADOR:
            return 'Separador'
        elif self.tipo == self.ESPACIO:
            return 'Espacio'
    
    def get_lexema(self):
        return self.lexema_valido 
    
    def get_id(self):
        return self.id
    
    def get_indice_elaboracion(self):
        return self.indice_elaboracion 
    
    def get_nombre_producto(self):
        return self.nombre_producto