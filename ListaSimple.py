from Producto import Producto
from Token import Token
from Trabajo import Trabajo

class ListaSimple():
 
    def __init__(self):
        self.inicio_producto = None
        self.final_linea = None
        self.size_producto = 0
        
        self.inicio_token = None
        self.final_token = None
        self.size_token = 0
        
        self.inicio_elaboracion = None
        self.final_elaboracion = None
        self.size_elaboracion = 0
    
    def insertar_producto(self, nombre, tiempo_total, estado, indice_elaboracion):
        nuevo = Producto(nombre, tiempo_total, estado, indice_elaboracion)
        self.size_producto += 1
        if self.inicio_producto is None:
            self.inicio_producto = nuevo
            self.final_linea = nuevo
        else:
            tmp = self.inicio_producto
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
    
    def insertar_token(self, lexema, tipo, id, indice_elaboracion):
        nuevo = Token(lexema, tipo, id, indice_elaboracion)
        self.size_token += 1
        if self.inicio_token is None:
            self.inicio_token = nuevo
            self.final_token = nuevo
        else:
            tmp = self.inicio_token
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
    
    def insertar_elaboracion(self, numero_linea, numero_componente, indice_producto):
        nuevo = Trabajo(numero_linea, numero_componente, indice_producto)
        self.size_elaboracion += 1
        if self.inicio_elaboracion is None:
            self.inicio_elaboracion = nuevo
            self.final_elaboracion = nuevo
        else:
            tmp = self.inicio_elaboracion
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo                
    
    def guardar_trabajo(self):
        actual = self.inicio_token
        numero_linea = -1
        numero_componente = -1
        indice_elaboracion = -1
        while actual is not None:
            tmp = actual.siguiente
            if tmp is None:
                #self.insertar_elaboracion(numero_linea, numero_componente, indice_elaboracion)
                break
            if actual.get_lexema() == 'L':
                numero_linea = tmp.get_lexema()
                indice_elaboracion = actual.get_indice_elaboracion()
            if actual.get_lexema() == 'C':
                numero_componente = tmp.get_lexema()
            if actual.get_lexema() == '':   
                if self.repetidos(numero_linea, numero_componente):
                    self.insertar_elaboracion(numero_linea, numero_componente, indice_elaboracion)
                    #print('L',numero_linea, 'C',numero_componente, indice_elaboracion)
            actual = actual.siguiente 
   
    def repetidos(self, numero_linea, numero_componente):
        actual = self.inicio_elaboracion
        while actual is not None:
            if actual.get_numero_linea() == numero_linea and actual.get_numero_componente() == numero_componente:
                return False
            actual = actual.siguiente 
        return True
       
    def imprimir_tokens(self):
        print('----------------------------------')
        actual = self.inicio_token
        while actual is not None:
            print('lexema',actual.get_lexema(), 'tipo',actual.get_tipo(), 'id', actual.get_id(),'indice',actual.get_indice_elaboracion())
            actual = actual.siguiente 
    
    def imprimir_producto(self):
        print('----------------------------------')
        actual = self.inicio_producto
        while actual is not None:
            print('nombre',actual.get_nombre(), 'tiempo',actual.get_tiempo_total(), 'estado', actual.get_estado(),'indice',actual.get_indice_elaboracion())
            actual = actual.siguiente
            
    def imprimir_trabajo(self):
        print('---------Trabajo------------')
        actual = self.inicio_elaboracion
        while actual is not None:
            print('L',actual.get_numero_linea(), 'C',actual.get_numero_componente(), 'indice',actual.get_indice_producto())
            actual = actual.siguiente 
       