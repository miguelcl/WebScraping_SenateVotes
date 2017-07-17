import csv
import os

#lista de todas las carpetas con votaciones
directory = os.path.join(os.getcwd() , "VOTOS")
os.walk(directory)
carpetas_proyectos=[x[1] for x in os.walk(directory)]
carpetas_proyectos = [x for x in carpetas_proyectos if x != []]


#genera VotosSenado que contendra la base completa de votaciones
#y le asigna el header
header =[]
header.append('Senador')
header.append('Voto')
header.append('Legislatura')
header.append('Sesion')
header.append('Num')
header.append('Dia')
header.append('Mes')
header.append('Año')
header.append('Tema')
header.append('Senador_name')
#print(header)

VotosSenado=[]
VotosSenado.append(header)

for carpeta in carpetas_proyectos[0]:
    #file = "C:/Users/Fgreve/Dropbox/votos_senadores/leg354_ses66_num1/Votacion.csv"
    file = os.path.join(directory , repr(carpeta).replace("'", ""), "Data.csv")
    votacion=[]
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            votacion.append(row)

    for i in range( 1, len(votacion)):
        VotosSenado.append(votacion[i])


#define el directorio fuera de VOTOS
directory = os.path.join(os.getcwd())
os.walk(directory)

csvfile = os.path.join(directory , "VotosSenado.csv")
with open(csvfile, "w", newline='\n') as file:
    writer = csv.writer(file)
    for item in VotosSenado: 
        writer.writerow(item)
        #print(item)

