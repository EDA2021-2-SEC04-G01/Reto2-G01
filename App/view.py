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
    print("2- las n obras más antiguas para un medio específico")
def initCatalog(tipo_lista):
    
    return controller.initCatalog(tipo_lista)
catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        catalog = initCatalog('ARRAY_LIST')
        controller.loadData(catalog)
        print("Cargando información de los archivos ....")

    elif int(inputs[0]) == 2:
        medium = input("Escriba un medio: ")
        cant = int(input("Escriba una cantidad: "))
        print(controller.masAntiguos(catalog,medium,cant))
        

    elif int(inputs[0]) == 4:
        print(model.ordenNacionalidad(catalog)[0])
        print(model.ordenNacionalidad(catalog)[1])

    elif int(inputs[0]) == 0:
        # print(mp.keySet(catalog['nationalities']))
        for key in lt.iterator(mp.keySet(catalog['nationalities'])):
            print(key,lt.size(mp.get(catalog['nationalities'],key)['value']))
        

    else:
        sys.exit(0)
sys.exit(0)
