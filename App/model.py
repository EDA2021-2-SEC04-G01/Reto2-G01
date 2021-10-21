"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """



from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
import math as m
import textwrap
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as insert
from DISClib.Algorithms.Sorting import quicksort as qsort
from DISClib.Algorithms.Sorting import mergesort as msort
assert cf
from tabulate import tabulate
import textwrap
import time
import datetime
"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
"""
IMPORTANTE:
Puede que haya algunas diferencias con los resultados mostrados en el ejemplo, sin embargo es
debido a que se usaron array list, lo que hace que funcione diferente el ordenamiento. Las cantidades, sin embargo son las mismas.
"""
# Construccion de modelos

def newCatalog():
    catalog = {
        'artworks':lt.newList('ARRAY_LIST'),
        'artists':mp.newMap(2000,maptype='CHAINING',loadfactor=0.8),
        'nationalities':mp.newMap(50,maptype='CHAINING',loadfactor=0.7,comparefunction=compareNation),
        'mediums': mp.newMap(25,maptype='PROBING',loadfactor=0.7,comparefunction=compareMediums),
        'dateArtists': mp.newMap(2025,maptype='CHAINING',loadfactor=0.5),
        'dateArtworks': mp.newMap(1000, maptype='CHAINING',loadfactor=0.5),
        'artworksArtists':mp.newMap(20,maptype='CHAINING',loadfactor=0.5),
        'departments' : mp.newMap(20,maptype='PROBING',loadfactor=0.6),
        'artistsNames' :mp.newMap(20,maptype='PROBING',loadfactor=0.6)
    }
    return catalog
# Funciones para agregar informacion al  catalogo


def addartistName(catalog,artwork):
    ids = artwork['ConstituentID']
    ids = ids.replace('[','').replace(']','').split(',') 
    for id in ids:
        id = id.strip()
        if mp.contains(catalog['artists'],id):
            name = (mp.get(catalog['artists'],id)['value'])['DisplayName']
            if mp.contains(catalog['artistsNames'],name):
                lista = mp.get(catalog['artistsNames'],name)['value']
            else:
                lista = lt.newList()

            lt.addLast(lista,artwork)
            mp.put(catalog['artistsNames'],name,lista)



def addArtworksArtist(catalog,artwork):
    artists = catalog['artists']
    medium = artwork['Medium']

    date = artwork['DateAcquired']
    if date =='' or date==None:
        artwork['DateAcquired'] = '2100-12-24'

    idArtist = artwork['ConstituentID'].replace('[','').replace(']','').split(',')
    for currentArtist in idArtist:
        currentArtist=currentArtist.strip() #Strip quita espacios innecesarios

        if mp.contains(catalog['artworksArtists'],currentArtist): listArtwork=mp.get(catalog['artworksArtists'],currentArtist)['value']
        else:listArtwork=lt.newList('SINGLE_LINKED')
        
        lt.addLast(listArtwork,artwork)
        mp.put(catalog['artworksArtists'],currentArtist,listArtwork)
    
def addArtist(catalog,artist):
    id=artist['ConstituentID']
    mp.put(catalog['artists'],str(id),artist)


def addDate(catalog,artist):
    date = str(artist['BeginDate'].strip())

    if mp.contains(catalog['dateArtists'],date):
        artistsList = me.getValue(mp.get(catalog['dateArtists'],date))

    else:
        artistsList = lt.newList('SINGLE_LINKED')
    lt.addLast(artistsList,artist)
    mp.put(catalog['dateArtists'],date,artistsList)

def addArtwork(catalog,artwork):
    lt.addLast(catalog['artworks'],artwork)


def addNation(catalog,artwork):
    mpArtists=catalog['artists']
    artistList=(artwork['ConstituentID'].replace('[','').replace(']','')).split(',')
    if artistList!=None or artistList!=[]:
        for artist in artistList:
            artist = artist.strip()
            if mp.contains(mpArtists,artist):
                nationality = mp.get(mpArtists,artist)['value']['Nationality']

                if nationality=='' or nationality==None:
                    nationality='Nationality unknown'

                if mp.get(catalog['nationalities'],nationality):
                    artworks=me.getValue(mp.get(catalog['nationalities'],nationality))
                else:
                    artworks = lt.newList('SINGLE_LINKED')
                lt.addLast(artworks,artwork)
                mp.put(catalog['nationalities'],nationality,artworks)

