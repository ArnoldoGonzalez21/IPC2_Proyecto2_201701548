from NodoEncabezado import NodoEncabezado

class ListaEncabezado():
    def __init__(self, tipo):
        self.primero: NodoEncabezado = None
        self.ultimo: NodoEncabezado = None
        self.tipo = tipo
        self.size = 0
    
    def insertar_nodoEncabezado(self, nuevo):
       #nuevo = NodoEncabezado(nuevo)
        self.size += 1
        if self.primero == None:
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            # nuevo es menor que el primero
            if int(nuevo.id) < int(self.primero.id):
                nuevo.siguiente = self.primero
                self.primero.anterior = nuevo
                self.primero = nuevo
            # nuevo es mayor que el ultimo
            elif int(nuevo.id) > int(self.ultimo.id):
                self.ultimo.siguiente = nuevo
                nuevo.anterior = self.ultimo
                self.ultimo = nuevo
            else:
                #entre el primero y el ultimo
                tmp: NodoEncabezado = self.primero 
                while tmp != None:
                    if int(nuevo.id) < int(tmp.id):
                        nuevo.siguiente = tmp
                        nuevo.anterior = tmp.anterior
                        tmp.anterior.siguiente = nuevo
                        tmp.anterior = nuevo
                        break
                    elif int(nuevo.id) > int(tmp.id):
                        tmp = tmp.siguiente
                    else:
                        break
    
    def mostrar_encabezados(self):
        tmp = self.primero
        while tmp != None:
            print('Encabezado', self.tipo, tmp.id)
            tmp = tmp.siguiente   
    
    def grafica_encabezados(self, columna_grafica):
        entro_fila = False
        entro_columna = False
        actual = self.primero
        contenido_fila = ''
        contenido_columna = ''
        contenido_fila_enlace = ''
        contenido_columna_enlace = ''
        contenido_raiz_f = ''
        
        contenido_raiz_c = ''
        if columna_grafica:
            contenido_rank = '{rank = same;raiz'
        while actual is not None:
            tmp = actual.siguiente
            if self.tipo == 'Fila':
                contenido_fila += 'F'+str(actual.id)+'[label="F'+str(actual.id)+'\",group=1,fillcolor=yellow];\n'
                if tmp is not None:
                    contenido_fila_enlace += 'F'+str(actual.id)+' -> F'+str(tmp.id)+';\n' 
                if not entro_fila:
                    contenido_raiz_f += 'raiz -> F'+str(actual.id)+';\n'
                    entro_fila = True
            elif self.tipo == 'Columna':
                contenido_columna += 'C'+str(actual.id)+'[label="C'+str(actual.id)+'\",group = '+str(int(actual.id) + 1)+',fillcolor=yellow];\n'
                if tmp is not None:
                    contenido_columna_enlace += 'C'+str(actual.id)+' -> C'+str(tmp.id)+';\n'
                if not entro_columna:
                    contenido_raiz_c += 'raiz -> C'+str(actual.id)+';\n'
                    entro_columna = True
                contenido_rank += '; C'+str(actual.id)                     
            actual = actual.siguiente
        if columna_grafica:    
            contenido_rank += '}'
            contenido = contenido_columna + contenido_columna_enlace + contenido_raiz_c + contenido_rank
        else:
            contenido = contenido_fila + contenido_fila_enlace + contenido_raiz_f
        print(contenido)
        return contenido
    
    def get_encabezado(self, id): #buscar el encabezado
        tmp = self.primero
        while tmp != None:
            if id == tmp.id:
                return tmp
            tmp = tmp.siguiente
        return None                
    