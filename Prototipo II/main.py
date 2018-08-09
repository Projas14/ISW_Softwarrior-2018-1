# !/usr/bin/python3
from tkinter.ttk import  Style
from tkinter import *
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk
from tkinter import messagebox
import time
import fix_yahoo_finance as yf
from tkcalendar import Calendar, DateEntry
from tkinter import filedialog

import quandl
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import *
from decimal import *
import random
#|--------------------------------------------------|
#|                  FUNCIONES                       |
#|--------------------------------------------------|



#Calculamos los n numeros aleatorios de 0 a raiz de t para hacer la simulacion   
def aleatorios(t,n):
    numeros = list()
    for i in range(n):
        numeros.append(random.uniform(0,float(t**0.5)))
    return numeros

#Precios aplicados con los numeros aleatorios
def funcion_precio(v,r,Pi,t,numeros):
    precios = list()
    for z in numeros:
        precios.append(Pi*math.exp(r-(0.5*v**2))*t + v*z)
    return precios

#Calculamos el maximo de los precios menos el precio de ejercicio
def maximo(v,r,Pi,t,n,k):
    al = aleatorios(t,n)
    precios = funcion_precio(v,r,Pi,t,al)
    resta = list()
    for p in precios:
        resta.append(p-k)
    resta.append(0)
    return max(resta)


#Ingresas la volatilidad, la tasa de interes, la lista con todos los precios de los activos de la accion, la fecha de inicio(solo una constante), cantidad de iteraciones y el precio de ejercicio que te da el cliente
def Monte_Carlo(volatilidad,intereses,Precios,t,iteraciones,Pejercicio):
    multiplicador = 0
    maximos = list()
    for p in Precios:
        maximos.append(maximo(volatilidad,intereses,p,t,iteraciones,Pejercicio))
    print(maximos)
    for m in maximos:
       multiplicador += m
    multiplicador = multiplicador/len(Precios)
    return math.exp(-intereses*t)*multiplicador

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

#Funciones nuevas pestañas 
def Resultados_online(volatividad):
	pes4 = ttk.Frame(notebook,style='My.TFrame')
	notebook.add(pes4,text="Resultados_OnLine")
	Banner4 = PhotoImage(file="img/bienvenidos2.png")
	lblBanner4 = Label(pes4,image=Banner4,bg=colorFondo).place(x=0,y=0)
	etiqueta1 = Label(pes4, text='El Resultado final es de : ',font=('Governor',20),fg=colorLetra,bg=colorFondo).place(x=150,y=280)
	etiqueta2 = Label(pes4, text=str(volatividad),font=('Governor',20),fg=colorLetra,bg=colorFondo).place(x=150,y=380)
	








def pestaña_offline(volatividad):
		pes3 = ttk.Frame(notebook,style='My.TFrame')
		notebook.add(pes3,text="Resultados_offline")
		#logo
		Banner3 = PhotoImage(file="img/bienvenidos.png")
		lblBanner3 = Label(pes3,image=Banner3,bg=colorFondo).place(x=0,y=0)
		etiqueta1_1 = Label(pes3, text='El Resultado final es de : ',font=('Governor',20),fg=colorLetra,bg=colorFondo).place(x=150,y=280)
		etiqueta2_1 = Label(pes3, text=str(volatividad),font=('Governor',20),fg=colorLetra,bg=colorFondo).place(x=150,y=380)




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
    print(Fecha_Inicio.get(),Fecha_Final.get())
    aapl = yf.download(Codigo.get(), start=invertir_fecha(Fecha_Inicio.get()), end=invertir_fecha(Fecha_Final.get()))
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
        volatividad = sigma(functionS(test)+functionS(test2))
        messagebox.showinfo("ok","la Volatividad es de: "+ str(volatividad))
        resultado = Monte_Carlo(volatividad,Tasa_interes.get(),test,1,100,Precio_ejecucion.get())
        messagebox.showinfo("ok","El resultado es  de: "+ str(resultado))
        Resultados_online(resultado)
        
    else:
        volatividad =sigma(functionS(test))
        messagebox.showinfo("ok","la Volatividad es de: "+ str(volatividad))
        resultado = Monte_Carlo(volatividad,Tasa_interes.get(),test,1,100,Precio_ejecucion.get())
        messagebox.showinfo("ok","El resultado es  de: "+ str(resultado))
        Resultados_online(resultado)
        
        
        