def addMedium(catalog,artwork):
    if mp.contains(catalog['mediums'],artwork['Medium']):
        artworks= me.getValue(mp.get(catalog['mediums'],artwork['Medium']))

    else:
        artworks = lt.newList('SINGLE_LINKED')
    lt.addLast(artworks,artwork)
    mp.put(catalog['mediums'],artwork['Medium'],artworks)

def addArtworkbyDate(catalog,artwork):
    date = artwork['DateAcquired']
    if date =='' or date==None:
        date = '2100-12-24'
    mapDates = catalog['dateArtworks']
    if mp.contains(mapDates,date):
        artworks = me.getValue(mp.get(mapDates,date))
    else:
        artworks = lt.newList('SINGLE_LINKED')

    lt.addLast(artworks,artwork)
    mp.put(mapDates,date,artworks)


def addToDpto(catalog,artwork):
    dpto = artwork['Department']
    mapDpto = catalog['departments']
    if mp.contains(mapDpto,dpto):
        artworks = me.getValue(mp.get(mapDpto,dpto))
    else:
        artworks = lt.newList('SINGLE_LINKED')
    lt.addLast(artworks,artwork)
    mp.put(mapDpto,dpto,artworks)

# Funciones para creacion de datos


# Funciones utilizadas para comparar elementos dentro de una lista

def compareQuantityMedium(medium1,medium2):
    return medium1['value'] > medium2['value']

def sortMediumArtist(listMediums):
    sa.sort(listMediums,compareQuantityMedium)

def compareMediums(artworkMedium,entry):
    mediumentry = me.getKey(entry)
    if artworkMedium == mediumentry:
        return 0
    elif artworkMedium>mediumentry:
        return 1

    return -1


def compareNation(artistNation,entry):
    nationEntry=me.getKey(entry)
    if nationEntry == artistNation:
        return 0
    return -1

def compareArtists(artistid,entry):
    artistEntry=me.getKey(entry)
    if str(artistid) == str(artistEntry):
        return 0
    return -1

def compareArtworks(artwork1,artwork):
    if (str(artwork1) == str(artwork['ObjectID'])):
        return 0
    return -1

def compareQuantity(nation1,nation2):
    return nation1['size'] > nation2['size']

def compareDates(date1,date2):
    return (date1<date2)

def compareYears(artwork1,artwork2):
    if artwork1['Date']=='None' or artwork1['Date']=='':
        artwork1['Date']=5000
    if artwork2['Date']=='None' or artwork2['Date']=='':
        artwork2['Date']=5000
    return int(artwork1['Date'])<int(artwork2['Date'])

def comparePrices(artwork1,artwork2):
    return artwork1['Price']>artwork2['Price']

def compareArtDates(art1,art2):
    date1 = time.strptime(art1,'%Y-%m-%d')
    date2 = time.strptime(art2,'%Y-%m-%d')
    return (date1<date2)

def compareArtDates_op2(art1,art2):
    art1 = art1['DateAcquired']
    art2 = art2['DateAcquired']
    return compareArtDates(art1,art2)

def compareArtistsArtworks(art1,art2):
    cant_obras1 = art1['cant_obras']
    cant_mediums1 = art1['cant_mediums']
    cant_obras2 = art2['cant_obras']
    cant_mediums2 = art2['cant_mediums']

    if cant_obras1 == cant_obras2:
        return cant_mediums1>cant_mediums2
    return cant_obras1>cant_obras2

# Funciones de ordenamiento
def sortDates(keySet):
    sa.sort(keySet,compareDates)


def sortArtYears(artworks):
    sa.sort(artworks,compareYears)

def sortArtworksDates(datesList):
    sa.sort(datesList,compareArtDates)

def sortArtworksDates_op2(datesList):
    sa.sort(datesList,compareArtDates_op2)

def sortNation(nationality):
    sa.sort(nationality,compareQuantity)


def sortArtPrice(artworks):
    msort.sort(artworks,comparePrices)

def sortArtistsArtworks(artists):
    sa.sort(artists,compareArtistsArtworks)

def masAntiguos(catalog,medium,cant):
    medium=mp.get(catalog['mediums'],medium)
    if medium!=None:
        listArtworks=me.getValue(medium)
        sa.sort(listArtworks,cmpfunction=compareYears)
        return lt.subList(listArtworks,1,cant)

    else:
        return 'No hay nada'





