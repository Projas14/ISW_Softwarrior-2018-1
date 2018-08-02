from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import  Style
from tkinter import messagebox
import time
import fix_yahoo_finance as yf
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog

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

#funciones OFFLINE
def abrir():
   filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("all files","*."),("all files","*.*")))
   Archivo.set(str(filename))
   print(Archivo.get())
#funciones de procesamiento
def invertir_fecha(fecha):
    fecha = fecha.split("-")
    fechaNueva = str(fecha[2])+"-"+str(fecha[1])+"-"+str(fecha[0])
    return fechaNueva

def procesar():
	aapl = yf.download(Codigo.get(), start=invertir_fecha(Fecha_Inicio.get()), end=invertir_fecha(Fecha_Final.get()))
	print (aapl)
	aapl.to_csv('cache/fb_ohlc.csv')
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

def procesar2():
	import csv
	with open(Archivo.get(), newline='') as File:  
		reader = csv.reader(File)
		contador = 0
		DataFinal = []
		for row in reader:
			if contador != 0:
				print(row[4])

				DataFinal.append(float(row[4]))
			contador = contador + 1
	if Time_maduracion.get() > 3:
		volatividad = sigma(functionS(DataFinal))
		messagebox.showinfo("ok","La Volatividad es de:  "+ str(volatividad))
		etiqueta_Volatividad = Label(ventana, text='La Volatividad es de:  '+str(volatividad))
		etiqueta_Volatividad.grid(row=15, column=3)
	else:
		print (DataFinal)
		volatividad =sigma(functionS(DataFinal))
		messagebox.showinfo("ok","la Volatividad es de: "+ str(volatividad))
		etiqueta_Volatividad = Label(ventana, text='La Volatividad es de:  '+str(volatividad))
		etiqueta_Volatividad.grid(row=15, column=3)
    
def guardar(data):
    archivo = open("cache/" + str(Codigo.get())+".txt", "w")
    archivo.write(str(data))
    archivo.close()
    return ("Guardado")


#ventana
ventana = Tk()
colorFondo = "#00a1f2"
colorLetra = "#000"
s = Style()
s2 = Style()
s.configure('My.TFrame',background=colorFondo,foreground=colorLetra)
s2.configure('My.TFrame2',background="#000",foreground=colorLetra)

ventana.title('Valoración de Opciones sobre Acciones')
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand='yes')
ventana.geometry("754x480+0+0")

#pestaña 0
pes0 = ttk.Frame(notebook)
notebook.add(pes0,text="INICIO")
#bienvenidos
BV = PhotoImage(file="img/bienvenidos.png")
etiqueta1= Label(pes0, image=BV,fg="#000",bg="#000").place(x=0,y=0)
etiqueta2 = Label(pes0, text="Beatriz Segura - Paul Rojas - Gabriela Sepulvedad",fg=colorLetra,bg="#00a1f2").place(x=260,y=400)


#pestaña 1
pes1 = ttk.Frame(notebook,style='My.TFrame')
notebook.add(pes1,text="ONLINE")
#variables pestaña 1
Codigo = StringVar()
Fecha_Inicio = StringVar()
Fecha_Final = StringVar()
Tasa_interes = IntVar()
Fecha_Inicio.set(str(time.strftime("20%y-%m-%d")))
Fecha_Final.set(str(time.strftime("20%y-%m-%d")))
Time_maduracion = IntVar()
Precio_ejecucion = IntVar()
Volatividad = IntVar()

#generación de widgets
#logo
Banner1 = PhotoImage(file="img/bienvenidos2.png")
lblBanner1 = Label(pes1,image=Banner1,bg=colorFondo).place(x=0,y=0)
#Codigo
etiqueta_Codigo = Label(pes1, text='Codigo:',fg=colorLetra,bg=colorFondo).place(x=150,y=130)
entrada_Codigo = Entry(pes1, textvariable=Codigo,width=15).place(x=300,y=130)



#Fecha Inicio
etiqueta_Fecha_Inicio = Label(pes1, text='Fecha Inicio: ',fg=colorLetra,bg=colorFondo).place(x=150,y=180)
entrada_Fecha_Inicio = DateEntry(pes1, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Inicio).place(x=300,y=180)




