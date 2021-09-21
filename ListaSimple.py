from Producto import Producto
from Token import Token
from Trabajo import Trabajo
from Simulacion import Simulacion
from MatrizDispersa import MatrizDispersa

primer_componente = True
termino = False

class ListaSimple():
    matriz = MatrizDispersa(0)
    
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
        
        self.inicio_simulacion = None
        self.final_simulacion = None
        self.size_simulacion = 0        
    
    def insertar_producto(self, nombre):
        nuevo = Producto(nombre, 0, 0)
        self.size_producto += 1
        if self.inicio_producto is None:
            self.inicio_producto = nuevo
            self.final_linea = nuevo
        else:
            tmp = self.inicio_producto
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
    
    def insertar_token(self, lexema, tipo, id, indice_elaboracion, nombre_producto):
        nuevo = Token(lexema, tipo, id, indice_elaboracion, nombre_producto)
        self.size_token += 1
        if self.inicio_token is None:
            self.inicio_token = nuevo
            self.final_token = nuevo
        else:
            tmp = self.inicio_token
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
    
    def insertar_elaboracion(self, numero_linea, numero_componente, tiempo, indice_producto, nombre_producto):
        nuevo = Trabajo(numero_linea, numero_componente, tiempo, indice_producto, nombre_producto, 0, 1, 0)
        self.size_elaboracion += 1
        if self.inicio_elaboracion is None:
            self.inicio_elaboracion = nuevo
            self.final_elaboracion = nuevo
        else:
            tmp = self.inicio_elaboracion
            while tmp.siguiente is not None:
                tmp = tmp.siguiente
            tmp.siguiente = nuevo
            nuevo.anterior = tmp
            self.final_elaboracion = nuevo               
    
    def insertar_simulacion(self, nombre_simulacion, nombre_producto, cantidad_productos_simular):
        nuevo = Simulacion(nombre_simulacion, nombre_producto, 0, 0, cantidad_productos_simular, False)
        self.size_simulacion += 1
        if self.inicio_simulacion is None:
            self.inicio_simulacion = nuevo
            self.final_elaboracion = nuevo
        else:
            tmp = self.inicio_simulacion
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
                break
            if actual.get_lexema() == 'L':
                numero_linea = tmp.get_lexema()
                indice_elaboracion = actual.get_indice_elaboracion()
                nombre_producto = actual.get_nombre_producto()
            if actual.get_lexema() == 'C':
                numero_componente = tmp.get_lexema()
            if actual.get_lexema() == '':   
                if self.repetidos(numero_linea, numero_componente, indice_elaboracion):
                    self.insertar_elaboracion(numero_linea, numero_componente, 0, indice_elaboracion, nombre_producto)
                    #print('L',numero_linea, 'C',numero_componente, indice_elaboracion)
            actual = actual.siguiente 

    def llenar_matriz(self):
        actual = self.inicio_elaboracion
        while actual is not None:
            pos_x = actual.get_numero_linea()
            pos_y = actual.get_numero_componente()
            tiempo = actual.get_tiempo()
            self.matriz.insert(pos_x, pos_y, tiempo)
            actual = actual.siguiente
        #self.matriz.sizep() 
        self.matriz.generarGraphviz(True) 
        
    def recorrer_tiempo_elaboracion(self, nombre_producto):
        actual = self.inicio_elaboracion
        while actual is not None:
            tmp = actual.siguiente
            if nombre_producto == actual.get_nombre_producto():
                if int(actual.get_numero_componente()) == int(actual.get_contador_posicion()) and int(actual.get_estado()) != 2:
                    
                    actual.set_estado(2) 
                    nuevo_tiempo = int(actual.get_tiempo_total()) + int(actual.get_tiempo()) 
                    actual.set_tiempo_total(nuevo_tiempo)
                    if tmp is not None and tmp.get_nombre_producto() == nombre_producto:
                        cont_act = actual.get_numero_componente()
                        tmp.set_contador_posicion(cont_act)
                    return 1

                elif int(actual.get_numero_componente()) != int(actual.get_contador_posicion()) and int(actual.get_estado()) != 2:
                    actual.set_estado(1)
                    nuevo_tiempo = int(actual.get_tiempo_total()) + 1
                    actual.set_tiempo_total(nuevo_tiempo)
                    if int(actual.get_numero_componente()) > int(actual.get_contador_posicion()):
                        cont_act = int(actual.get_contador_posicion()) + 1
                        actual.set_contador_posicion(cont_act)
                    elif int(actual.get_numero_componente()) < int(actual.get_contador_posicion()):
                        cont_act = int(actual.get_contador_posicion()) - 1
                        actual.set_contador_posicion(cont_act)
                    return 0
            actual = actual.siguiente  
            
    def recorrer_simulacion(self, tokens):
        contador = 0
        while True:
            actual = self.inicio_simulacion
            while actual is not None:
                if int(actual.get_componentes_terminados()) != int(actual.get_cantidad_componentes_elaborar()):
                    nombre_producto = actual.get_nombre_producto()
                    TK_cont = tokens.recorrer_tiempo_elaboracion(nombre_producto)
                    num_terminados = int(actual.get_componentes_terminados()) + TK_cont
                    actual.set_componentes_terminados(num_terminados)
                    
                elif int(actual.get_componentes_terminados()) == int(actual.get_cantidad_componentes_elaborar()) and not actual.get_entro():
                    actual.set_entro(True)
                    contador += 1
                if contador >= actual.get_cantidad_productos_simular():
                    return  
                actual = actual.siguiente
    
    def guardar_numero_componentes_simulacion(self, tokens):
        actual = self.inicio_simulacion
        while actual is not None:
            nombre = actual.get_nombre_producto()
            num_componentes = tokens.recorrer_trabajo(nombre)
            actual.set_cantidad_componentes_elaborar(num_componentes)
            actual = actual.siguiente              
    
    def recorrer_trabajo(self, nombre_producto):
        actual = self.inicio_elaboracion
        contador = 0
        while actual is not None:
            if actual.get_nombre_producto() == nombre_producto:
                contador += 1
            actual = actual.siguiente 
        return contador    
    
        
    def colocar_tiempo(self, lineas):
        actual = self.inicio_elaboracion
        while actual is not None:
            numero_linea = actual.get_numero_linea()
            tiempo_ensamblaje = lineas.get_tiempo(numero_linea)
            actual.set_tiempo(tiempo_ensamblaje)
            actual = actual.siguiente
    
    def repetidos(self, numero_linea, numero_componente, indice_elaboracion):
        actual = self.inicio_elaboracion
        while actual is not None:
            if actual.get_numero_linea() == numero_linea and actual.get_numero_componente() == numero_componente and actual.get_indice_producto() == indice_elaboracion:
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
        print('---------------Producto-------------------')
        actual = self.inicio_producto
        while actual is not None:
            print('nombre',actual.get_nombre(), 'tiempo',actual.get_tiempo_total(), 'estado', actual.get_estado(),'indice',actual.get_indice_elaboracion(),'num_comp', actual.get_cantidad_componentes_elaborar())
            actual = actual.siguiente
            
    def imprimir_trabajo(self):
        print('---------Trabajo------------')
        actual = self.inicio_elaboracion
        while actual is not None:
            print('L',actual.get_numero_linea(), 'C',actual.get_numero_componente(), 'tiempo',actual.get_tiempo(), 'indice',actual.get_indice_producto(), 'nombre',actual.get_nombre_producto(), 'tiempo_total', actual.get_tiempo_total())
            actual = actual.siguiente 
    
    def imprimir_simulacion(self):
        print('---------Simulacion------------')
        actual = self.inicio_simulacion
        while actual is not None:
            print('nombre simul',actual.get_nombre_simulacion(), 'nombre',actual.get_nombre_producto(), 'cant_pro',actual.get_cantidad_componentes_elaborar())
            actual = actual.siguiente 
    
       