#Req 1.
def cronoArtist(catalog, inicio, fin):
    completeList=lt.newList('SINGLE_LINKED')
    keySet=mp.keySet(catalog['dateArtists'])
    sortDates(keySet)
    for date in lt.iterator(keySet):
        if int(date) in range(inicio,fin+1): 
            for artist in lt.iterator(mp.get(catalog['dateArtists'],date)['value']):
                lt.addLast(completeList,artist)
        elif int(date)>fin+1:
            break
    if lt.isEmpty(completeList):
        return "No hay artistas en el rango indicado"

    else: 
        lstArtist=[]
        artistCant = lt.size(completeList)
        for position in range(1,4):
            selectArtist(position,completeList,lstArtist,False)
        for position in range(lt.size(completeList)-2,lt.size(completeList)+1):
            selectArtist(position,completeList,lstArtist,False)
        headers = ['ConstituentID','DisplayName','BeginDate','Nationality','Gender','ArtistBio','Wiki QID','ULAN']
        tabla = tabulate(lstArtist,headers=headers,tablefmt='grid')

    return (tabla,artistCant)

#↑↑↑Aquí termina el Req1 ↑↑↑

#Req2.
def cronoArtwork(catalog, inicio, fin):
    inicio = time.strptime(inicio,"%Y-%m-%d")
    fin = time.strptime(fin,"%Y-%m-%d")
    dates = mp.keySet(catalog['dateArtworks'])
    purchasedCant=0 
    FilteredList=lt.newList('ARRAY_LIST')
    mpArtists = mp.newMap(numelements=1,maptype='CHAINING',loadfactor=0.7)

    sortArtworksDates(dates)

    for date in lt.iterator(dates):
        dateFormat = time.strptime(date,'%Y-%m-%d')
        if dateFormat>=inicio and dateFormat<=fin:
            artworks = mp.get(catalog['dateArtworks'],date)['value']
            for artwork in lt.iterator(artworks):
                lt.addLast(FilteredList,artwork)

                if 'purchase' in artwork['CreditLine'].lower():
                    purchasedCant+=1
                
                idArtist = artwork['ConstituentID'].replace('[','').replace(']','').split(',')
                for id in idArtist:
                    id = id.strip()
                    mp.put(mpArtists,id,'Nada')

        elif dateFormat>fin: #Como está ordenado cuando se sale del rango deja de iterar.
            break

    if lt.isEmpty(FilteredList):
        return "No hay obras de arte en el rango indicado"
    else:
        cantArtists = mp.size(mpArtists)
        listReturn = []
        for position in range(1,4):
            selectInfo(position,FilteredList,listReturn,catalog,False,False,False)

        for position in range(lt.size(FilteredList)-2,lt.size(FilteredList)+1):
            selectInfo(position,FilteredList,listReturn,catalog,False,False,False)
        headers = ['ObjectID','Title','Artist(s)','Medium','Dimensions','Date','Department','Classification','URL']
        tabla = tabulate(listReturn,headers=headers,tablefmt='grid',numalign='center')
        return (tabla,lt.size(FilteredList),purchasedCant,cantArtists)
#↑↑↑Aquí termina el Req2.↑↑↑

#REQ 3 ELABORADO POR DANIEL MOLANO - 202012695


def buscarArtista(name,catalog):
    artistas = catalog['artistsNames']
    tecnicas = mp.newMap(20,maptype='PROBING',loadfactor=0.6)
    cantidades = lt.newList('ARRAY_LIST')
    obras_final= lt.newList('ARRAY_LIST')
    listCant = []
    listArtworksEnd=[]
    cant_mayor=0
    if mp.contains(artistas,name):
        obras = mp.get(artistas,name)['value']
        total_obras = lt.size(obras)
        for obra in lt.iterator(obras):
            if mp.contains(tecnicas,obra['Medium']):
                cant=mp.get(tecnicas,obra['Medium'])['value']+1
            else:
                cant = 1
            if cant>cant_mayor:
                cant_mayor=cant
                medio_mayor= obra['Medium']
            mp.put(tecnicas,obra['Medium'],cant)
        
        for tecnica in lt.iterator(mp.keySet(tecnicas)):
            cantidad = (mp.get(tecnicas,tecnica)['value'])
            lt.addLast(cantidades,{'tecnica':tecnica,'value':cantidad})

        sortMediumArtist(cantidades)

        
        for obra in lt.iterator(obras):
            if medio_mayor == obra['Medium']:
                lt.addLast(obras_final,obra)

        cant_tecnicas = mp.size(tecnicas)


        for position in range(1,4):
            selectInfo(position,obras_final,listArtworksEnd,catalog,False,False,False)

        for position in range(lt.size(obras_final)-3,lt.size(obras_final)):
            selectInfo(position,obras_final,listArtworksEnd,catalog,False,False,False)
        headers = ['ObjectID','Title','Artist(s)','Medium','Dimensions','Date','Department','Classification','URL']
        tabla=(tabulate(listArtworksEnd, headers=headers, tablefmt='grid',numalign='center'))
        
        headers_cantidad = ['Medium Name','Cant']
        for position in range(1,6):
            medium = lt.getElement(cantidades,position)
            size = medium['value']
            listCant.append([medium['tecnica'],size])

        tabla_cantidad = tabulate(listCant,headers=headers_cantidad,tablefmt='grid',numalign='right')
        return(total_obras,cant_tecnicas,medio_mayor,tabla_cantidad,tabla)

    else:
        return 'No existe un artista con el nombre ingresado.'


