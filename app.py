from ListaDoble import ListaDoble
from ListaSimple import ListaSimple
from Analizador import Analizador
from Simulacion import Simulacion
from tkinter.constants import LEFT, TOP, X
from tkinter.font import BOLD
import tkinter as tk
from tkinter import Frame, ttk, filedialog
import xml.etree.ElementTree as ET
from os import startfile, system

class interfaz():
    lexico = Analizador()
    lineas = ListaDoble() 
    productos = ListaSimple()
    simulaciones = ListaSimple()
    def __init__(self):
        ventana = tk.Tk()
        fuente = 'Courier'
        self.configuracion_ventana(ventana)
        self.crear_toolbar(ventana, fuente)
        self.configuracion_widgets(ventana, fuente)   
        # ttk.Treeview crear la tabla https://programmerclick.com/article/5625227255/
        ventana.mainloop()
        
    def configuracion_ventana(self, ventana):
        ventana.geometry("1000x500")
        ventana.title('Digital Intelligence S. A. Simulator')   
        ventana.configure(bg = '#EAEAEA')    
        
    def leer_archivo(self, estado):
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print(ruta)
                print('Archivo cargado con éxito')
                tree = ET.parse(f)
                root = tree.getroot()
                if estado:
                    self.analizar_maquina(root)
                else:
                    self.analizar_simulacion(root)
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return
        
    def analizar_maquina(self, root):    
        indice_elaboracion = 0
        lineas_produccion = 0
        for elem in root: #con la cantidadlineasprod se puede saber cuantas hay que meter y con un contador detenerse
            #print(elem.tag, elem.attrib)  
            if elem.tag == 'CantidadLineasProduccion':
                lineas_produccion = elem.text
                #print(lineas_produccion)
            if elem.tag == 'ListadoLineasProduccion':
                for node in root.iter('LineaProduccion'):
                    numero = node.findtext('Numero').replace("\n","").replace("\t","")
                    cantidad_componentes = node.findtext('CantidadComponentes').replace("\n","").replace("\t","")
                    tiempo_ensamblaje = node.findtext('TiempoEnsamblaje').replace("\n","").replace("\t","")
                    self.lineas.insertar_linea(numero, cantidad_componentes, tiempo_ensamblaje, 0) 
                    
            if elem.tag == 'ListadoProductos':
                for node in root.iter('Producto'):
                    nombre = node.findtext('nombre').replace("\n","").replace("\t","")
                    elaboracion = node.findtext('elaboracion')
                    self.productos.insertar_producto(nombre, 0, 0, indice_elaboracion)
                    self.lexico.analizador_estados(elaboracion, indice_elaboracion, nombre) 
                    indice_elaboracion += 1
        #self.lineas.imprimir_linea()       
        self.lexico.tamano(self.lineas)
        #self.productos.imprimir_producto()
    
    def analizar_simulacion(self, root):  
        for elem in root:
            if elem.tag == 'Nombre':
                nombre_simulacion = elem.text
            if elem.tag == 'ListadoProductos':
                for node in root.iter('Producto'):
                    nombre_producto = node.text
                    self.simulaciones.insertar_simulacion(nombre_simulacion, nombre_producto)
        self.simulaciones.imprimir_simulacion()
                    
    def crear_toolbar(self, ventana, fuente):
        toolbar = Frame(ventana, bg = 'white')         
        boton_archivo_maquina = tk.Button(toolbar, text = 'Archivo Máquina', width = 15, height = 1, font = (fuente, 10), command = lambda: self.leer_archivo(True) )
        boton_archivo_simulacion = tk.Button(toolbar, text = 'Archivo Simulación', width = 18, height = 1, font = (fuente, 10), command = lambda: self.leer_archivo(False) )
        boton_reporte = tk.Button(toolbar, text = 'Analizar', width = 9, height = 1, font = (fuente, 10))
        boton_ayuda = tk.Button(toolbar, text = 'Reportes', width = 9, height = 1, font = (fuente, 10))
        boton_archivo_maquina.pack(side = LEFT, padx=2, pady= 2)
        boton_archivo_simulacion.pack(side = LEFT, padx=2, pady= 2)  
        boton_reporte.pack(side = LEFT, padx=2, pady= 2)
        boton_ayuda.pack(side = LEFT, padx=2, pady= 2)  
        toolbar.pack(side = TOP, fill = X)
    
    def configuracion_widgets(self, ventana, fuente): #https://www.delftstack.com/es/tutorial/tkinter-tutorial/tkinter-combobox/
        label_productos = tk.Label(ventana, text = "Productos disponibles", font = (fuente, 16, BOLD), bg = '#EAEAEA')
        label_productos.place(x = 10, y = 50)
        combo_productos = ttk.Combobox(ventana, font = (fuente, 11), state = "readonly",values=[
                                    "January", 
                                    "February",
                                    "March",
                                    "April"])
        combo_productos.place(x = 30, y = 85)
        combo_productos.current(0) # obtener el indice del producto seleccionado luego con get obtener el elemento
        
        label_componentes = tk.Label(ventana, text = "Componentes a ensamblar", font = (fuente, 14, BOLD), bg = '#EAEAEA')
        label_componentes.place(x = 30, y = 115)        
        txtfield_componenetes = tk.Text(ventana, height = 10, width = 20, font = (fuente, 18), bg = 'white')
        txtfield_componenetes.configure(state = 'disabled')
        txtfield_componenetes.place(x = 30, y = 150)
        label_tabla = tk.Label(ventana, text = "Tabla de resultados", font = (fuente, 14, BOLD), bg = '#EAEAEA')
        label_tabla.place(x = 575, y = 115)
        tiempo_transcurrido = tk.Label(ventana, text = "Tiempo Transcurrido", font = (fuente, 12, BOLD), bg = '#EAEAEA')
        tiempo_transcurrido.place(x = 700, y = 450)        

if __name__ == '__main__':
    interfaz()

