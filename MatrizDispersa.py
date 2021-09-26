from NodoEncabezado import NodoEncabezado
from ListaEncabezado import ListaEncabezado
from NodoInterno import NodoInterno
from os import system, startfile

class MatrizDispersa():
    
    def __init__(self, capa): #capa -----> para que puede ser de mas de una dimension aumenta la capa                          
        self.filas = ListaEncabezado('Fila')
        self.columnas = ListaEncabezado('Columna')
        self.capa = capa
        
    def insert(self, pos_x, pos_y, tiempo):
        nuevo = NodoInterno(pos_x, pos_y, tiempo) 
        # --- lo primero sera buscar si ya existen los encabezados en la matriz
        nodo_X = self.filas.get_encabezado(pos_x)
        nodo_Y = self.columnas.get_encabezado(pos_y)

        if nodo_X == None: # --- comprobamos que el encabezado fila pos_x exista
             # --- si nodo_X es nulo, quiere decir que no existe encabezado fila pos_x
            nodo_X = NodoEncabezado(pos_x)
            self.filas.insertar_nodoEncabezado(nodo_X)

        if nodo_Y == None: # --- comprobamos que el encabezado columna pos_y exista
            # --- si nodo_Y es nulo, quiere decir que no existe encabezado columna pos_y
            nodo_Y = NodoEncabezado(pos_y)
            self.columnas.insertar_nodoEncabezado(nodo_Y)

        # ----- INSERTAR NUEVO EN FILA
        if nodo_X.acceso == None: # -- comprobamos que el nodo_x no esta apuntando hacia ningun nodoInterno
            nodo_X.acceso = nuevo
        else: # -- si esta apuntando, validamos si la posicion de la columna del NUEVO nodoInterno es menor a la posicion de la columna del acceso 
            if int(nuevo.coordenadaY) < int(nodo_X.acceso.coordenadaY): 
                nuevo.derecha = nodo_X.acceso              
                nodo_X.acceso.izquierda = nuevo
                nodo_X.acceso = nuevo
            else:
                #de no cumplirse debemos movernos de izquierda a derecha buscando donde posicionar el NUEVO nodoInterno
                tmp : NodoInterno = nodo_X.acceso    
                while tmp != None:                     
                    if int(nuevo.coordenadaY) < int(tmp.coordenadaY):
                        nuevo.derecha = tmp
                        nuevo.izquierda = tmp.izquierda
                        tmp.izquierda.derecha = nuevo
                        tmp.izquierda = nuevo
                        break
                    elif nuevo.coordenadaX == tmp.coordenadaX and nuevo.coordenadaY == tmp.coordenadaY: #validamos que no haya repetidas
                        break
                    else:
                        if tmp.derecha == None:
                            tmp.derecha = nuevo
                            nuevo.izquierda = tmp
                            break
                        else:
                            tmp = tmp.derecha 

        # ----- INSERTAR NUEVO EN COLUMNA
        if nodo_Y.acceso == None:  # -- comprobamos que el nodo_y no esta apuntando hacia ningun nodoCelda
            nodo_Y.acceso = nuevo
        else: # -- si esta apuntando, validamos si la posicion de la fila del NUEVO nodoCelda es menor a la posicion de la fila del acceso 
            if int(nuevo.coordenadaX) < int(nodo_Y.acceso.coordenadaX):
                nuevo.abajo = nodo_Y.acceso
                nodo_Y.acceso.arriba = nuevo
                nodo_Y.acceso = nuevo
            else:
                # de no cumplirse, debemos movernos de arriba hacia abajo buscando donde posicionar el NUEVO
                tmp2 : NodoInterno = nodo_Y.acceso
                while tmp2 != None:
                    if int(nuevo.coordenadaX) < int(tmp2.coordenadaX):
                        nuevo.abajo = tmp2
                        nuevo.arriba = tmp2.arriba
                        tmp2.arriba.abajo = nuevo
                        tmp2.arriba = nuevo
                        break
                    elif nuevo.coordenadaX == tmp2.coordenadaX and nuevo.coordenadaY == tmp2.coordenadaY: #validamos que no haya repetidas
                        break
                    else:
                        if tmp2.abajo == None:
                            tmp2.abajo = nuevo
                            nuevo.arriba = tmp2
                            break
                        else:
                            tmp2 = tmp2.abajo
    
    def recorrer_matriz_simulacion(self):
        pivote = self.filas.primero
        while pivote is not None:
            pivote_celda : NodoInterno = pivote.acceso
            while pivote_celda is not None:
                pivote_celda = pivote_celda.derecha
                
            pivote = pivote.siguiente
    
    def enlazar_nodos(self):
        pivote = self.filas.primero
        contenido_nodos = ''
        contenido_enlace_fila = ''
        contenido_enlace_columna = ''
        contenido_rank = ''
        while pivote is not None:
            entro_primera_fila = False
            pivote_celda : NodoInterno = pivote.acceso
            contenido_enlace_fila += '\t\tF'+str(pivote.id)+' -> '
            contenido_rank += '\t\t{rank=same;F'+str(pivote.id)
            while pivote_celda is not None:
                tmp_pivote_celda = pivote_celda.izquierda
                
                contenido_nodos += '\n\t\tnodo'+str(pivote_celda.coordenadaX)+'_'+str(pivote_celda.coordenadaY)
                contenido_nodos += '[label="'+str(pivote_celda.tiempo)+'",fillcolor = green, group = '+str(int(pivote_celda.coordenadaY) + 1)+']\n'
                
                if pivote.id == pivote_celda.coordenadaX:
                    contenido_rank += ';nodo'+str(pivote_celda.coordenadaX)+'_'+str(pivote_celda.coordenadaY)
                    if not entro_primera_fila:
                        contenido_enlace_fila += 'nodo'+str(pivote_celda.coordenadaX)+'_'+str(pivote_celda.coordenadaY)+';\n'
                        entro_primera_fila = True
                    else:
                        if tmp_pivote_celda is not None:
                            contenido_enlace_fila += '\t\tnodo'+str(tmp_pivote_celda.coordenadaX)+'_'+str(tmp_pivote_celda.coordenadaY)+' -> ' + 'nodo'+str(pivote_celda.coordenadaX)+'_'+str(pivote_celda.coordenadaY)+';\n'                            

                pivote_celda = pivote_celda.derecha
            contenido_rank += '}\n'
            pivote = pivote.siguiente
        
        pivote = self.columnas.primero
        while pivote is not None:
            entro_primera_columna = False
            pivote_celda : NodoInterno = pivote.acceso
            contenido_enlace_columna += '\t\tC'+str(pivote.id)+' -> '
            while pivote_celda is not None:
                tmp_pivote_celda = pivote_celda.arriba
                 
                if pivote.id == pivote_celda.coordenadaY:
                    if not entro_primera_columna:
                        contenido_enlace_columna += 'nodo'+str(pivote_celda.coordenadaX)+'_'+str(pivote_celda.coordenadaY)+';\n'
                        entro_primera_columna = True
                    else:
                        if tmp_pivote_celda is not None:
                            contenido_enlace_columna += '\t\tnodo'+str(tmp_pivote_celda.coordenadaX)+'_'+str(tmp_pivote_celda.coordenadaY)+' -> ' + 'nodo'+str(pivote_celda.coordenadaX)+'_'+str(pivote_celda.coordenadaY)+';\n'                        

                pivote_celda = pivote_celda.abajo
            pivote = pivote.siguiente
        
        contenido_nodos += contenido_enlace_fila + contenido_rank + contenido_enlace_columna
        return contenido_nodos
    
    def generarGraphviz(self):
        nombre = 'Matriz Dispersa'
        inicio_graphviz = '''
        \rdigraph L{
        \r\tnode[shape = circle fillcolor="white" style = filled]
        \r\tsubgraph cluster_p{
        \r\t\tlabel = \"'''+nombre+''' \"
        \r\t\tbgcolor = "#398D9C"
        \r\t\traiz[label = "0,0"]
        \r\t\tedge[dir = "both"]
    '''
        encabezados = self.filas.grafica_encabezados(False)
        encabezados += self.columnas.grafica_encabezados(True)
        
        nodos = self.enlazar_nodos()
        
        final_graphviz = '\n\t}\n}'
        graphviz = inicio_graphviz + encabezados + nodos + final_graphviz
        print('<<<<< Generando imagen >>>>>')
        #print(graphviz)
        miArchivo= open('graphviz_matriz.dot','w')
        miArchivo.write(graphviz)
        miArchivo.close()
        system('dot -Tpng graphviz_matriz.dot -o graphviz_matriz.png')
        system('cd ./graphviz_matriz.png')
        #startfile('graphviz_matriz.png')