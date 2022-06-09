# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:47:11 2022

@author: jm.rivera@uniandes.edu.co
"""

import os
import pandas as pd
hembras=False
if hembras:
    base="D:/Users/USER/OneDrive - Universidad de los Andes/REGISTRO APRENDIZAJE/HEMBRAS/"
else:
    base="D:/Users/USER/OneDrive - Universidad de los Andes/REGISTRO APRENDIZAJE/MACHOS/"


def listaDeRegistros(base):
    """

    Parameters:
    base (str): dirección de base donde se buscarán los archivos que haya presentes

    Returns:
    registros (Array of str): lista de registros presentes en la carpeta

   """
    registros=[]
    for i in os.listdir(base):
        if os.path.isdir(base+i):
            registros+=listaDeRegistros(base+i+"/")
        elif os.path.isfile(base+i):
            registros.append(i)
    return registros

def listaDeAnimales(registros):
    """

    Parameters:
    registros (Array of str): lista de registros

    Returns:
    data (Pandas dataframe): dataframe de pandas con las columnas indicadas

   """
    if hembras:
        sexChar='H'
    else:
        sexChar='M'
   
    dia=[]
    mes=[]
    año=[]
    sexo=[]
    caja=[]
    marca=[]
    tipoPrueba=[]
    diaEnsayo=[]
    bloque=[]
    nombreArchivo=[]
    for registro in registros:
        try:
            # Ejemplo de registro '3.12.2021.H_C21_5_REV_AZ_D8_B1.docx'
            temp=registro.split(".")
            dia.append(int(temp[0]))
            mes.append(int(temp[1]))
            año.append(int(temp[2]))
            temp1=temp[3].strip().split('_')
            temp2=[]
            for i in temp1:
                temp2+=i.split(' ')
            temp1=temp2.copy()
                
            incluyeSexo=0
            if temp1[0].find(sexChar)==-1:
                incluyeSexo=1
                sexo.append(sexChar)
            else:
                sexo.append(temp1[0])
            marca.append(int(temp1[2-incluyeSexo]))
            
            indicadorCaja=temp1[1-incluyeSexo].find('C')
            if indicadorCaja==-1:
                print("Error en registro: "+registro)
            else:
                numCaja=temp1[1-incluyeSexo][indicadorCaja+1:]
                caja.append(numCaja)
            
            indicadorBloque=temp1[-1:][0].find('B')
            if indicadorBloque==-1:
                print("Error en registro: "+registro)
            else:
                bloque.append(int(temp1[-1:][0][indicadorBloque+1:]))
            
            indicadorDia=temp1[-2:-1][0].find('D')
            if indicadorDia==-1:
                print("Error en registro: "+registro)
            else:
                diaEnsayo.append(temp1[-2:-1][0][indicadorDia+1:])
            
            tipo=''
            for i in temp1[3-incluyeSexo:len(temp1)-2]:
                tipo+=(i+'_')
            tipoPrueba.append(tipo[:-1])
            nombreArchivo.append(registro)
            
        except:
            print(registro)
    d={'dia':dia, 'mes':mes, 'año':año, 'sexo':sexo, 'caja':caja,
       'marca':marca, 'tipoPrueba':tipoPrueba, 'diaEnsayo':diaEnsayo,
       'bloque':bloque, "nombreArchivo":nombreArchivo}
    data=pd.DataFrame(data=d)
    return data

print(listaDeAnimales(listaDeRegistros(base)))