def procesar2():
	import csv
	with open(Archivo.get(), newline='') as File:  
		reader = csv.reader(File)
		contador = 0
		DataFinal = []
		for row in reader:
			if contador != 0:
				DataFinal.append(float(row[4]))
			contador = contador + 1
	if Time_maduracion.get() > 3:
		volatividad2 = sigma(functionS(DataFinal))
		messagebox.showinfo("ok","la Volatividad es de: "+ str(volatividad2))
		resultado = Monte_Carlo(volatividad2,Tasa_interes.get(),DataFinal,1,100,Precio_ejecucion.get())
		messagebox.showinfo("ok","El resultado es  de: "+ str(resultado))
		pestaña_offline(resultado)
		

	else:
		volatividad2 = sigma(functionS(DataFinal))
		messagebox.showinfo("ok","la Volatividad es de: "+ str(volatividad2))
		resultado = Monte_Carlo(volatividad2,Tasa_interes.get(),DataFinal,1,100,Precio_ejecucion.get())
		messagebox.showinfo("ok","El resultado es  de: "+ str(resultado))
		pestaña_offline(resultado)

    
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
ventana.geometry("754x480+100+100")

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
entrada_Fecha_Final = DateEntry(pes1, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Final)
entrada_Fecha_Final.place(x=500,y=180)



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
Fecha_Inicio2 = StringVar()
Fecha_Final2 = StringVar()
Tasa_interes2 = IntVar()
Fecha_Inicio2.set(str(time.strftime("20%y-%m-%d")))
Fecha_Final2.set(str(time.strftime("20%y-%m-%d")))
Time_maduracion2 = IntVar()
Precio_ejecucion2 = IntVar()


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
entrada_Fecha_Inicio = DateEntry(pes2, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Inicio2).place(x=300,y=180)



#Fecha Final
etiqueta_Fecha_Final = Label(pes2, text='Fecha Final: ',fg=colorLetra,bg=colorFondo).place(x=420,y=180)
entrada_Fecha_Final = DateEntry(pes2, width=12, background='darkblue',foreground='white', borderwidth=2, textvariable=Fecha_Final2)
entrada_Fecha_Final.place(x=500,y=180)




#Tasa interes
etiqueta_Tasa_interes = Label(pes2, text='Tasa interes: ',fg=colorLetra,bg=colorFondo).place(x=150,y=330)
entrada_Tasa_interes = Entry(pes2, textvariable=Tasa_interes2,width=15).place(x=300,y=330)


#Tiempo de maduracion 
etiqueta_Time_maduracion = Label(pes2, text='Tiempo de maduracion: ',fg=colorLetra,bg=colorFondo).place(x=150,y=230)
entrada_Time_maduracion = Entry(pes2, textvariable=Time_maduracion2,width=15).place(x=300,y=230)


#Precio de ejecucion  
etiqueta_Precio_ejecucion = Label(pes2, text='Precio de ejecucion : ',font=('Governor',10),fg=colorLetra,bg=colorFondo).place(x=150,y=280)
entrada_Precio_ejecucion = Entry(pes2, textvariable=Precio_ejecucion2,width=15).place(x=300,y=280)

#boton
boton = Button(pes2, text='Procesar', command=procesar2, width=15, bg=colorFondo).place(x=300,y=380)


#variables pestaña 2
#generación de widgets
#logo
# Banner2 = PhotoImage(file="img/bienvenidos2.png")
# lblBanner2 = Label(pes3,image=Banner2,bg=colorFondo).place(x=0,y=0)








ventana.mainloop()




