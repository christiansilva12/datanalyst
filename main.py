import pandas as pd
import requests 
import csv
import rutas
import os
from datetime import date
from rutas import conn
import psycopg2
import numpy as np
import psycopg2.extras as extras
from ej import carga,crear_tablas



# Extraccion

""""Descarga de datos"""

SalaCine=requests.get(rutas.salacine_url)
Museo=requests.get(rutas.museo_url)
Biblioteca=requests.get(rutas.bib_url)

"""conversion a csv"""

SalaCine_csv= csv.reader(
    SalaCine.content.decode('utf-8').splitlines(), delimiter=','
)

Museo_csv= csv.reader(
    Museo.content.decode('utf-8').splitlines(), delimiter=','
)

Biblioteca_csv= csv.reader(
    Biblioteca.content.decode('utf-8').splitlines(), delimiter=','
)


"""convertir en dataframes de pandas, para mejor manejo"""
df_cine = pd.DataFrame(SalaCine_csv)
df_museo = pd.DataFrame(Museo_csv)
df_bib = pd.DataFrame(Biblioteca_csv)



"""Colocamos como nombre de columna la primera fila y borramos el duplicado"""
df_cine=df_cine.set_axis(df_cine.iloc[0], axis = 1)
df_cine=df_cine.drop(0 , axis = 0)





df_museo = df_museo.set_axis(df_museo.iloc[0], axis = 1)
df_museo = df_museo.drop(0 , axis = 0)

df_bib = df_bib.set_axis(df_bib.iloc[0], axis = 1)
df_bib = df_bib.drop(0 , axis = 0)

"""listas para iterar y fecha de hoy"""

categoria = ["cines","museos","bibliotecas_populares"]
datos = [df_cine, df_museo, df_bib]
today = date.today()


"""Creamos las carpetas y colocamos los archivos en los mismos"""
for i in range(0,3):
    os.makedirs(
        "data/{i}/{anio}-{mes}".format(
            i = categoria[i] , anio = today.strftime("%Y"), mes = today.strftime("%B")
            ),
         exist_ok=True
         )

    df_bib.to_excel(    #creo que va datos.to_excel#
        "data/{i}/{anio}-{mes}/{i}-{nombre}.xlsx".format(
        i = categoria[i] , anio = today.strftime("%Y"), mes = today.strftime("%B") , nombre = today.strftime("%d-%m-%Y")
        )
        )

datos[0]=datos[0].rename(columns={"categoria":"Categoria","Dirección":"Domicilio","Teléfono":"Telefono","id_departamento":"IdDepartamento"})
print (datos[0])

datos[1]=datos[1].rename(columns={"categoria":"Categoria","provincia":"Provincia",
"localidad":"Localidad","nombre":"Nombre","direccion":"Domicilio","telefono":"Telefono",
"Cod_Loc":"cod_localidad",
 "IdProvincia":"id_provincia"})
#print (datos[1])


datos[2]=datos[2].rename(columns={"categoria":"Categoria","Teléfono":"Telefono"})
#print (datos[2])

#print(datos, "then")

df_principal=pd.concat( datos, ignore_index=True, join="inner")


print(df_principal.columns.to_list())

"""
Podemos ver que hay algunas columnas de mas con
print(df_principal.columns.to_list())
Entonces eliminamos las que sobran
"""
df_principal=df_principal.drop(columns=['piso',  'fuente'
                                        ])

""" 
Ahora creamos la otra
Procesar la información de cines para poder crear una tabla que contenga:
o Provincia
o Cantidad de pantallas
o Cantidad de butacas
o Cantidad de espacios INCAA
Podemos ver las columnas con
print(df_cine.columns.to_list())
"""
#print(df_cine.columns.to_list())

df_cine_principal=df_cine[["provincia","pantallas","butacas","espacio_incaa"]]
df_cine_principal=df_cine_principal.rename(columns={"Pantallas":"pantallas","Butacas":"butacas","espacio_INCAA":"espacio_incaa"})

"""Ingresamos los datos de la fecha en los dataframe"""
df_cine_principal["upload_date"]=today.strftime("%Y-%m-%d")
df_principal["upload_date"]=today.strftime("%Y-%m-%d")

#----------------Carga a base de datos------------------
crear_tablas()
carga(conn,df_principal,"principal")
carga(conn,df_cine_principal,"cine_tabla")



