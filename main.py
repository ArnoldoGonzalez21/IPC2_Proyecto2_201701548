#import tkinter as tk
#from tkinter import ttk


import tkinter as tk
from tkinter import font, ttk

def recuperar():
    fuen = opcion.get()
    print(fuen)
    labelTop.configure(text=fuen, font=fuen)
valores = []
app = tk.Tk()
for font in font.families():
    valores.append(font)
app.geometry('300x300')

opcion=tk.StringVar()
comboExample = ttk.Combobox(app, textvariable=opcion)
comboExample['values'] = valores
comboExample.grid(column=0, row=1)
comboExample.current(0)
fuente = comboExample.get()
labelTop = tk.Label(app, text = fuente, font = fuente)
labelTop.grid(column=0, row=0)
boton1=tk.Button(app, text="Recuperar",command=recuperar)
boton1.grid(column=1, row=3)


app.mainloop()






"""
COLOCAR LAS POSICIONES EN EL COMBOBOX
import tkinter as tk
from tkinter import font, ttk

valores = []
app = tk.Tk()
for font in font.families():
    valores.append(font)
    #print(font)

#app = tk.Tk() 
app.geometry('300x300')

#labelTop = tk.Label(app, text = "Choose your favourite month")
#labelTop.grid(column=0, row=0)

comboExample = ttk.Combobox(app)
comboExample['values'] = valores
#print(dict(comboExample)) 
comboExample.grid(column=0, row=1)
comboExample.current(1)

#print(comboExample.current(), comboExample.get())

app.mainloop()
"""

