from tkinter import *
import time
import fix_yahoo_finance as yf
#funciones de procesamiento
def procesar():
    data = yf.download(Codigo.get(), start=Fecha_Inicio.get(), end=Fecha_Final.get())
    etiqueta_actividad = Label(ventana, text=str(data))
    etiqueta_actividad.grid(row=14, column=1)
	

#Instancia de la clase Tk
ventana = Tk()
ventana.title('Valoración de Opciones sobre Acciones')

#Variables que almacenarán los datos
Codigo = StringVar()
Fecha_Inicio = StringVar()
Fecha_Final = StringVar()
Tasa_interes = IntVar()
actividad = StringVar()
actividad.set("Americana")
Fecha_Inicio.set(str(time.strftime("20%y-%m-%d")))
Fecha_Final.set(str(time.strftime("20%y-%m-%d")))

#generación de widgets
#Codigo
etiqueta_Codigo = Label(ventana, text='Codigo:')
entrada_Codigo = Entry(ventana, textvariable=Codigo)
etiqueta_Codigo.grid(row=2, column=1)
entrada_Codigo.grid(row=2, column=2)


#Fecha Inicio
etiqueta_Fecha_Inicio = Label(ventana, text='Fecha Inicio: ')
entrada_Fecha_Inicio = Entry(ventana, textvariable=Fecha_Inicio)
etiqueta_Fecha_Inicio.grid(row=4, column=1)
entrada_Fecha_Inicio.grid(row=4, column=2)

#Fecha Final
etiqueta_Fecha_Final = Label(ventana, text='Fecha Final: ')
entrada_Fecha_Final = Entry(ventana, textvariable=Fecha_Final)
etiqueta_Fecha_Final.grid(row=6, column=1)
entrada_Fecha_Final.grid(row=6, column=2)

#Tasa interes
etiqueta_Tasa_interes = Label(ventana, text='Tasa interes: ')
entrada_Tasa_interes = Entry(ventana, textvariable=Tasa_interes)
etiqueta_Tasa_interes.grid(row=8, column=1)
entrada_Tasa_interes.grid(row=8, column=2)


#OPCIONES
etiqueta_actividad = Label(ventana, text='OPCIONES: ')
entrada_actividad = OptionMenu(ventana, actividad, "Americana", "Europea", "Monte-Carlod")
etiqueta_actividad.grid(row=10, column=1)
entrada_actividad.grid(row=10, column=2)

#boton
boton = Button(ventana, text='Procesar', command=procesar, width=20)
boton.grid(row=12, column=3)

#ejecución de ventana
ventana.mainloop()