#Comienza el Req4.  ELABORADO POR: GERMÁN LEONARDO MORENO CAINABA. COD->202116701
def ordenNacionalidad(catalog):
    nacionalidades=mp.keySet(catalog['nationalities'])
    listNacionalidades=lt.newList()
    listArtworksEnd=[]
    listCant=[]

    for nation in lt.iterator(nacionalidades):
        size = lt.size(mp.get(catalog['nationalities'],nation)['value'])
        lt.addLast(listNacionalidades,{'nation':nation,'size':size})
    sortNation(listNacionalidades)

    nameMayor = lt.firstElement(listNacionalidades)['nation']
    mayor = mp.get(catalog['nationalities'],nameMayor)['value']

    for position in range(1,4):
        selectInfo(position,mayor,listArtworksEnd,catalog,False,False,False)

    for position in range(lt.size(mayor)-3,lt.size(mayor)):
        selectInfo(position,mayor,listArtworksEnd,catalog,False,False,False)

#       Se hacen los headers, para ponerlos en la tabla
    headers = ['ObjectID','Title','Artist(s)','Medium','Dimensions','Date','Department','Classification','URL']
#       Se crea la tabla pasándole como parámetro la lista grande, los headers creados al final y format grid para que se vea más como una tabla.
    tabla=(tabulate(listArtworksEnd, headers=headers, tablefmt='grid',numalign='center'))

    for position in range(1,11):
        nation = lt.getElement(listNacionalidades,position)
        size = nation['size']
        listCant.append([nation['nation'],size])

    tablaCant = tabulate(listCant,headers=['Nationality','Artworks'],tablefmt='grid',numalign='right')

    
    return (tablaCant,tabla,nameMayor,lt.size(mayor))

# #↑↑↑Aquí termina el req4.↑↑↑

# Req 5
def check_none(artwork,clave):
    if artwork[clave]!='' and artwork[clave]!=None:
        return float(artwork[clave])/100
    else:
        return 0
def cambiar_uno(variable):
    if variable==0:
        return 1
    else:
        return variable
def precioTransporte(catalog,department):
    artworks = mp.get(catalog['departments'],department)['value']
    listbyPrice=[] #Estas dos listas son para pasarle al módulo tabulate
    listbyDate=[]
    precio = 0
    estimado_peso=0
    for artwork in lt.iterator(artworks):
        rad=0
        op1=0
        op2=0
        op3=0
        no_ceros=0
        circ = check_none(artwork,'Circumference (cm)')
        diam = check_none(artwork,'Diameter (cm)')
        prof =  check_none(artwork,'Depth (cm)')
        height =  check_none(artwork,'Height (cm)')
        leng =  check_none(artwork,'Length (cm)')
        width =  check_none(artwork,'Width (cm)')
        peso=0
        if artwork['Weight (kg)']!='' and artwork['Weight (kg)']!=None:
            peso =  float(artwork['Weight (kg)'])
            estimado_peso+=peso

        lista = [prof,height,leng,width]
        for dato in lista:
            if dato!=0:
                no_ceros+=1
        if no_ceros>=2 :

            prof = cambiar_uno(prof)
            height = cambiar_uno(height)
            leng = cambiar_uno(leng)
            width = cambiar_uno(width)
            
            if circ!=0: rad = circ/2*m.pi
            elif diam!=0: rad = diam/2

            if rad != 0: op1 = m.pow(rad,2)*m.pi*height*72

            else: op2 = prof*height*leng*width*72

            op3 = peso*72
            actual_precio = max([op1,op2,op3])
            artwork['Price']=actual_precio
            precio += actual_precio
        else:
            artwork['Price']=48
            precio+=48

    sortArtPrice(artworks)
    for pos in range(1,6):
        selectInfo(pos,artworks,listbyPrice,catalog,True,False,False)

    sortArtYears(artworks)
    for pos in range(1,6):
        selectInfo(pos,artworks,listbyDate,catalog,True,False,False)


    headers = ['ObjectID','Title','Artist(s)','Medium','Dimensions','Date','TransCost','Classification','URL']

    tablePrice = tabulate(listbyPrice, headers=headers, tablefmt='grid',numalign='center')

    tableDates = tabulate(listbyDate, headers=headers, tablefmt='grid',numalign='center')

    return (lt.size(artworks),round(estimado_peso,3),round(precio,3),tablePrice,tableDates)
