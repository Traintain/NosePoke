# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 12:47:11 2022

@author: jm.rivera@uniandes.edu.co
"""

import os
import pandas as pd

def listaDeRegistros(base):
    """
    Toma una ubicación y realiza un proceso iterativo buscando en todos los 
    archivos que se encuentren almacenados
    
    Parameters:
    base (str): dirección del directorio base donde se buscarán los archivos que
    haya presentes

    Returns:
    registros (Array of str): lista de registros presentes en la carpeta

   """
    registros=[]
    for i in os.listdir(base):
        if os.path.isdir(base+i):
            registros+=listaDeRegistros(base+i+"/")
        elif os.path.isfile(base+i):
            registros.append(base+i)
    return registros

def listaDeAnimales(registros):
    """
    Toma el nombre de archivo de un registro y la divide, extrayendo los datos
    correspondientes, asumiendo que cumple con la convención de formato
    [DD].[MM].[AAAA].[Sex]_C[#Caja]_[#Animal]_[IdPrueba]_D[#dia]_B[#Bloque].[optional].docx
    
    Parameters:
    registros (Array of str): lista de registros

    Returns:
    data (Pandas dataframe): dataframe de pandas con los datos de cada registro
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
            temp=registro.split("/")[-1:][0].split(".")
            # '3' '12' '2021'
            dia.append(int(temp[0]))
            mes.append(int(temp[1]))
            año.append(int(temp[2]))
            # 'H_C21_5_REV_AZ_D8_B1'
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
                print("Error al leer el identificador de caja: "+registro)
                caja.append(None)
            else:
                numCaja=temp1[1-incluyeSexo][indicadorCaja+1:]
                caja.append(numCaja)
            

            indicadorBloque=temp1[-1:][0].find('B')
                
            if indicadorBloque==-1:
                print("Error al leer el identificador del bloque: "+registro)
                bloque.append(None)
            else:
                bloque.append(int(temp1[-1:][0][indicadorBloque+1:]))
            
            indicadorDia=temp1[-2:-1][0].find('D')
            if indicadorDia==-1:
                print("Error al leer el identificador del día: "+registro)
                diaEnsayo.append(None)
            else:
                diaEnsayo.append(temp1[-2:-1][0][indicadorDia+1:])
            
            tipo=''
            for i in temp1[3-incluyeSexo:len(temp1)-2]:
                tipo+=(i+'_')
            tipoPrueba.append(tipo[:-1])
            nombreArchivo.append(registro)
            
        except:
            (registro)
    d={'dia':dia, 'mes':mes, 'año':año, 'sexo':sexo, 'caja':caja,
       'marca':marca, 'tipoPrueba':tipoPrueba, 'diaEnsayo':diaEnsayo,
       'bloque':bloque, "nombreArchivo":nombreArchivo}
    data=pd.DataFrame(data=d)
    return data

def estandarizarTerminosTipoDePrueba(data):
    """
    Se tienen variaciones del identificador usado para los 7 tipos de prueba
    que se realizaron. Este método unifica los diferentes términos usados
    
    Parameters:
    data (Pandas dataframe): dataframe de pandas con los datos de cada registro

    Returns:
    cleanData (Pandas dataframe): dataframe de pandas con los términos unificados para la columna tipoPrueba
    """
    cleanData=data.copy()
    replaceDict={"_HAB":"HAB",
                 "P_DER":"SM_ADQ_DER", "SM_P_DER":"SM_ADQ_DER",
                 "SM_PRE_DER":"SM_ADQ_DER", "SM_ADQ_DER_":"SM_ADQ_DER","SM_DER_ADQ":"SM_ADQ_DER",
                 "SMM_ADQ_DER":"SM_ADQ_DER",
                 "P_IZQ":"SM_ADQ_IZQ","SM_P_IZQ":"SM_ADQ_IZQ","SM_IZQ_ADQ":"SM_ADQ_IZQ",
                 "SM_IZQ":"SM_ADQ_IZQ","SM_PRE_IZQ":"SM_ADQ_IZQ",
                 
                 "R_DER":"SM_REV_DER","SM_R_DER":"SM_REV_DER",
                 "R_IZQ":"SM_REV_IZQ","SM_R_IZQ":"SM_REV_IZQ",
                 
                 "DIS":"RA_ADQ", "DIS_AZ":"RA_ADQ", "ADQ_AZ":"RA_ADQ",
                 
                 "REV_AZ":"RA_REV", "RA":"RA_REV", "REV":"RA_REV", "R_AZ":"RA_REV",
                 }
    cleanData['tipoPrueba'].replace(to_replace=replaceDict, inplace=True)
    return cleanData

#-------------------------Extraer los datos------------------------------------
for i in range(2):
    hembras= (i%2==0)
    if hembras:
        base="D:/Users/USER/OneDrive - Universidad de los Andes/REGISTRO APRENDIZAJE/HEMBRAS/"
        nombreSalida='registrosHembras.xlsx'
    else:
        base="D:/Users/USER/OneDrive - Universidad de los Andes/REGISTRO APRENDIZAJE/MACHOS/"
        nombreSalida='registrosMachos.xlsx'

    # (listaDeAnimales(listaDeRegistros(base)))
    # Se extrae la información a un archivo de Excel
    estandarizarTerminosTipoDePrueba(listaDeAnimales(listaDeRegistros(base))).to_excel(nombreSalida)

registrosMachos=pd.read_excel("registrosMachos.xlsx", index_col=0)
registrosHembras=pd.read_excel("registrosHembras.xlsx", index_col=0)
registros=pd.concat([registrosMachos, registrosHembras], ignore_index=True)
registros['IdAnimal']=registros['sexo']+"-"+registros['caja']+"-"+registros.marca.map(str)
registros.to_excel("registrosMachosYHembras.xlsx")