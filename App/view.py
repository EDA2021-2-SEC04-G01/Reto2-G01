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
    print("2- las n obras más antiguas para un medio específico.")
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

    elif int(inputs[0]) == 2:
        medium = input("Escriba un medio: ")
        cant = int(input("Escriba una cantidad: "))
        print(controller.masAntiguos(catalog,medium,cant))
        

    elif int(inputs[0]) == 5:
        print(model.ordenNacionalidad(catalog)[0])
        print(model.ordenNacionalidad(catalog)[1])


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

    elif int(inputs[0]) == 7:
        print(mp.valueSet(catalog['artworksArtists']))

    elif int(inputs[0]) == 9:
        nation = input("Escriba una nacionalidad: ")
        cantidad = controller.cantNationality(catalog,nation)
        print("La cantidad de obras para la nacionalidad {} es {}.".format(nation,cantidad))

    elif int(inputs[0]) == 0:
        print(model.cronoArtist(catalog,1920,1985))
        # print('\n')
        # for i in lt.iterator(mp.keySet(catalog['dateArtists'])):
        #     print(i)
        # # print(mp.keySet(catalog['nationalities']))
        # for key in lt.iterator(mp.keySet(catalog['nationalities'])):
        #     print(key,lt.size(mp.get(catalog['nationalities'],key)['value']))
        

    else:
        sys.exit(0)
sys.exit(0)
