import os
from os import listdir
from os.path import join,isfile
from time import time
import csv
import math
import sys

from os import scandir, getcwd

#base ="/home/robot/Escritorio/Projects/Merra_Master/Interpolation_merraJB/demo/" 
base = "./volumen/"
base = "./" #for testhing
#Las siguientes funciones son solo para desarrollo y conocimiento del dataset.


def ls(ruta = getcwd()):
	if ruta[:-1] ==" ":
		ruta = ruta[:-1]
	return [arch.name for arch in scandir(ruta) if arch.is_file()]
#------------------------------------------------------------------------------------------------------------


path_folder = sys.argv[1] + "/"

output_folder = base+"prueba/"
#-------------------------------------------------------------------------------------------------------------
tiempo_inicial = time() 

#carpeta de logs y salida

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

carpeta = ls(path_folder)

cant_archivos=0
#se lee la lista de estaciones
for archivo in carpeta:
    try:
        fecha = archivo.split(".")[-2]
        if len(fecha)==8:
            fecha = "%s/%s/%s" %(fecha[6:8],fecha[4:6],fecha[0:4])
            with open(path_folder+archivo, mode='r') as lista:
                lista_reader = csv.reader(lista)
                next(lista_reader)
                for x in lista_reader:
                    x.append(fecha)
                    x.append(archivo)
                    lista_datos = ",".join(x)
                    with open(output_folder+x[0]+".csv", "a") as file_antena:
                        file_antena.write(lista_datos+"\n")    
                    #os.system("echo '%s' >> %s%s.csv" %(lista_datos,output_folder,x[0]))
            cant_archivos+=1
            print(cant_archivos)
    except Exception:
        with open("errores.txt", "a") as file_error:
            file_error.write(archivo+"\n")
            file_error.close()

tiempo_final = time() 
tiempo_ejecucion = tiempo_final - tiempo_inicial
print ("Time: "+str(tiempo_ejecucion))


