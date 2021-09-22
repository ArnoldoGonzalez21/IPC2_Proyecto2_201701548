from ListaSimple import ListaSimple
from Token import Token

class Analizador():
    
    tokens = ListaSimple()   
    lexema = ''
    estado = 0
    id = 0
    tipos = Token("Lexema",-1,-1,-1,'')
    
    def agregar_token(self, tipo, indice_elaboracion, nombre_producto):
        self.tokens.insertar_token(self.lexema, tipo, self.id, indice_elaboracion, nombre_producto)
        self.lexema = ''
        self.id += 1
    
    def analizador_estados(self, entrada, indice_elaboracion, nombre_producto):
        self.estado = 0
        self.lexema = ''
        entrada += '¬'
        actual = ''
        longitud = len(entrada)
        for contador in range(longitud):
            actual = entrada[contador]
            if self.estado == 0:
                if actual == 'L':
                    self.estado = 1
                    self.lexema += actual
                    self.agregar_token(self.tipos.LETRA, indice_elaboracion, nombre_producto)
                
            elif self.estado == 1:
                if actual.isdigit():
                    self.estado = 2
                    self.lexema += actual
                  
            elif self.estado == 2:
                if actual.isdigit():
                    self.estado = 2
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.DIGITO, indice_elaboracion, nombre_producto) 
                    
                if actual == 'p': 
                    self.estado = 3
                    self.lexema += actual  
                    self.agregar_token(self.tipos.SEPARADOR, indice_elaboracion, nombre_producto)  
                      
            elif self.estado == 3:         
                if actual == 'C': 
                    self.estado = 4
                    self.lexema += actual 
                    self.agregar_token(self.tipos.LETRA,indice_elaboracion, nombre_producto)                
                    
            elif self.estado == 4: 
                if actual.isdigit():
                    self.estado = 5
                    self.lexema += actual                   
                                
            elif self.estado == 5:
                if actual.isdigit():
                    self.estado = 5
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.DIGITO, indice_elaboracion, nombre_producto)     
                if actual == ' ':
                    self.agregar_token(self.tipos.ESPACIO, indice_elaboracion, nombre_producto)
                    self.estado = 0  
    def tamano(self, lineas):
        self.tokens.guardar_trabajo()  
        self.tokens.colocar_tiempo(lineas)  
        #self.tokens.imprimir_trabajo() 
        self.tokens.llenar_matriz()
    
    def elaboracion_combo(self, nombre_producto, tabla, END):
        self.tokens.recorrer_tiempo_elaboracion_combo(nombre_producto, tabla, END)
        self.tokens.imprimir_trabajo()
    
    def get_tokens(self):
        return self.tokens
    
    def text_elaboracion(self, nombre_producto):
        return self.tokens.proceso_elaboracion_label(nombre_producto)  