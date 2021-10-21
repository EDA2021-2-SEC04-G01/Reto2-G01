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
 """

from App.model import ordenNacionalidad
import config as cf
import model
import csv

def initCatalog():
    catalog = model.newCatalog()
    return catalog


def loadData(catalog):
    loadArtists(catalog)
    loadArtworks(catalog)


def loadArtists(catalog):
    artistFile=cf.data_dir+"Artists-utf8-large.csv"
    input_file = csv.DictReader(open(artistFile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog,artist)
        model.addDate(catalog,artist)
        

        

def loadArtworks(catalog):
    artworkFile=cf.data_dir+"Artworks-utf8-large.csv"
    input_file = csv.DictReader(open(artworkFile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog,artwork)
        model.addMedium(catalog,artwork)
        model.addNation(catalog,artwork)
        model.addArtworksArtist(catalog,artwork)
        model.addToDpto(catalog,artwork)
        model.addArtworkbyDate(catalog,artwork)
        model.addartistName(catalog,artwork)



# Funciones de ordenamiento

# def sortDates(catalog):
#     model.sortDates(catalog)

def sortArtDates(catalog,cant,method):
    return model.sortArtworksDates(catalog,cant,method)

def masAntiguos(catalog,medium,cant):
    return model.masAntiguos(catalog,medium,cant)

def cantNationality(catalog,nation):
    return model.cantNationality(catalog,nation)

def precioTransporte(catalog,department):
    return model.precioTransporte(catalog,department)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def cronoArtworks(catalog,inicio,fin):
    #Ordenamos aquí y no al inicio con lo demás para no alterar el resultado del requerimiento 4.
    return(model.cronoArtwork(catalog,inicio,fin))

def ordenNacionalidad(catalog):
    return (model.ordenNacionalidad(catalog))

def cronoArtist(catalog,inicio,fin):
    return model.cronoArtist(catalog,inicio,fin)

def artistPerTecnique(nombre,catalog):
    return model.buscarArtista(nombre,catalog)

def proli(begin,end,cant_artists,catalog):
    return model.Proli(begin,end,cant_artists,catalog)