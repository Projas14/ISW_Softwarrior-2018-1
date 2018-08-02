import fix_yahoo_finance as yf
from tkinter import messagebox


def procesar(Codigo,Fecha_Inicio,Fecha_Final):
    print("holi")
    if Codigo != "":
        
        data = yf.download(Codigo, start=Fecha_Inicio, end=Fecha_Final)
        print (guardar(data,Codigo))
        limpieza = (str(data).split("\n"))
        DataFinal = []
        for linea in limpieza[1:]:
            datos = linea.split()
            if len(datos) > 5:
                DataFinal.append([datos[0],datos[4]])

        if len(DataFinal) == 0:
            messagebox.showwarning("Advertencia","Informacion invalida vuelva a intentar")
        else:
            messagebox.showinfo("Ok","Datos Listos y almacenados")
            print (DataFinal)
    else:
        print ("Bienvenidos usuario X")


def guardar(data,Codigo):
    archivo = open("../cache" + str(Codigo)+".txt", "w")
    archivo.write(str(data))
    archivo.close()
    return ("Guardado")
