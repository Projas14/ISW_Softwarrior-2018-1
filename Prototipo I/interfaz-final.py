# -*- coding: cp1252 -*-
#|--------------------------------------------------|
#|                  LIBRERIAS                       |
#|--------------------------------------------------|
from tkinter import *
from tkinter import messagebox
import time
import fix_yahoo_finance as yf

import quandl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
from decimal import *

#|--------------------------------------------------|
#|                  FUNCIONES                       |
#|--------------------------------------------------|
def prom(list):
   suma = 0
   for i in list:
      suma += i
   return (suma/len(list))

def sigma(s):
   cteT = sqrt(1/252)
   return(round(s/cteT,6))

def functionS(data):
   list = []
   
   i = 0
   for x in data:
      if i == 0:
         list.append(0)
      else:
         list.append(log(data[i]/data[i-1]))
      i += 1
         
   sumatoria = 0
   promedio = prom(list)

   for i in list:
      sumatoria += (i-promedio)**2

   return((1/(len(list)-1))*sumatoria)


def procesar():
    aapl = yf.download(Codigo.get(), start=Fecha_Inicio.get(), end=Fecha_Final.get())
    aapl.to_csv('fb_ohlc.csv')
    limpieza = (str(aapl).split("\n"))
    DataFinal = []
    for linea in limpieza[1:]:
        datos = linea.split()
        if len(datos) > 5:
            DataFinal.append([datos[0],datos[4]])

    if len(DataFinal) == 0:
        messagebox.showwarning("Advertencia","Informacion invalida vuelva a intentar")
        return
    else:
        messagebox.showinfo("Ok","Datos Listos y almacenados")
    test = aapl['Close'][-60:-1]
    test2 = aapl['Close'][-120:-60]
    if Time_maduracion.get() > 3:
        print (test,test2)
        volatividad = sigma(functionS(test)+functionS(test2))
        messagebox.showinfo("ok","La Volatividad es de:  "+ str(volatividad))
        etiqueta_Volatividad = Label(ventana, text='La Volatividad es de:  '+str(volatividad))
        etiqueta_Volatividad.grid(row=15, column=3)
        
    else:
        print (test)
        volatividad =sigma(functionS(test))
        messagebox.showinfo("ok","la Volatividad es de: "+ str(volatividad))
        etiqueta_Volatividad = Label(ventana, text='La Volatividad es de:  '+str(volatividad))
        etiqueta_Volatividad.grid(row=15, column=3)
    
        
    
#def guardar(data):
#   archivo = open(str(Codigo.get())+".txt", "w")
#    archivo.write(str(data))
#    archivo.close()
#    return ("Guardado")
	
#|--------------------------------------------------|
#|             Instancia de la clase Tk             |
#|--------------------------------------------------|

ventana = Tk()
ventana.title('Valoración de Opciones sobre Acciones')

#|--------------------------------------------------|
#|                  VARIABLES                       |
#|--------------------------------------------------|
Codigo = StringVar()
Fecha_Inicio = StringVar()
Fecha_Final = StringVar()
Tasa_interes = IntVar()
actividad = StringVar()
Time_maduracion = IntVar()
Precio_ejecucion = IntVar()
Volatividad = IntVar()
#inicio
actividad.set("Americana")
Fecha_Inicio.set(str(time.strftime("20%y-%m-%d")))
Fecha_Final.set(str(time.strftime("20%y-%m-%d")))

#|--------------------------------------------------|
#|              Generación de widgets               | 
#|--------------------------------------------------|

#Codigo
etiqueta_Codigo = Label(ventana, text='Codigo:')
entrada_Codigo = Entry(ventana, textvariable=Codigo)
etiqueta_Codigo.grid(row=1, column=1)
entrada_Codigo.grid(row=1, column=2)


#Fecha Inicio
etiqueta_Fecha_Inicio = Label(ventana, text='Fecha Inicio: ')
entrada_Fecha_Inicio = Entry(ventana, textvariable=Fecha_Inicio)
etiqueta_Fecha_Inicio.grid(row=4, column=1)
entrada_Fecha_Inicio.grid(row=4, column=2)

#Fecha Final
etiqueta_Fecha_Final = Label(ventana, text='Fecha Final: ')
entrada_Fecha_Final = Entry(ventana, textvariable=Fecha_Final)
etiqueta_Fecha_Final.grid(row=4, column=4)
entrada_Fecha_Final.grid(row=4, column=5)

#Tasa interes
etiqueta_Tasa_interes = Label(ventana, text='Tasa interes: ')
entrada_Tasa_interes = Entry(ventana, textvariable=Tasa_interes)
etiqueta_Tasa_interes.grid(row=6, column=1)
entrada_Tasa_interes.grid(row=6, column=2)

#Tiempo de maduracion 
etiqueta_Time_maduracion = Label(ventana, text='Tiempo de maduracion: ')
entrada_Time_maduracion = Entry(ventana, textvariable=Time_maduracion)
etiqueta_Time_maduracion.grid(row=6, column=4)
entrada_Time_maduracion.grid(row=6, column=5)

#Precio de ejecucion  
etiqueta_Precio_ejecucion = Label(ventana, text='Precio de ejecucion : ')
entrada_Precio_ejecucion = Entry(ventana, textvariable=Precio_ejecucion)
etiqueta_Precio_ejecucion.grid(row=10, column=1)
entrada_Precio_ejecucion.grid(row=10, column=2)

#OPCIONES
etiqueta_actividad = Label(ventana, text='OPCIONES: ')
entrada_actividad = OptionMenu(ventana, actividad, "Americana", "Europea", "Monte-Carlos")
etiqueta_actividad.grid(row=10, column=4)
entrada_actividad.grid(row=10, column=5)

#boton
boton = Button(ventana, text='Procesar',font=('Governor',10),background='#01a8a6',foreground='White',command=procesar)
boton.grid(row=12, column=3)

#ejecución de ventana
ventana.mainloop()
