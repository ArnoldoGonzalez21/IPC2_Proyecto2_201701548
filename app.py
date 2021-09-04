from tkinter.constants import LEFT, TOP, X
from tkinter.font import BOLD
import tkinter as tk
from tkinter import Frame, ttk, filedialog
import xml.etree.ElementTree as ET
#from os import startfile, system
#lineas = ListaSimple() 

class interfaz():
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
        
    def leer_archivo(self): #pedir True or False / 0 ó 1 para saber si es un archivo maquina o simulación --> command = lambda: leer_archivo("1")
        try:
            ruta = filedialog.askopenfilename(title = "Abrir un archivo")
            with open(ruta, 'rt', encoding = 'utf-8') as f:
                print(ruta)
                print('Archivo cargado con éxito')
                tree = ET.parse(f)
                root = tree.getroot()
        except OSError:
            print("<<< No se pudo leer el Archivo", ruta ,'>>>')
            return
        """    
        contador = 0
        for elem in root:      
            nombre = elem.get('nombre') #nombre del terreno
            dim_x = elem.findtext('dimension/m') #dimension x del terreno
            dim_y = elem.findtext('dimension/n') #dimension y del terreno                  
            inicio_x = elem.findtext('posicioninicio/x') #incio x 
            inicio_y = elem.findtext('posicioninicio/y') #incio y 
            final_x = elem.findtext('posicionfin/x') #fin x 
            final_y = elem.findtext('posicionfin/y') #fin y         
            #lineas.insertar_terrenos(contador,nombre,dim_x,dim_y,inicio_x,inicio_y,final_x,final_y)
            contador += 1
        
        contador_id = 1
        contador_pos = -1
        for node in root.iter('posicion'):        
            posx = node.attrib.get('x')
            posy = node.attrib.get('y')
            valor = node.text
            contador_id += 1
            if int(posx) == 1 and int(posy) == 1:
                contador_pos +=1
                contador_id = 1
            #posiciones.insertar(contador_pos, contador_id, posx, posy, valor, False)    """      
     
    def crear_toolbar(self, ventana, fuente):
        toolbar = Frame(ventana, bg = 'white')         
        boton_archivo_maquina = tk.Button(toolbar, text = 'Archivo Máquina', width = 15, height = 1, font = (fuente, 10), command = self.leer_archivo )
        boton_archivo_simulacion = tk.Button(toolbar, text = 'Archivo Simulación', width = 18, height = 1, font = (fuente, 10), command = self.leer_archivo )
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

