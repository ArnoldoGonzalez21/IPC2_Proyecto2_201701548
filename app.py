from ListaDoble import ListaDoble
from ListaSimple import ListaSimple
from Analizador import Analizador
from tkinter.constants import CENTER, END, LEFT, TOP, X
from tkinter.font import BOLD
import tkinter as tk
from tkinter import Frame, ttk, filedialog
import xml.etree.ElementTree as ET

class interfaz():
    lexico = Analizador()
    lineas = ListaDoble() 
    productos = ListaSimple()
    simulaciones = ListaSimple()
    
    def __init__(self):
        ventana = tk.Tk()
        fuente = 'Courier'
        self.configuracion_ventana(ventana)
        combo_productos = ttk.Combobox(ventana, font = (fuente, 11), state = "readonly")
        label_proceso_elaboracion = tk.Label(ventana, height = 18, width = 30, font = (fuente, 11), bg = 'white')
        self.tabla = ttk.Treeview(ventana)
        self.crear_toolbar(ventana, fuente, combo_productos, label_proceso_elaboracion)
        self.configuracion_widgets(ventana, fuente, label_proceso_elaboracion)   
        ventana.mainloop()
        
    def configuracion_ventana(self, ventana):
        ventana.geometry("1000x500")
        ventana.title('Digital Intelligence S. A. Simulator')   
        ventana.configure(bg = '#EAEAEA')    
         
    def crear_toolbar(self, ventana, fuente, combo_productos, label_proceso_elaboracion):
        toolbar = Frame(ventana, bg = 'white')         
        boton_archivo_maquina = tk.Button(toolbar, text = 'Archivo Máquina', command = lambda: self.leer_archivo(True, combo_productos, ventana), width = 15, height = 1, font = (fuente, 10))
        boton_archivo_simulacion = tk.Button(toolbar, text = 'Archivo Simulación', command = lambda: self.leer_archivo(False, combo_productos, ventana), width = 18, height = 1, font = (fuente, 10))
        boton_reporte = tk.Button(toolbar, text = 'Analizar', command = lambda: self.analizar_producto(ventana, label_proceso_elaboracion, combo_productos), width = 9, height = 1, font = (fuente, 10))
        boton_ayuda = tk.Button(toolbar, text = 'Reportes', command = lambda: self.crear_reporte(combo_productos), width = 9, height = 1, font = (fuente, 10))
        boton_salir = tk.Button(toolbar, text = 'Salir', command = lambda: exit(), width = 9, height = 1, font = (fuente, 10))
        boton_archivo_maquina.pack(side = LEFT, padx = 2, pady = 2)
        boton_archivo_simulacion.pack(side = LEFT, padx = 2, pady = 2)  
        boton_reporte.pack(side = LEFT, padx = 2, pady = 2)
        boton_ayuda.pack(side = LEFT, padx = 2, pady = 2)  
        boton_salir.pack(side = LEFT, padx = 2, pady = 2)
        toolbar.pack(side = TOP, fill = X)
    
    def configuracion_widgets(self, ventana, fuente, label_proceso_elaboracion): 
        label_productos = tk.Label(ventana, text = "Productos disponibles", font = (fuente, 16, BOLD), bg = '#EAEAEA')
        label_productos.place(x = 10, y = 50)
        label_componentes = tk.Label(ventana, text = "Componentes a ensamblar", font = (fuente, 14, BOLD), bg = '#EAEAEA')
        label_componentes.place(x = 30, y = 115) 
        label_proceso_elaboracion.place(x = 30, y = 150)
        label_tabla = tk.Label(ventana, text = "Tabla de resultados", font = (fuente, 14, BOLD), bg = '#EAEAEA')
        label_tabla.place(x = 500, y = 115)
        tiempo_transcurrido = tk.Label(ventana, text = "Tiempo Transcurrido:", font = (fuente, 12, BOLD), bg = '#EAEAEA')
        tiempo_transcurrido.place(x = 650, y = 450)        
    
    def configuracion_tabla(self, ventana, es_combo, nombre_combo): 
        self.tabla.delete(*self.tabla.get_children())   
        if es_combo:    
            self.tabla.configure(columns = ('#1','#2'), height = 11)
            self.tabla.column('#0',width = 180, anchor = CENTER)
            self.tabla.column('#1',width = 180, anchor = CENTER)
            self.tabla.column('#2',width = 180, anchor = CENTER)
            self.tabla.heading('#0', text = 'Tiempo (seg)', anchor = CENTER)
            self.tabla.heading('#1', text = 'Linea', anchor = CENTER)
            self.tabla.heading('#2', text = 'Componente', anchor = CENTER)                
            scrollbar = ttk.Scrollbar(ventana, orient="vertical", command = self.tabla.yview)
            scrollbar.place(x = 935, y = 150, height = 245) 
            self.tabla.configure(yscrollcommand=scrollbar.set)
             
        else:
            columns = self.simulaciones.set_columnas_tabla_simulacion(True)
            self.tabla.configure(columns=columns, height=13)
            self.tabla.column('#0',width = 180, anchor = CENTER)
            for i in range(len(columns)):
                self.tabla.column('#'+str(i+1), width = 80, anchor = CENTER)
            self.tabla.heading('#0', text = 'Tiempo (segundos)', anchor = CENTER)
            self.simulaciones.set_heading_tabla_simulacion(self.tabla, True)    
            scrollbar = ttk.Scrollbar(ventana, orient="vertical", command = self.tabla.yview)
            scrollbar.place(x = 935, y = 150, height = 245) 
            self.tabla.configure(yscrollcommand=scrollbar.set)
            
        self.lexico.elaboracion_combo(nombre_combo, self.lineas, self.tabla, END)
        self.productos.set_tiempo_total_producto(nombre_combo, self.lexico.get_tokens())  
        self.tabla.place(x = 350, y = 150)
        lbl_tiempo_total= tk.Label(ventana, text = str(self.lexico.tiempo_segundos())+' segundos', font = ('Courier', 12, BOLD), bg = '#EAEAEA')
        lbl_tiempo_total.place(x = 850, y = 450) 
    
    def crear_reporte(self, combo_producto):
        nombre_producto : str = combo_producto.get()
        nombre_producto.strip()
        self.lexico.graphviz_elaboracion(nombre_producto, self.lexico.get_tokens())
          
    def analizar_producto(self, ventana, label_proceso_elaboracion, combo_productos):
        nombre_combo : str = combo_productos.get()
        nombre_combo.strip()
        nuevo_texto = self.lexico.text_elaboracion(nombre_combo)
        label_proceso_elaboracion['text'] = nuevo_texto        
        self.configuracion_tabla(ventana, True, nombre_combo)
        
    def configuracion_combo(self, combo_productos):
        self.productos.opciones_productos_combo(combo_productos)
        combo_productos.place(x = 30, y = 85)
    
    def leer_archivo(self, estado, combo_productos, ventana):
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print(ruta)
                print('Archivo cargado con éxito')
                tree = ET.parse(f)
                root = tree.getroot()
                if estado:
                    self.analizar_maquina(root, combo_productos)
                else:
                    self.analizar_simulacion(root, ventana)
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return
        
    def analizar_maquina(self, root, combo_productos):    
        indice_elaboracion = 0
        lineas_produccion = 0
        for elem in root: 
            if elem.tag == 'CantidadLineasProduccion':
                lineas_produccion = elem.text
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
                    self.productos.insertar_producto(nombre)
                    self.lexico.analizador_estados(elaboracion, indice_elaboracion, nombre) 
                    indice_elaboracion += 1
        self.lexico.metodos_lexico(self.lineas)
        self.configuracion_combo(combo_productos)
    
    def analizar_simulacion(self, root, ventana):
        cantidad_productos_simular = 0  
        for elem in root:
            if elem.tag == 'Nombre':
                nombre_simulacion = elem.text.replace("\n","").replace("\t","")
            if elem.tag == 'ListadoProductos':
                for node in root.iter('Producto'):
                    cantidad_productos_simular += 1
                for node in root.iter('Producto'):
                    nombre_producto = node.text.replace("\n","").replace("\t","").strip()
                    self.simulaciones.insertar_simulacion(nombre_simulacion, nombre_producto, cantidad_productos_simular)    
        self.simulaciones.guardar_numero_componentes_simulacion(self.lexico.get_tokens())
        self.simulaciones.recorrer_simulacion(self.lexico.get_tokens())
        self.simulaciones.imprimir_simulacion()      
        self.configuracion_tabla(ventana, False)
    
if __name__ == '__main__':
    interfaz()

