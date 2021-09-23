from Linea import Linea

class ListaDoble():
    
    def __init__(self):
        self.inicio_linea = None
        self.final_linea = None
        self.size_linea = 0
     
    def insertar_linea(self, numero, cantidad_componentes,tiempo_ensamblaje, estado):
        nueva_linea = Linea(numero, cantidad_componentes, tiempo_ensamblaje, estado, 0)
        self.size_linea += 1
        if self.inicio_linea is None:
            self.inicio_linea = nueva_linea
            self.final_linea = nueva_linea
        else:
            tmp = self.inicio_linea
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nueva_linea
            nueva_linea.anterior = tmp
            self.final_linea = nueva_linea
            
    def imprimir_linea(self):
        print('----------------------------------')
        actual = self.inicio_linea
        while actual is not None:
            print('numero',actual.numero, 'tiempo',actual.tiempo_ensamblaje, 'estado', actual.cantidad_mov,'cantidad_componentes',actual.cantidad_componentes)
            actual = actual.siguiente           
    
    def get_tiempo(self, numero_linea):
        actual = self.inicio_linea
        while actual is not None: 
            if actual.numero == numero_linea:
                return actual.tiempo_ensamblaje
            actual = actual.siguiente
    
    def solicitar_ultima_posicion_linea(self, numero_linea):
        actual = self.inicio_linea
        ultima_posicion = 0
        while actual is not None:
            if int(actual.numero) == int(numero_linea):     
                ultima_posicion = actual.get_ultima_posicion()
                return ultima_posicion 
            actual = actual.siguiente        
        return 0  
    
    def guardar_ultima_posicion_linea(self, numero_linea, ultima_posicion):
        actual = self.inicio_linea
        while actual is not None:
            if int(actual.numero) == int(numero_linea):
                actual.set_ultima_posicion(ultima_posicion)
                return
            actual = actual.siguiente  
    
    def guardar_cantidad_mov(self, numero_linea, cant_mov):
        actual = self.inicio_linea
        while actual is not None:
            if int(actual.numero) == int(numero_linea):
                suma = int(actual.get_cantidad_mov()) + int(cant_mov)
                actual.set_cantidad_mov(suma)
                print(suma, 'suma')
                return
            actual = actual.siguiente
    
    def solicitar_cantidad_mov(self, numero_linea):
        actual = self.inicio_linea
        while actual is not None:
            if int(actual.numero) == int(numero_linea):
                cant_mov = actual.get_cantidad_mov()
                return cant_mov
            actual = actual.siguiente                                  