#Fecha Final
etiqueta_Fecha_Final = Label(pes1, text='Fecha Final: ',fg=colorLetra,bg=colorFondo).place(x=420,y=180)
entrada_Fecha_Final = DateEntry(pes1, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Final).place(x=500,y=180)



#Tasa interes
etiqueta_Tasa_interes = Label(pes1, text='Tasa interes: ',fg=colorLetra,bg=colorFondo).place(x=150,y=330)
entrada_Tasa_interes = Entry(pes1, textvariable=Tasa_interes,width=15).place(x=300,y=330)


#Tiempo de maduracion 
etiqueta_Time_maduracion = Label(pes1, text='Tiempo de maduracion: ',fg=colorLetra,bg=colorFondo).place(x=150,y=230)
entrada_Time_maduracion = Entry(pes1, textvariable=Time_maduracion,width=15).place(x=300,y=230)


#Precio de ejecucion  
etiqueta_Precio_ejecucion = Label(pes1, text='Precio de ejecucion : ',font=('Governor',10),fg=colorLetra,bg=colorFondo).place(x=150,y=280)
entrada_Precio_ejecucion = Entry(pes1, textvariable=Precio_ejecucion,width=15).place(x=300,y=280)

#boton
boton = Button(pes1, text='Procesar', command=procesar, width=15, bg=colorFondo).place(x=300,y=380)


#pestaña 2
pes2 = ttk.Frame(notebook,style='My.TFrame')
notebook.add(pes2,text="OFFLINE")
#variables pestaña 2
Archivo = StringVar()
Fecha_Inicio = StringVar()
Fecha_Final = StringVar()
Tasa_interes = IntVar()
Fecha_Inicio.set(str(time.strftime("20%y-%m-%d")))
Fecha_Final.set(str(time.strftime("20%y-%m-%d")))
Time_maduracion = IntVar()
Precio_ejecucion = IntVar()
Volatividad = IntVar()

#generación de widgets
#logo
Banner2 = PhotoImage(file="img/bienvenidos2.png")
lblBanner2 = Label(pes2,image=Banner2,bg=colorFondo).place(x=0,y=0)
#Codigo
etiqueta_Archivo = Label(pes2, text='Archivo:',fg=colorLetra,bg=colorFondo).place(x=150,y=130)
Etiqueta_Archivo = Entry(pes2, textvariable=Archivo,width=15).place(x=220,y=130)
entrada_Codigo = Button(pes2,text="Seleccionar archivo", command=abrir).place(x=320,y=130)



#Fecha Inicio
etiqueta_Fecha_Inicio = Label(pes2, text='Fecha Inicio: ',fg=colorLetra,bg=colorFondo).place(x=150,y=180)
entrada_Fecha_Inicio = DateEntry(pes2, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Inicio).place(x=300,y=180)




#Fecha Final
etiqueta_Fecha_Final = Label(pes2, text='Fecha Final: ',fg=colorLetra,bg=colorFondo).place(x=420,y=180)
entrada_Fecha_Final = DateEntry(pes2, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Final).place(x=500,y=180)



#Tasa interes
etiqueta_Tasa_interes = Label(pes2, text='Tasa interes: ',fg=colorLetra,bg=colorFondo).place(x=150,y=330)
entrada_Tasa_interes = Entry(pes2, textvariable=Tasa_interes,width=15).place(x=300,y=330)


#Tiempo de maduracion 
etiqueta_Time_maduracion = Label(pes2, text='Tiempo de maduracion: ',fg=colorLetra,bg=colorFondo).place(x=150,y=230)
entrada_Time_maduracion = Entry(pes2, textvariable=Time_maduracion,width=15).place(x=300,y=230)


#Precio de ejecucion  
etiqueta_Precio_ejecucion = Label(pes2, text='Precio de ejecucion : ',font=('Governor',10),fg=colorLetra,bg=colorFondo).place(x=150,y=280)
entrada_Precio_ejecucion = Entry(pes2, textvariable=Precio_ejecucion,width=15).place(x=300,y=280)

#boton
boton = Button(pes2, text='Procesar', command=procesar2, width=15, bg=colorFondo).place(x=300,y=380)










ventana.mainloop()




