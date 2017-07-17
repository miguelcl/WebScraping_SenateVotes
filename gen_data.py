#el codigo se quedó pegado en leg353_ses62_num1 y no pudo crear los votos
#creo la carpeta y dentro Sesion_y_Tema

import csv
import os

#lista de todas las carpetas con votaciones
directory = os.path.join(os.getcwd() , "VOTOS")
os.walk(directory)
carpetas_proyectos=[x[1] for x in os.walk(directory)]
carpetas_proyectos = [x for x in carpetas_proyectos if x != []]

for carpeta in carpetas_proyectos[0]:
    
    #file = "C:/Users/Fgreve/Dropbox/votos_senadores/leg354_ses66_num1/Votacion.csv"
    file = os.path.join(directory , repr(carpeta).replace("'", ""), "Votacion.csv")
    votacion=[]
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            votacion.append(row)

    votacion = [[s.strip() for s in inner] for inner in votacion]
    votacion = [[s.replace("  "," ") for s in inner] for inner in votacion]
    votacion = [x for x in votacion if x != ['']]
    #print(votacion)


    #file = "C:/Users/Fgreve/Dropbox/votos_senadores/leg354_ses66_num1/Sesion_y_Tema.csv"
    file = os.path.join(directory , repr(carpeta).replace("'", ""), "Sesion_y_Tema.csv")
    sesionytema=[]
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            sesionytema.append(row)

    sesionytema = [[s.replace("  "," ") for s in inner] for inner in sesionytema]

    tema = ''.join(sesionytema[1])
    tema.strip()
    tema.replace("  ","")
    print(tema)

    #elimina espacios en blanco
    sesionytema = [[s.strip() for s in inner] for inner in sesionytema]

    print(sesionytema)

    #divide (ses) la fila sesion por los espacios en blanco
    ses_split = repr(sesionytema[0]).split()
    #print(ses_split)

    legislatura_num=ses_split[3]
    sesion_num=ses_split[1]
    dia_num=ses_split[5]
    mes_nombre=ses_split[7]
    ano_num=ses_split[9]

    num=carpeta[carpeta.find("m")+1:len(carpeta)]

    #reemplazo nombre de mes por numero
    if mes_nombre=="Enero": mes_num="1" 
    if mes_nombre=="Febrero": mes_num="2"
    if mes_nombre=="Marzo": mes_num="3"
    if mes_nombre=="Abril": mes_num="4"
    if mes_nombre=="Mayo": mes_num="5"
    if mes_nombre=="Junio": mes_num="6"
    if mes_nombre=="Julio": mes_num="7"
    if mes_nombre=="Agosto": mes_num="8"
    if mes_nombre=="Septiembre": mes_num="9"
    if mes_nombre=="Octubre": mes_num="10"
    if mes_nombre=="Noviembre": mes_num="11" 
    if mes_nombre=="Diciembre": mes_num="12"      


    #genera senador_name (nombre de senadores sin tildes ni espacios, para generar indice)
    import unicodedata
    def strip_accents(s):
       return ''.join(c for c in unicodedata.normalize('NFD', s)
                      if unicodedata.category(c) != 'Mn')

    senador_columna = [item[0] for item in votacion]

    senador_name = [rec.replace(" ", "_") for rec in senador_columna]
    senador_name = [rec.replace(".", "") for rec in senador_name]
    senador_name = [strip_accents(rec) for rec in senador_name]

    #print(senador_columna)
    #print(senador_name)



    header = votacion[0]
    header.append('Legislatura')
    header.append('Sesion') 
    header.append('Num')
    header.append('Dia')
    header.append('Mes')
    header.append('Año')
    header.append('Tema')
    header.append('Senador_name')
    #print(header)

    for i in range( 1, len(votacion)):
        votacion[i].append(legislatura_num)
        votacion[i].append(sesion_num)
        votacion[i].append(num)
        votacion[i].append(dia_num)
        votacion[i].append(mes_num)
        votacion[i].append(ano_num)
        votacion[i].append(tema)
        votacion[i].append(senador_name[i])

    #print(votacion)

    Data=[]
    Data.append(header)
    for i in range( 1, len(votacion)):
        Data.append(votacion[i])
    #print(Data)

    #guardar a archivo CSV
    #csvfile = "C:/Users/Fgreve/Dropbox/votos_senadores/leg354_ses66_num1/Data.csv"
    csvfile = os.path.join(directory , repr(carpeta).replace("'", ""), "Data.csv")
    with open(csvfile, "w", newline='\n') as file:
        writer = csv.writer(file)
        for item in Data: 
            writer.writerow(item)
            #print(item)
