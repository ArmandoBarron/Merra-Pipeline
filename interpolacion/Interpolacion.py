from netCDF4 import Dataset
import numpy as np
import os
from os import listdir
from os.path import join,isfile
from time import time
import csv
import argparse
import math

from os import scandir, getcwd

#base ="/home/robot/Escritorio/Projects/Merra_Master/Interpolation_merraJB/demo/" 
base = "./volumen/"
base = "./" #for testhing
#Las siguientes funciones son solo para desarrollo y conocimiento del dataset.
def DimensionesdeVariables(dataset):
	var= dataset.variables.keys()
	for v in var:
		print (dataset[v].shape)
		vdim= dataset[v].dimensions
		for vd in vdim:
			print (vd)
def PrintVariables(dataset):
	var= dataset.variables.keys()
	for v in var:
		vattrs=dataset[v].ncattrs() #diccionario de atributos
		print ("Numero de attributos"+str(len(vattrs)))
		for vat in vattrs:
			print ("att "+vat + ": "+str(getattr(dataset[v],vat)))
def PrintDimensions(dataset):
	dk=  dataset.dimensions
	for key in dk:
		print (key + " = " +str(len(dk[key])))

def PrintAtributos(dataset):
	gattrs = dataset.ncattrs()
	print ("NUMERO DE ATRIBUTOS: "+ str(len(gattrs)))
	for key in gattrs:
		print (key + " = " + str(getattr(dataset,key)))

def distance(lat1, long1, lat2, long2):
	# Convert latitude and longitude to 
	# spherical coordinates in radians.
	degrees_to_radians = math.pi/180.0
	phi1 = (90.0 - lat1)*degrees_to_radians
	phi2 = (90.0 - lat2)*degrees_to_radians

	theta1 = long1*degrees_to_radians
	theta2 = long2*degrees_to_radians
	cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
	arc = math.acos( cos )
	return arc
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def ls(ruta = getcwd()):
	if ruta[:-1] ==" ":
		ruta = ruta[:-1]
	return [arch.name for arch in scandir(ruta) if arch.is_file()]
#------------------------------------------------------------------------------------------------------------
#-----------------------------------------------INICIO DEL PROGRAMA------------------------------------------
######################### FLAGS
parser = argparse.ArgumentParser()
parser.add_argument("-i", help="Ruta de la carpeta de archivos")
parser.add_argument("-w", help="id del trabajador")
parser.add_argument("-d", help="lista de puntos")

args = parser.parse_args()
if args.i==None or args.w==None:
	print ("falta un argumento")
	exit(0)
else:
	folderIn = args.i
	workerID = args.w
	if args.d == None:
		ListaPuntos = "./estaciones.csv"
	else:
		ListaPuntos = args.d




#-------------------------------------------------------------------------------------------------------------
tiempo_inicial = time() 

#carpeta de logs y salida
if not os.path.exists(base+"logs/"):
    os.makedirs(base+"logs/")
if not os.path.exists(base+"output"+workerID+"/"):
    os.makedirs(base+"output"+workerID+"/")

logfile= open(join(base+"logs/","LOG_lote_"+workerID+".txt"), "a+")
logfile.write("########################\n")

station_list =[]
logfile.write("leer estaciones meteorologicas\n")
#se lee la lista de estaciones
with open(ListaPuntos, mode='r') as lista:
	lista_reader = csv.DictReader(lista)
	for x in lista_reader:
		station_list.append(x)
logfile.write("--- estaciones guardadas --- \n")


## se recorren todas las rutas de carpetas disponibles ##
logfile.write(folderIn+"\n")
folderIn = folderIn.split(",")
#logfile.write(folderIn)#array con direcciones de carpetas

