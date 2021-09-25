from Producto import Producto
from Token import Token
from Trabajo import Trabajo
from Simulacion import Simulacion
from MatrizDispersa import MatrizDispersa
from os import system, startfile

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
    
    def insertar_simulacion(self, nombre_simulacion, nombre_producto):
        nuevo = Simulacion(nombre_simulacion, nombre_producto)
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
                self.insertar_elaboracion(numero_linea, numero_componente, 0, indice_elaboracion, nombre_producto)
                break
            if actual.get_lexema() == 'L':
                numero_linea = tmp.get_lexema()
                indice_elaboracion = actual.get_indice_elaboracion()
                nombre_producto = actual.get_nombre_producto()
            if actual.get_lexema() == 'C':
                numero_componente = tmp.get_lexema()
            if actual.get_lexema() == '':   
                self.insertar_elaboracion(numero_linea, numero_componente, 0, indice_elaboracion, nombre_producto)
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
    
    def set_tiempo_total_producto(self, nombre_producto, tiempo_total):
        actual = self.inicio_producto
        while actual is not None:
            if nombre_producto == actual.get_nombre():
                actual.set_tiempo_total(tiempo_total)
                return
            actual = actual.siguiente
        self.imprimir_producto()    
    
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
    
    def recorrer_elaboracion_tabla(self, nombre_producto, lineas, tabla, END, solitario): 
        global tiempo_segundos
        ultimo_componente = 0
        linea_mayor = 0
        movimiento_entre_componentes = 0
        if solitario:
            tiempo_segundos = 0
            lineas.reinciar_lineas()
            
        actual = self.inicio_elaboracion
        while actual is not None:
            if solitario:
                actual.set_contador_posicion(0)
                actual.set_tiempo_total(0)
                actual.set_estado(0)
            if actual.get_nombre_producto() == nombre_producto:
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
                    lineas.guardar_cantidad_mov(int(actual.get_numero_linea()), movimiento_entre_componentes)
                    tiempo_segundos += movimiento_entre_componentes  
                lineas.guardar_ultima_posicion_linea(int(actual.get_numero_linea()), int(actual.get_numero_componente()))
                tiempo_segundos += int(actual.get_tiempo())
                actual.set_tiempo_total(tiempo_segundos)
                if solitario:
                    tabla.insert('',END, text = '\t      '+str(tiempo_segundos), values=(actual.get_numero_linea(),actual.get_numero_componente()))  
                else:
                    tabla.insert('',END, text = nombre_producto, values=(tiempo_segundos,actual.get_numero_linea(),actual.get_numero_componente()))  
            actual = actual.siguiente
        
        tiempo_segundos += linea_mayor
        print(tiempo_segundos, 'tiempo segundos global')             
        
    def recorrer_simulacion(self, tokens, lineas, tabla, END):
        global tiempo_segundos
        tiempo_segundos = 0
        actual = tokens.inicio_elaboracion
        lineas.reinciar_lineas()
        while actual is not None:
            actual.set_contador_posicion(0)
            actual.set_tiempo_total(0)
            actual.set_estado(0)
            actual = actual.siguiente
            
        actual = self.inicio_simulacion
        while actual is not None:
            nombre_producto = actual.get_nombre_producto()
            tokens.recorrer_elaboracion_tabla(nombre_producto, lineas, tabla, END, False)
            actual = actual.siguiente
        return tiempo_segundos       
        
    def colocar_tiempo(self, lineas):
        actual = self.inicio_elaboracion
        while actual is not None:
            numero_linea = actual.get_numero_linea()
            tiempo_ensamblaje = lineas.get_tiempo(numero_linea)
            actual.set_tiempo(tiempo_ensamblaje)
            actual = actual.siguiente
    
    def proceso_elaboracion_txt(self, nombre_producto):
        actual = self.inicio_elaboracion
        contenido = '\n'
        while actual is not None:
            if nombre_producto == actual.get_nombre_producto():
                contenido += '  Línea '+str(actual.get_numero_linea())+ ' - Componente '+str(actual.get_numero_componente())+'\n'
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
    
    def datos_salida_simulacion(self, tokens):
        titulo = False
        actual = self.inicio_simulacion
        contenido = '<SalidaSimulacion>\n'
        while actual is not None:
            if not titulo:
                contenido += '\t<Nombre>'+actual.get_nombre_simulacion()+'</Nombre>\n\t<ListadoProductos>'
                titulo = True
            contenido += '\n\t\t<Producto>\n\t\t\t<Nombre>'+actual.get_nombre_producto()+'</Nombre>'
            contenido += tokens.datos_salida_solitario(actual.get_nombre_producto())
            actual = actual.siguiente
        return contenido  
    
    def datos_salida_solitario(self, nombre_producto):
        global tiempo_segundos
        actual = self.inicio_elaboracion
        contenido = '\n\t\t\t<TiempoTotal>'+str(tiempo_segundos)+'</TiempoTotal>\n\t\t\t<ElaboracionOptima>'
        while actual is not None:
            if actual.get_nombre_producto() == nombre_producto:
                contenido += '\n\t\t\t\t<Tiempo NoSegundo = "'+str(actual.get_tiempo_total())+'">'
                contenido += '\n\t\t\t\t\t<LineaEnsamblaje NoLinea = "'+str(actual.get_numero_linea())+'">\n\t\t\t\t\t\tEnsamblando\n\t\t\t\t\t</LineaEnsamblaje>\n\t\t\t\t</Tiempo>'
            actual = actual.siguiente
        contenido += '\n\t\t\t</ElaboracionOptima>\n\t\t</Producto>'
        return contenido
            
    def imprimir_tokens(self):
        print('--------------Tokens--------------------')
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
            print('L',actual.get_numero_linea(), 'C',actual.get_numero_componente(), 'tiempo',actual.get_tiempo(), 'nombre',actual.get_nombre_producto(), 'tiempo_total', actual.get_tiempo_total(), 'pos',actual.get_contador_posicion(),'estado', actual.get_estado())
            actual = actual.siguiente 
    
    def imprimir_simulacion(self):
        print('---------Simulacion------------')
        actual = self.inicio_simulacion
        while actual is not None:
            print('nombre simul',actual.get_nombre_simulacion(), 'nombre',actual.get_nombre_producto())
            actual = actual.siguiente 