#Termina el Req 5


# Req 6
#TODO retornar todos los valores que piden en el pdf
def Proli(begin,end,cant_artists ,catalog):
    dataArtists = catalog['artists']
    artist_list = mp.keySet(catalog['artworksArtists'])
    artworksArtist = catalog['artworksArtists']
    listArtworksEnd=[]
    listArtistsEnd=[]

    completeArtists=lt.newList('ARRAY_LIST')

    for artist in lt.iterator (artist_list):
        data = mp.get(dataArtists,artist)['value']
   
        if int(data['BeginDate']) in range(begin,end+1): 
           
            tecnica_mayor = None
            cant_mayor = 0
            tecnicas = mp.newMap(numelements=2,maptype='CHAINING',loadfactor=0.8)
            
            obras = mp.get(artworksArtist, artist)['value']
            cant_obras = lt.size(obras)

            for obra in lt.iterator(obras):
                tecnica = obra['Medium']
                if mp.contains(tecnicas,tecnica):
                    cantidad = mp.get(tecnicas,tecnica)['value']+1
                else:
                    cantidad = 1
                if cantidad > cant_mayor:
                    tecnica_mayor = tecnica 
                    cant_mayor=cantidad
                mp.put(tecnicas,tecnica,cantidad)

            cant_mediums = mp.size(tecnicas)

            data['tecnicaMayor'] = tecnica_mayor
            data['cant_obras'] = cant_obras
            data['cant_mediums'] = cant_mediums

            lt.addLast(completeArtists,data)

    sortArtistsArtworks(completeArtists)

    #AQUÍ COMIENZA LA PARTE 2 DEL BONO
    filteredArtworks=lt.newList('ARRAY_LIST')
    most_prolific_name = lt.firstElement(completeArtists)['DisplayName']
    most_prolific_id = lt.firstElement(completeArtists)['ConstituentID']
    bestArtist_maxMedium = lt.firstElement(completeArtists)['tecnicaMayor']
    artbestartist = mp.get(artworksArtist,most_prolific_id)['value']
    artcantBest=lt.size(mp.get(artworksArtist,most_prolific_id)['value'])
    for artwork in lt.iterator(artbestartist):
        if artwork['Medium'] == bestArtist_maxMedium and type(artwork['DateAcquired'])is str:
            lt.addLast(filteredArtworks,artwork)


    sortArtworksDates_op2(filteredArtworks)

    for pos in range(1,6):
        selectInfo(pos,filteredArtworks,listArtworksEnd,catalog,False,False,True)
    headers = ['ObjectID','Title','Artist(s)','Medium','Date','Dimensions','DateAcquired','Department','URL']
    table = tabulate(listArtworksEnd, headers=headers, tablefmt='grid',numalign='center')  

    for pos in range(1,cant_artists):
        selectArtist(pos,completeArtists,listArtistsEnd,True)
    headersArtists = ['ConstituentID','DisplayName','BeginDate','Gender','ArtistBio','Wiki QID','ULAN','Artwork Number','Medium Number','Top medium']
    table_artists = tabulate(listArtistsEnd,headers=headersArtists,tablefmt='grid')
    
    return (lt.size(completeArtists),table_artists, most_prolific_name,most_prolific_id,artcantBest,table)
