from ListaSimple import ListaSimple
from Token import Token

class Analizador():
    
    tokens = ListaSimple()   
    lexema = ''
    estado = 0
    id = 0
    tipos = Token("Lexema",-1,-1,-1)
    
    def agregar_token(self, tipo, indice_elaboracion):
        self.tokens.insertar_token(self.lexema, tipo, self.id, indice_elaboracion)
        self.lexema = ''
        self.id += 1
    
    def analizador_estados(self, entrada, indice_elaboracion):
        self.estado = 0
        self.lexema = ''
        entrada += '¬'
        #print(entrada)
        actual = ''
        longitud = len(entrada)
        for contador in range(longitud):
            actual = entrada[contador]
            if self.estado == 0:
                if actual == 'L':
                    self.estado = 1
                    self.lexema += actual
                    self.agregar_token(self.tipos.LETRA, indice_elaboracion)
                
            elif self.estado == 1:
                if actual.isdigit():
                    self.estado = 2
                    self.lexema += actual
                  
            elif self.estado == 2:
                if actual.isdigit():
                    self.estado = 2
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.DIGITO, indice_elaboracion) 
                    
                if actual == 'p': 
                    self.estado = 3
                    self.lexema += actual  
                    self.agregar_token(self.tipos.SEPARADOR, indice_elaboracion)  
                      
            elif self.estado == 3:         
                if actual == 'C': 
                    self.estado = 4
                    self.lexema += actual 
                    self.agregar_token(self.tipos.LETRA,indice_elaboracion)                
                    
            elif self.estado == 4: 
                if actual.isdigit():
                    self.estado = 5
                    self.lexema += actual                   
                                
            elif self.estado == 5:
                if actual.isdigit():
                    self.estado = 5
                    self.lexema += actual
                else:
                    self.agregar_token(self.tipos.DIGITO, indice_elaboracion)     
                if actual == ' ':
                    self.agregar_token(self.tipos.ESPACIO, indice_elaboracion)
                    self.estado = 0  
    def tamano(self):
        #self.tokens.imprimir_tokens()
        self.tokens.guardar_trabajo()   
        self.tokens.imprimir_trabajo()           
                    
              