for FI in folderIn:
	if FI == "": break
	FI = FI.replace(" ","")
	logfile.write("--------- FOLDER : "+FI+"\n\n")
	carpeta = ls(FI)
	print("data to process by %s: %s" %(workerID,len(carpeta)))
	for filename in carpeta: #all files in folder

		outfilename = filename[:-4]
		try:
			logfile.write("FILE: "+outfilename + "\n")
			file= open(join(base+"output"+workerID+"/",outfilename+".csv"), "w")
			writer = csv.writer(file)
			#log

			dataset = Dataset(join(FI, filename)) #se abre el archivo

			keys= dataset.variables.keys() 
			Varkey = []
			Varkey.append("antena")
			Varkey.append("latitud")
			Varkey.append("longitud")

			vr = []

			for v in keys:
				if (v != "lat" and v!= "lon" and v!="time"):
					Varkey.append(v)
					vr.append(dataset.variables[v][:])
			#PrintDimensions(dataset)

			writer.writerow(Varkey)

			########### VARIABLES ESENCIALES ############
			#OBTENER LOS DATOS DE CADA VARIABLE
			lat = dataset.variables["lat"][:]
			lon = dataset.variables["lon"][:]
			nc_time = dataset.variables["time"][:]
			#############################################

			vsize = len(vr) #cantidad de variables

			#HNORAIN= dataset.variables["HOURNORAIN"][:] #time-during_an_hour_with_no_precipitation
			#Temp_MAX=dataset.variables["T2MMAX"][:]
			#Temp_MIN=dataset.variables["T2MMIN"][:]
			#Temp_MEAN=dataset.variables["T2MMEAN"][:]
			#Prec_MAX =dataset.variables["TPRECMAX"][:] # total_precipitation

			estaciones_descartadas=0
			for station in station_list:
					towerlat=round(float(station['latitud']),3)
					towerlon=round(float(station['longitud']),3)
					pointlat = find_nearest(lat, towerlat) #encontrar valores norte y sur
					pointlon = find_nearest(lon, towerlon) #encontrar valores este y oeste

					if (towerlat>pointlat):
						North= pointlat +.5
						South= pointlat
					else:
						North = pointlat 
						South = pointlat-.5
						
					if (towerlon<pointlon):
						East= pointlon
						West= pointlon -.625
					else:
						East = pointlon +.625
						West = pointlon

					distSE=distance(towerlat,towerlon,South, East) #DISTANCE calcula great circle distance entre 2 puntos
					distNE=distance(towerlat,towerlon,North, East)
					distSW=distance(towerlat,towerlon,South, West)
					distNW=distance(towerlat,towerlon,North, West)
					distMAX=distance(South,East,North,West)

					DSE=(math.cos((math.pi/2)*(distSE/distMAX)))**4    #Calculo de pesos segun Zhao et al. 2005
					DNE=(math.cos((math.pi/2)*(distNE/distMAX)))**4
					DSW=(math.cos((math.pi/2)*(distSW/distMAX)))**4
					DNW=(math.cos((math.pi/2)*(distNW/distMAX)))**4

					wSE=DSE/(DSE+DNE+DSW+DNW)    #Calculo de pesos segun Zhao et al. 2005
					wNE=DNE/(DSE+DNE+DSW+DNW)
					wSW=DSW/(DSE+DNE+DSW+DNW)
					wNW=DNW/(DSE+DNE+DSW+DNW)

					KS=lat==South
					KN=lat==North
					KW=lon==West       #FIND encuentra la posicion de 97.5 dentro de la variable lon
					KE=lon==East
					
					#obtener indices de coordenadas
					KS=np.nonzero(KS)[0]
					KN=np.nonzero(KN)[0]
					KW=np.nonzero(KW)[0]  
					KE=np.nonzero(KE)[0]
					idx_time=np.nonzero(nc_time)[0]

					#Temperatura media
					res = [None]*5
					save=True
					for V in range(len(vr)):
						VSE=vr[V][:,KS,KE]
						VNE=vr[V][:,KN,KE]
						VSW=vr[V][:,KS,KW]
						VNW=vr[V][:,KN,KW]
						if(len(VSE[0])>0 and len(VNE[0])>0 and len(VSW[0])>0 and len(VNW[0])>0):
							res[V]=(((wSE*VSE)+(wNE*VNE)+(wSW*VSW)+(wNW*VNW)))- 273.15 #273
						else:
							save = False

					if save==True:
						try:
							for t in idx_time: #por cada valor de tiempo
									values =[]
									values.append(station['antena']) #tiempo
									values.append(round(float(station['latitud']),4)) #lat
									values.append(round(float(station['longitud']),4)) #tiempo
									for V in range(len(vr)):
										values.append(round(float(res[V][t][0]),5))
									writer.writerow(values)  #escribir linea
						except Exception as e:
							#estaciones_descartadas+=1
							#print North,South,East,West
							logfile.write(e +"\n")

			file.close()
		except Exception:
			print(filename)
		
tiempo_final = time() 
tiempo_ejecucion = tiempo_final - tiempo_inicial
print ("Time: "+str(tiempo_ejecucion))

logfile.write("########################\n")
logfile.close()


