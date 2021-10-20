"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """


import config as cf
import sys
import controller
import model
from DISClib.ADT import list as lt
assert cf
from DISClib.ADT import map as mp
import sys
import time
sys.setrecursionlimit(5000)
"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar artistas cronológicamente en un rango de años")
    print("3- Listar adquisiciones cronológicamente\n")
    print("5- Clasificar obras por nacionalidad de sus creadores")
    print("6- Calcular costo de transporte de todas las obras a un departamento\n")
    print("8- las n obras más antiguas para un medio específico.")
    print("9- Cantidad de obras para una nacionalidad específica.")
def initCatalog():
    
    return controller.initCatalog()
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        start_time = time.process_time()
        catalog = initCatalog()
        controller.loadData(catalog)
        print("Cargando información de los archivos ....")

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)    

#Requerimiento 1
    elif int(inputs[0]) == 2:
        
        start_time = time.process_time()
        inicio=int(input("Escriba el año de inicio: "))
        fin=int(input("Escriba el año final: "))
        print("================= Req No. 1 Inputs ==================")
        print("\nArtist born between {} and {}.\n".format(inicio,fin))
        resultados= controller.cronoArtist(catalog,inicio,fin)
        if  "No hay" in resultados :
            print(resultados+"\n")
            break
        tabla=resultados[0]
        cantArtists = resultados[1]
        print("================= Req No. 1 Answer ==================\n")
        print("There are {0} artist born between {1} and {2}\n\n".format(cantArtists,inicio,fin))
        print("The first and last 3 artists in range are...\n")
        print(tabla)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

##Requerimiento 2
    elif int(inputs[0]) == 3:
        start_time = time.process_time()
        inicio=(input("Escriba la fecha de inicio: "))
        fin=(input("Escriba la fecha final: "))
        resultado = controller.cronoArtworks(catalog,inicio,fin)
        tabla = resultado[0]
        cantObras = resultado[1]
        cantCompradas = resultado[2]
        cantArtists = resultado[3]
        print("=================== Req No. 2 Inputs =====================\n")
        print("Artworks acquired between {0} and {1}".format(inicio,fin))
        print("=================== Req No. 2 Answer =====================\n\n")
        print("The MoMA acquired {0} unique pieces between {1} and {2}\n".format(str(cantObras),inicio,fin))
        print("With {0} different artists and purchased {1} of them.\n\nThe first and last 3 artworks in the range are... ".format(cantArtists,cantCompradas))
        print(tabla)

        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print("El tiempo usado completo fue"+str(elapsed_time_mseg))

#Requerimiento 3


#Requerimiento 4
    elif int(inputs[0]) == 5:
        start_time = time.process_time()
        print("=================Req No. 4 Inputs ====================\n ")
        print("Ranking countries by their number of Artworks in the MoMA...\n")
        resultados = controller.ordenNacionalidad(catalog)
        print("\n--------------- Req No. 4 Answer -----------------\n")
        print("The TOP 10 Countries in the MoMA are: ")
        topNation=(resultados[0])
        tablaOrden = resultados[1]
        nameMajor = resultados[2]
        cantMajor = resultados[3]
        print(topNation)
        print("The TOP nacionality in the museum is: {0} with {1} unique pieces.\nThe first and last 3 objects in the {0} artwork list are: ".format(nameMajor,str(cantMajor)))
        print(tablaOrden)
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)
        

#Requerimiento 5
    elif int(inputs[0]) == 6:
        start_time = time.process_time()
        dpto=input("Escriba el departamento del museo: ")
        print("\n=================Req No. 5 Inputs ====================\n ")
        print("Estimate the cost to transport all artifacts in {} MoMA's Departament . . .\n".format(dpto))
        rta=controller.precioTransporte(catalog,dpto)
        print("================ Req No. 5 Answer ================\n")
        print("The MoMA is going to transport {0} artifacts from the {1} department. ".format(rta[0],dpto))
        print("REMEMBER!, NOT all MoMA's data is complete! ! !... These are estimates.  ")
        print("Estimated cargo weight (kg): "+str(rta[1]))
        print("Estimated cargo cost (USD): "+str(rta[2]))
        print("\nThe TOP 5 most expensive items to transport are:")
        print(controller.precioTransporte(catalog,dpto)[3])
        print("\nThe TOP 5 oldest items to tranport are: ")
        print(controller.precioTransporte(catalog,dpto)[4])
        stop_time = time.process_time()
        elapsed_time_mseg = (stop_time - start_time)*1000
        print(elapsed_time_mseg)

#Requerimiento 6 (BONO)
    elif int(inputs[0]) == 7:
        print(mp.valueSet(catalog['artworksArtists']))

#Cosas de los laboratorios
    elif int(inputs[0]) == 8:
        medium = input("Escriba un medio: ")
        cant = int(input("Escriba una cantidad: "))
        print(controller.masAntiguos(catalog,medium,cant))

    
    elif int(inputs[0]) == 9:
        nation = input("Escriba una nacionalidad: ")
        cantidad = controller.cantNationality(catalog,nation)
        print("La cantidad de obras para la nacionalidad {} es {}.".format(nation,cantidad))

    elif int(inputs[0]) == 0:
        (model.Proli(1914,1939,7,catalog))
        # print(model.buscarArtista('Louise Bourgeois',catalog))
        #Aquí es para probar nada más
        pass

    else:
        sys.exit(0)
sys.exit(0)
