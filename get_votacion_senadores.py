#Author: Fernando Greve fgreve@gmail.com
#This code scraps the Chilean Senate Webpage and constructs a database with
#votes of every law project available online. In particular, the code
#automaticatly generates a folder for every project and save a csv with votes
#and other csv with some project details.
#In total there are around 360 projects.

#extraer datos web
import urllib
import urllib.request
from bs4 import BeautifulSoup

#gestion de archivos
import os
import os.path
import shutil

#csv
import csv


#Funcion que realiza un enlace
def make_soup(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    return soupdata


def gen_sesiones(url):
    soup = make_soup(url)
    #Tabla de Sesiones (SesTab)
    SesTab = soup.find("select", { "name" : "sesionessala" })
    if SesTab is None:
        return 0   
    #genera lista vacia
    Sesiones_fecha=[]
    Sesiones_num=[]
    #genera la tabla Sesiones
    for fila in SesTab.findAll('option'):
        Sesiones_fecha.append(fila.text)
    #print(Sesiones_fecha)
    #genera lista vacia
    SesTab_options=[]
    #imprimimos el value de las options en SesTab
    for fila in SesTab.findAll('option'):
        SesTab_options.append(fila['value'])
    #print(SesTab_options)
    return SesTab_options


def gen_legislaturas(url):
    soup = make_soup(url)
    #Tabla de Legislaturas (LegTab)
    LegTab = soup.find("select", { "name" : "legislaturas" })
    #genera lista vacia
    Legislaturas=[]
    #genera la tabla Legislaturas
    for fila in LegTab.findAll('option'):
        Legislaturas.append(fila.text[:3])
    #print(Legislaturas)
    #genera lista vacia
    LegTab_options=[]
    #imprimimos el value de las options en LegTab
    for fila in LegTab.findAll('option'):
        LegTab_options.append(fila['value'])
    #print(LegTab_options)
    return LegTab_options


def gen_proyectos(url):
    #coneccion con la web del senado
    soup = make_soup(url)
    #Tabla de Proyectos (LegTab)
    ProyTab = soup.find("table", { "width" : "100%" })
    if ProyTab is None:
        return 0   
    #genera lista vacia
    Proyectos=[]
    #genera la tabla Legislaturas
    for fila in ProyTab.findAll('tr'):
        Proyectos.append(fila)
    #genera lista vacia
    Proyectos_link=[]
    for link in ProyTab.find_all('a'):
        Proyectos_link.append(link.get('href'))
        #print(link.get('href'))
    #print(Proyectos_link)
    if not Proyectos_link:
        return 0 
    return Proyectos_link


def gen_votos(url, folder):
    soup = make_soup(url)
    #Tabla de Votos con todo el código HTML (VotTab)
    VotTab = soup.find("table", { "width" : "100%" })
    if VotTab is None:
        return 0 
    #genera una lista de los que votaron (Votos_nombres)
    Votos_nombres=[]
    #genera la tabla Votos
    for fila in VotTab.findAll('tr'):
        for columna in fila.findAll('td'):
            if len(columna.text)>3:
                Votos_nombres.append(columna.text.replace(',', ''))
    #genera lista vacia
    VotTab_src=[]
    #imprimimos el value de las options en VotTab
    for fila in VotTab.findAll("img"):
        VotTab_src.append(fila['src'])
    Voto=[]
    for fila in VotTab.findAll('tr'):
        for cell in fila.findAll('td'):
            Voto.append(cell.findAll('img'))
            #print(cell.findAll('img'))
    Votacion=[]
    j=1
    for i in range(len(Voto)):
        if j==6: j=1
        if len(Voto[i])>0:
            #print(len(Voto[i]))
            if j==2: Votacion.append("Si") 
            if j==3: Votacion.append("No")
            if j==4: Votacion.append("Abstencion")
            if j==5: Votacion.append("Pareo")
        j=j+1
    matriz_votos=[]
    for i in range(len(Votacion)):
        matriz_votos.append(Votos_nombres[i]+" , "+Votacion[i]+" \n")
    header="Senador , Voto"
    #guardar a archivo CSV
    csvfile = "C:/Users/Fgreve/Dropbox/votos_senadores/"+folder+"/Votacion.csv"
    with open(csvfile, "w", newline='\n') as file:
        writer = csv.writer(file, quotechar=' ')
        writer.writerow([header])
        for item in matriz_votos: 
            writer.writerow([item])
            #print(item)


def gen_sesionytema(url, folder):
    soup = make_soup(url)
    A=soup.find("div", { "class" : "col1" })
    if A is None:
        return 0 
    B=[]
    for string in A.stripped_strings:
        B.append(repr(string))
        #print(repr(string))
    Sesion=B[0].replace("'", "")+" "+B[1].replace("'", "")
    Tema=B[2].replace("'", "")+" "+B[3].replace("'", "")
    #guardar a archivo CSV
    csvfile = "C:/Users/Fgreve/Dropbox/votos_senadores/"+folder+"/Sesion_y_Tema.csv"
    with open(csvfile, "w", newline='\n') as file:
        writer = csv.writer(file, quotechar=' ')
        writer.writerow([Sesion])
        writer.writerow([Tema])   


def gen_folder(url, n):
    soup = make_soup(url)
    A=soup.find("div", { "class" : "col1" })
    if A is None:
        return 0 
    B=[]
    for string in A.stripped_strings:
        B.append(repr(string))
        #print(repr(string))
    b=B[1].split( )
    #print(b)
    #print(b[0].replace("'", "")+"_"+b[2]+"_")
    folder_name = "leg"+b[2]+"_ses"+b[0].replace("'", "")+"_num"+n
    ##if os.path.exists(folder_name):
        ##os.remove(folder_name)
    os.makedirs(folder_name)
    return folder_name



url_legislaturas = "http://www.senado.cl/appsenado/index.php?mo=sesionessala&ac=votacionSala&legiini=462"
#print(url1)

legislaturas = gen_legislaturas(url_legislaturas)
#print(legislaturas)

for j in range(len(legislaturas)):
    url = "http://www.senado.cl/appsenado/index.php?mo=sesionessala&ac=votacionSala&legiini=361&legiid="+legislaturas[j]
    #print(url)
    sesiones = gen_sesiones(url)
    #print(sesiones)
    if sesiones != 0:
        for k in range(len(sesiones)):
            if k != 0:
                url_sesion = "http://www.senado.cl/appsenado/index.php?mo=sesionessala&ac=votacionSala&legiini=361&legiid="+legislaturas[j]+"&sesiid="+sesiones[k]
                #print(url_sesion)
                proyectos=gen_proyectos(url_sesion)
                if proyectos != 0:
                    #print(proyectos)
                    for i in range(len(proyectos)): 
                        url_proyecto = "http://www.senado.cl/appsenado/"+proyectos[i]
                        #print(url_proyecto)
                        folder=gen_folder(url_proyecto, str(i+1))
                        print(folder)
                        gen_sesionytema(url_proyecto, folder)
                        votos=gen_votos(url_proyecto, folder)

