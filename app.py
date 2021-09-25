import tkinter
from ListaDoble import ListaDoble
from ListaSimple import ListaSimple
from Analizador import Analizador
from tkinter.constants import CENTER, END, LEFT, TOP, X
from tkinter.font import BOLD
import tkinter as tk
from tkinter import Frame, ttk, filedialog, messagebox
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
        self.txt_proceso_elaboracion = tk.Text(ventana, height = 18, width = 30, font = (fuente, 11), bg = 'white')
        self.tabla = ttk.Treeview(ventana)
        self.crear_toolbar(ventana, fuente, combo_productos)
        self.configuracion_widgets(ventana, fuente)   
        ventana.mainloop()
        
    def configuracion_ventana(self, ventana):
        ventana.geometry("1000x500")
        ventana.title('Digital Intelligence S. A. Simulator')   
        ventana.configure(bg = '#EAEAEA')    
         
    def crear_toolbar(self, ventana, fuente, combo_productos):
        toolbar = Frame(ventana, bg = 'white')         
        boton_archivo_maquina = tk.Button(toolbar, text = 'Archivo Máquina', command = lambda: self.leer_archivo(True, combo_productos, ventana), width = 15, height = 1, font = (fuente, 10))
        boton_archivo_simulacion = tk.Button(toolbar, text = 'Archivo Simulación', command = lambda: self.leer_archivo(False, combo_productos, ventana), width = 18, height = 1, font = (fuente, 10))
        boton_analizar = tk.Button(toolbar, text = 'Analizar', command = lambda: self.analizar_producto(ventana, combo_productos), width = 9, height = 1, font = (fuente, 10))
        boton_reporte = tk.Button(toolbar, text = 'Reportes', command = lambda: self.crear_reporte(combo_productos), width = 9, height = 1, font = (fuente, 10))
        boton_ayuda = tk.Button(toolbar, text = 'Ayuda', command = self.ventana_ayuda, width = 9, height = 1, font = (fuente, 10))
        boton_salir = tk.Button(toolbar, text = 'Salir', command = lambda: exit(), width = 9, height = 1, font = (fuente, 10))
        boton_archivo_maquina.pack(side = LEFT, padx = 2, pady = 2)
        boton_archivo_simulacion.pack(side = LEFT, padx = 2, pady = 2)  
        boton_analizar.pack(side = LEFT, padx = 2, pady = 2)
        boton_reporte.pack(side = LEFT, padx = 2, pady = 2)
        boton_ayuda.pack(side = LEFT, padx = 2, pady = 2)  
        boton_salir.pack(side = LEFT, padx = 2, pady = 2)
        toolbar.pack(side = TOP, fill = X)
    
    def configuracion_widgets(self, ventana, fuente): 
        label_productos = tk.Label(ventana, text = "Productos disponibles", font = (fuente, 16, BOLD), bg = '#EAEAEA')
        label_productos.place(x = 10, y = 50)
        label_componentes = tk.Label(ventana, text = "Componentes a ensamblar", font = (fuente, 14, BOLD), bg = '#EAEAEA')
        label_componentes.place(x = 30, y = 115) 
        self.txt_proceso_elaboracion.place(x = 30, y = 150)
        label_tabla = tk.Label(ventana, text = "Tabla de resultados", font = (fuente, 14, BOLD), bg = '#EAEAEA')
        label_tabla.place(x = 500, y = 115)
        tiempo_transcurrido = tk.Label(ventana, text = "Tiempo Transcurrido:", font = (fuente, 12, BOLD), bg = '#EAEAEA')
        tiempo_transcurrido.place(x = 650, y = 450)        
    
    def configuracion_tabla(self, ventana, solitario, nombre_combo):        
        self.tabla.delete(*self.tabla.get_children())   
        lbl_tiempo_total = tk.Label(ventana, font = ('Courier', 12, BOLD), bg = '#EAEAEA')
        if solitario:  
            self.tabla.configure(columns = ('#1','#2'), height = 11)
            self.tabla.column('#0',width = 180, anchor = CENTER)
            self.tabla.column('#1',width = 180, anchor = CENTER)
            self.tabla.column('#2',width = 180, anchor = CENTER)
            self.tabla.heading('#0', text = 'Tiempo (seg)', anchor = CENTER)
            self.tabla.heading('#1', text = 'Linea', anchor = CENTER)
            self.tabla.heading('#2', text = 'Componente', anchor = CENTER)                
            scrollbary = ttk.Scrollbar(ventana, orient="vertical", command = self.tabla.yview)
            scrollbary.place(x = 935, y = 150, height = 245) 
            self.tabla.configure(yscrollcommand=scrollbary.set)
            self.lexico.elaboracion_combo(nombre_combo, self.lineas, self.tabla, END)
            lbl_tiempo_total.configure(text = str(self.lexico.tiempo_segundos())+' segundos')
            lbl_tiempo_total.place(x = 850, y = 450)
             
        else:
            self.tabla.destroy()
            self.tabla = ttk.Treeview(ventana)
            self.txt_proceso_elaboracion.configure(state = 'normal')
            self.txt_proceso_elaboracion.delete('1.0', END)  
            self.txt_proceso_elaboracion.configure(state = 'disabled')
            self.tabla.configure(columns = ('#1','#2','#3'), height = 11)
            self.tabla.column('#0',width = 180, anchor = CENTER)
            self.tabla.column('#1',width = 180, anchor = CENTER)
            self.tabla.column('#2',width = 100, anchor = CENTER)
            self.tabla.column('#3',width = 100, anchor = CENTER)
            self.tabla.heading('#0', text = 'Producto', anchor = CENTER)
            self.tabla.heading('#1', text = 'Tiempo (segundos)', anchor = CENTER)
            self.tabla.heading('#2', text = 'Linea', anchor = CENTER)
            self.tabla.heading('#3', text = 'Componente', anchor = CENTER)            
            scrollbary = ttk.Scrollbar(ventana, orient = "vertical", command = self.tabla.yview)
            scrollbary.place(x = 935, y = 150, height = 245) 
            self.tabla.configure(yscrollcommand=scrollbary.set)    
        
        self.tabla.place(x = 350, y = 150)
        self.lexico.imprimir_elaboracion()
    
    def configuracion_combo(self, combo_productos):
        self.productos.opciones_productos_combo(combo_productos)
        combo_productos.place(x = 30, y = 85)
        
    def crear_reporte(self, combo_producto):
        nombre_producto : str = combo_producto.get()
        nombre_producto.strip()
        self.lexico.graphviz_elaboracion(nombre_producto, self.lexico.get_tokens())
        self.escribir_archivo(nombre_producto, True)
          
    def analizar_producto(self, ventana, combo_productos):
        nombre_combo : str = combo_productos.get()
        nombre_combo.strip()
        nuevo_texto = self.lexico.text_elaboracion(nombre_combo)
        self.txt_proceso_elaboracion.insert(tk.INSERT, nuevo_texto)     
        self.txt_proceso_elaboracion.configure(state = 'disable')
        self.configuracion_tabla(ventana, True, nombre_combo)
    
    def ventana_ayuda(self):
        ventana_ayuda = tk.Tk()
        ventana_ayuda.geometry("1000x450")
        ventana_ayuda.title('Digital Intelligence S. A. Simulator - Ayuda')   
        ventana_ayuda.configure(bg = '#EAEAEA')
        boton_cerrar = tk.Button(ventana_ayuda, text = 'Cerrar Ayuda', command = lambda: ventana_ayuda.destroy(), width = 15, height = 1, font = ('Courier', 10))
        boton_cerrar.pack(side = TOP, pady = 2)
        txt_informacion = tk.Text(ventana_ayuda, width = 150, height = 30)
        txt_informacion.insert(tk.INSERT, self.informacion_ayuda())
        txt_informacion.configure(state = 'disabled')
        txt_informacion.pack()
        ventana_ayuda.mainloop()
        
    def informacion_ayuda(self):
        contenido = '''\n\tDATOS ESTUDIANTE:\n
        > Arnoldo Luis Antonio González Camey\n
        > Carné: 201701548\n
        > Introducción a la Programación y Computación 2 Sección "D"\n
        > Ingeniería en Ciencias y Sistemas\n
        > 6to Semestre\n\n
        INSTRUCCIONES:\n
        1) Cargue el archivo de máquina dando clic en el botón Archivo Máquina\n
        2) Seleccione un producto a procesar de la lista de productos cargados y presione el botón Analizar\n
        3) Si desea analizar varios productos a la vez cargue el archivo simulación en el botón Archivo Simulación\n
        4) Cree los reportes del archivo de salida y la gráfica dando clic en el botón Reportes
        '''
        return contenido
             
    def escribir_archivo(self, nombre_producto, solitario):
        if solitario:
            if nombre_producto != '':
                inicio_xml = '<SalidaSimulacion>\n'
                inicio_xml += '\t<Nombre>Maquina</Nombre>\n\t<ListadoProductos>\n'
                inicio_xml += '\t\t<Producto>\n\t\t\t<Nombre>'+nombre_producto+'</Nombre>'
                datos_salida_producto = self.lexico.return_datos_salida_solitario(nombre_producto)
                fin_xml = '\n\t</ListadoProductos>\n</SalidaSimulacion>'
                inicio_xml += datos_salida_producto + fin_xml
                miArchivo = open(nombre_producto+'.xml','w')
                miArchivo.write(inicio_xml)
                miArchivo.close()
                print('Se generó el archivo correctamente')
            else:
                messagebox.showwarning(title = 'Aviso', message = 'Elige el producto a simular')
        else:
            datos_salida_producto = self.simulaciones.datos_salida_simulacion(self.lexico.get_tokens())
            fin_xml = '\n\t</ListadoProductos>\n</SalidaSimulacion>'
            datos_salida_producto += fin_xml
            miArchivo = open('Salida_Simulacion.xml','w')
            miArchivo.write(datos_salida_producto)
            miArchivo.close()
            print('Se generó el archivo correctamente')       
    
    def leer_archivo(self, estado, combo_productos, ventana):
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
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
        for elem in root: 
            if elem.tag == 'CantidadLineasProduccion':
                lineas_produccion = elem.text
            if elem.tag == 'ListadoLineasProduccion':
                for node in root.iter('LineaProduccion'):
                    numero = node.findtext('Numero').replace("\n","").replace("\t","")
                    cantidad_componentes = node.findtext('CantidadComponentes').replace("\n","").replace("\t","")
                    tiempo_ensamblaje = node.findtext('TiempoEnsamblaje').replace("\n","").replace("\t","")
                    self.lineas.insertar_linea(numero, cantidad_componentes, tiempo_ensamblaje) 
                    
            if elem.tag == 'ListadoProductos':
                for node in root.iter('Producto'):
                    nombre = node.findtext('nombre').replace("\n","").replace("\t","")
                    elaboracion = node.findtext('elaboracion').replace("\n","").replace("\t","").strip()
                    elaboracion += ' '
                    self.productos.insertar_producto(nombre)
                    self.lexico.analizador_estados(elaboracion, indice_elaboracion, nombre) 
                    indice_elaboracion += 1
        self.lexico.metodos_lexico(self.lineas)
        self.configuracion_combo(combo_productos)
    
    def analizar_simulacion(self, root, ventana):
        for elem in root:
            if elem.tag == 'Nombre':
                nombre_simulacion = elem.text.replace("\n","").replace("\t","")
            if elem.tag == 'ListadoProductos':
                for node in root.iter('Producto'):
                    nombre_producto = node.text.replace("\n","").replace("\t","").strip()
                    self.simulaciones.insertar_simulacion(nombre_simulacion, nombre_producto) 
        self.configuracion_tabla(ventana, False, "")
        tiempo_total = self.simulaciones.recorrer_simulacion(self.lexico.get_tokens(), self.lineas, self.tabla, END)
        self.lexico.imprimir_elaboracion()
        lbl_tiempo_total = tk.Label(ventana, text = str(tiempo_total)+' segundos', font = ('Courier', 12, BOLD), bg = '#EAEAEA')
        lbl_tiempo_total.place(x = 850, y = 450)
        self.escribir_archivo(nombre_producto, False)
    
if __name__ == '__main__':
    interfaz()