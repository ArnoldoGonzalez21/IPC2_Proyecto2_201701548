from tkinter import Tk
from Producto import Producto
from Token import Token
from Trabajo import Trabajo
from Simulacion import Simulacion
from MatrizDispersa import MatrizDispersa
from os import system, startfile

primer_componente = True
termino = False
tiempo_total_mayor = 0  
tiempo_segundos = 0

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
        #self.matriz.generarGraphviz(True) 
    
    def get_tiempo_total_producto(self, nombre_producto) -> str:
        actual = self.inicio_producto
        total = 0
        while actual is not None:
            if nombre_producto == actual.get_nombre():
                total = int(actual.get_tiempo_total())
            actual = actual.siguiente   
        return str(total)     
    
    def set_tiempo_total_producto(self, nombre_producto, tokens):
        actual = self.inicio_producto
        while actual is not None:
            if nombre_producto == actual.get_nombre():
                actual.set_tiempo_total(tokens.get_tiempo_total_suma_productos(nombre_producto))
                print(actual.get_tiempo_total())
            actual = actual.siguiente
    
    def get_tiempo_total_suma_productos(self, nombre_producto) -> int :
        actual = self.inicio_elaboracion
        tiempo_total = 0
        while actual is not None:
            if nombre_producto == actual.get_nombre_producto():
                tiempo_total += int(actual.get_tiempo_total())
            actual = actual.siguiente
        return tiempo_total   
    
    def get_tiempo_seg(self):
        global tiempo_segundos
        return tiempo_segundos
    
    def recorrer_elaboracion_lineas_combo2(self, nombre_producto, lineas, tabla, END): #, tabla, END, lineas
        global tiempo_segundos
        ultimo_componente = 0
        linea_mayor = 0
        tamano = 0
        movimiento_entre_componentes = 0
        actual = self.inicio_elaboracion
        while actual is not None:
            if actual.get_nombre_producto() == nombre_producto:
                tamano += 1
                tmp_mayor = int(actual.get_numero_linea())
                if tmp_mayor > linea_mayor:
                    linea_mayor = tmp_mayor
            actual = actual.siguiente  
                  
        actual = self.inicio_elaboracion
        while actual is not None:
            if actual.get_nombre_producto() == nombre_producto:                
                ultimo_componente = lineas.solicitar_ultima_posicion_linea(int(actual.get_numero_linea())) 
                if ultimo_componente != 0:
                    movimiento_entre_componentes = int(actual.get_numero_componente()) - int(ultimo_componente)
                    movimiento_entre_componentes = abs(movimiento_entre_componentes)
                    print('movimiento_entre_componentes',movimiento_entre_componentes) 
                    lineas.guardar_cantidad_mov(int(actual.get_numero_linea()), movimiento_entre_componentes)
                    #if int(movimiento_entre_componentes) + int(actual.get_numero_componente()) > int(linea_mayor):
                    tiempo_segundos += movimiento_entre_componentes  
                lineas.guardar_ultima_posicion_linea(int(actual.get_numero_linea()), int(actual.get_numero_componente()))
                tiempo_segundos += int(actual.get_tiempo())
                tabla.insert('',END, text = tiempo_segundos, values=(actual.get_numero_linea(),actual.get_numero_componente()))  
            actual = actual.siguiente
        
        tiempo_segundos += linea_mayor
        print(tiempo_segundos, 'tiempo segundos global')                 
           
    def recorrer_tiempo_elaboracion_combo(self, nombre_producto, tabla, END): #fila por fila
        self.tiempo_total = 0
        global primer_componente
        primer_componente = True
        actual = self.inicio_elaboracion
        while actual is not None:
            tmp = actual.siguiente
            if nombre_producto == actual.get_nombre_producto():
                tiempo_tirada = 0
                tiempo = int(actual.get_tiempo())
                if primer_componente:
                    num_comp = int(actual.get_numero_componente())
                    primer_componente = False
                    tiempo_tirada = tiempo + num_comp
                else:    
                    movimiento = int(actual.get_contador_posicion()) - int(actual.get_numero_componente())
                    movimiento = abs(movimiento)
                    tiempo_tirada = tiempo + movimiento
                if tmp is not None and nombre_producto == tmp.get_nombre_producto() and actual.get_numero_linea() == tmp.get_numero_linea():
                    num_comp = int(actual.get_numero_componente())
                    tmp.set_contador_posicion(num_comp)
                self.tiempo_total += tiempo_tirada
                tabla.insert('',END, text = self.tiempo_total, values=(actual.get_numero_linea(),actual.get_numero_componente()))    
                actual.set_tiempo_total(tiempo_tirada)
            actual = actual.siguiente  
    
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
    
    def proceso_elaboracion_label(self, nombre_producto):
        actual = self.inicio_elaboracion
        contenido = ''
        while actual is not None:
            if nombre_producto == actual.get_nombre_producto():
                contenido += 'L'+str(actual.get_numero_linea())+ ' - C'+str(actual.get_numero_componente())+'\n'
            actual = actual.siguiente
        return contenido
    
    def opciones_productos_combo(self, combo):
        nombres = []
        values = list(combo["values"])
        actual = self.inicio_producto
        while actual is not None:       
            nombres.append(actual.get_nombre()) 
            actual = actual.siguiente
        combo["values"] = values + nombres
         
    def set_columnas_tabla_simulacion(self, con_archivo):
        if con_archivo:
            numero = 0
            columns = []
            actual = self.inicio_simulacion
            while actual is not None:
                numero = actual.get_cantidad_productos_simular()
                actual = actual.siguiente
            for i in range(numero):
                nueva_colum = '#'+str(i + 1)
                columns.insert(len(columns),nueva_colum)
        print(tuple(columns))        
        return tuple(columns)
    
    def set_heading_tabla_simulacion(self, tabla, con_archivo): #mas o menos funciona
        if con_archivo:
            contador = 1
            actual = self.inicio_simulacion
            while actual is not None:
                nombre :str = actual.get_nombre_producto()
                tabla.heading('#'+str(contador), text = nombre)
                contador += 1
                actual = actual.siguiente     
    
    def nodos_cola_secuencia(self, nombre_producto):
        entro_columna = False
        contenido_nodo = ''
        contenido_enlace_nodo = ''
        contenido_rank = '{rank = same;raiz'
        tamano = 0
        contador = 1
        actual = self.inicio_elaboracion
        while actual is not None:
            if actual.get_nombre_producto() == nombre_producto:
                tamano += 1
            actual = actual.siguiente
            
        actual = self.inicio_elaboracion    
        while actual is not None:
            if actual.get_nombre_producto() == nombre_producto:
                contenido_nodo += 'nodo'+str(contador)+'[label = "L'+actual.get_numero_linea()+'C'+actual.get_numero_componente()+'\", group = '+str(contador + 1)+', fillcolor="#E9FFFC", shape = note];\n'
                if not entro_columna:
                    contenido_enlace_nodo += 'raiz -> nodo'+str(contador)+';\n'
                    entro_columna = True
                if contador + 1 <= tamano: 
                    contenido_enlace_nodo += 'nodo'+str(contador)+' -> nodo'+str(contador + 1)+';\n'        
                contenido_rank += '; nodo'+str(contador)  
                contador += 1  
                             
            actual = actual.siguiente
        contenido_rank += '}\n'
        contenido = contenido_nodo + contenido_enlace_nodo + contenido_rank
        return contenido
    
    def generar_graphviz_secuencia(self, nombre_producto, tokens):
        inicio_graphviz = '''
        digraph L{
            node[shape = folder fillcolor="#F8DEA1" style = filled]
            subgraph cluster_p{
            label = \"Reporte Cola de Secuencia '''+nombre_producto+''' \"
            bgcolor = "#398D9C"
                raiz[label = "INICIO"]
                edge[dir = "right"]
        '''
        nodos = tokens.nodos_cola_secuencia(nombre_producto)
        
        final_graphviz = '}\n}'
        graphviz = inicio_graphviz + nodos + final_graphviz
        nombre_producto = nombre_producto.replace(" ","")
        miArchivo= open(nombre_producto+'.dot','w')
        miArchivo.write(graphviz)
        miArchivo.close()
        system('dot -Tpng ' +nombre_producto+'.dot -o '+nombre_producto+'.png')
        system('cd ./'+nombre_producto+'.png')
        startfile(nombre_producto+'.png')
            
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
            print('L',actual.get_numero_linea(), 'C',actual.get_numero_componente(), 'tiempo',actual.get_tiempo(), 'indice',actual.get_indice_producto(), 'nombre',actual.get_nombre_producto(), 'tiempo_total', actual.get_tiempo_total(), 'estado', actual.get_estado())
            actual = actual.siguiente 
    
    def imprimir_simulacion(self):
        print('---------Simulacion------------')
        actual = self.inicio_simulacion
        while actual is not None:
            print('nombre simul',actual.get_nombre_simulacion(), 'nombre',actual.get_nombre_producto(), 'cant_pro',actual.get_cantidad_componentes_elaborar())
            actual = actual.siguiente 
    
       