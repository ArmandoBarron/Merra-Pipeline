import os
from threading import Thread


def split_list(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def check_downloaded_files(lista,path):
    new_lista=[]
    for l in lista:
        namefile = l.split("/")[-1]
        namefile=namefile.replace("\n","")
        #print(path+"/"+namefile)
        if os.path.isfile(path+"/"+namefile):
            pass
        else:
            new_lista.append(l)
    return new_lista



def pipe(id,lista):
    list_name="%s_list.txt" % id
    folder_name="%s_output" % id

    #print("old %s list: %s" % (id,len(lista)))
    lista= check_downloaded_files(lista,"./acq/"+folder_name)
    print("new %s list: %s" % (id,len(lista)))
    #print(lista)

    write_list_on_disk(lista,"./acq/"+list_name)
    print("descargando %s archivos " % len(lista))

    #se descargan los archivos
    os.system("cd acq; ./acq.sh %s %s" %(folder_name,list_name))

    folder_name="../acq/%s" % folder_name
    print("interpolando %s archivos " % len(lista))

    #se realiza la interpolacion
    os.system("cd interpolacion; python3 Interpolacion.py -w %s -i %s" %(id,folder_name))

def write_list_on_disk(lista,filename):
    with open(filename, 'w') as f:
        for item in lista:
            f.write("%s\n" % item)



workers = 4
filename = "enlaces.txt"

with open(filename) as f:
   enlaces = f.readlines()

sublistas = list(split_list(enlaces,workers))
print(type(sublistas))
threads = []
for ii in range(workers):
    # We start one thread per url present.
    process = Thread(target=pipe, args=[ii,sublistas[ii]])
    process.start()
    threads.append(process)
# We now pause execution on the main thread by 'joining' all of our started threads.
# This ensures that each has finished processing the urls.
for process in threads:
    process.join()