#↑↑↑Termina el Req 6↑↑↑




#↓↓↓Esto de acá es para el formatting de las tablas ↓↓↓
def distribuir(elemento,cantidad):
    str_distribuido = '\n'.join((textwrap.wrap(elemento,cantidad)))
    return str_distribuido

def chkUnknown(origen,clave):
    if origen[clave]==None or origen[clave]=='' or origen[clave]==5000 or origen[clave]=='2100-12-24': return 'Unknown' #El 5000 se pone para compensar una de las funciones de comparación de años.
    else: return origen[clave]

def selectArtist(position,ArtistList,lstArtistEnd,isbonus:bool):

    artist = lt.getElement(ArtistList,position)
    ConstID = artist['ConstituentID']
    name=distribuir(artist['DisplayName'],15)

    bgndate=chkUnknown(artist,'BeginDate')
    nationality=chkUnknown(artist,'Nationality')
    gender=chkUnknown(artist,'Gender')
    bio=distribuir(chkUnknown(artist,'ArtistBio'),15)
    qid=distribuir(chkUnknown(artist,'Wiki QID'),10)
    ulan = chkUnknown(artist,'ULAN')
    if isbonus:
        artnum=chkUnknown(artist,'cant_obras')
        medNum=chkUnknown(artist,'cant_mediums')
        topMed=((artist['tecnicaMayor']))
        artistInfo=[ConstID,name,bgndate,gender,bio,qid,ulan,artnum,medNum,topMed]
    else: artistInfo=[ConstID,name,bgndate,nationality,gender,bio,qid,ulan]
    lstArtistEnd.append(artistInfo)

def selectInfo(position,ListArtworks,FilteredList,catalog,prices:bool,areas:bool,dateAcq:bool):
#       ↓↓↓ Todo este montón de líneas se encargan de sacar la info. necesaria del diccionario grande y con textwrap lo separa en líneas de un igual tamaño.
        artwork = lt.getElement(ListArtworks,position)

        objectID = artwork['ObjectID']
        title=distribuir(chkUnknown(artwork,'Title'),10)
        date=distribuir(chkUnknown(artwork,'Date'),10)
        medium=distribuir(chkUnknown(artwork,'Medium'),20)
        dimensions=distribuir(chkUnknown(artwork,'Dimensions'),20)
        department=distribuir(chkUnknown(artwork,'Department'),15)
        classification=distribuir(chkUnknown(artwork,'Classification'),15)
        url = distribuir(chkUnknown(artwork,'URL'),15)
        
#       Aquí se recorren internamente los artistas que tenga cada obra para luego buscarlos en el archivo artists y sacar sus nombres.
        artists = ""
        idArtist = artwork['ConstituentID'].replace('[','').replace(']','').split(',') #Hago lo de artwork['ConstituentID'].replace('[','').replace(']','') para quitarle los corchetes []
        for AuthorID in idArtist:
            AuthorID=AuthorID.strip() #Strip quita espacios innecesarios
            if mp.contains(catalog['artists'],AuthorID):
                artist = (mp.get(catalog['artists'],AuthorID)['value'])['DisplayName']


#           Este if solo es para separar por comas si hay varios artistas, para no iniciar con coma si está vacío.
            if artists=="":
                artists+=artist
            else:
                artists+=", "+artist
#       Se vuelve a hacer lo de antes para separar con una cantidad exacta de lineas.
        if artists==None or artists=='':
            artists='Unknown'
        artists=distribuir(artists,15)

#       Se crea una lista con todo lo que pide el requerimiento.

        artwork_entrega = [objectID,title,artists,medium,dimensions,date,
                   department,classification,url]
        if prices:
            price = chkUnknown(artwork,'Price')
            artwork_entrega = [objectID,title,artists,medium,dimensions,date,
                             price,classification,url]
        if areas:
            area = chkUnknown(artwork,'Area')
            artwork_entrega = [objectID,title,artists,medium,dimensions,date,department,
                                area,classification,url]
        if dateAcq:
            dateAcquired = distribuir(chkUnknown(artwork,'DateAcquired'),15)
            artwork_entrega = [objectID,title,artists,medium,date,dimensions,dateAcquired,
                                department,classification,url]
#       Se pone un nuevo registro con la info de cada obra en la lista grande declarada al inicio.
        FilteredList.append(artwork_entrega)
#↑↑↑ Termina el formatting de las tablas ↑↑↑
