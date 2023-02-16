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

def listaDeAnimales(registros, sexChar):
    """
    Toma el nombre de archivo de un registro y la divide, extrayendo los datos
    correspondientes, asumiendo que cumple con la convención de formato
    [DD].[MM].[AAAA].[Sex]_C[#Caja]_[#Animal]_[IdPrueba]_D[#dia]_B[#Bloque].[optional].docx
    
    Parameters:
    registros (Array of str): lista de registros
    sexo (Char): Caracter que puede ser 'H' para hembras y 'M' para machos

    Returns:
    data (Pandas dataframe): dataframe de pandas con los datos de cada registro
   """
   
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
    etiqueta=[]
    
    for registro in registros:
        try:
            # Ejemplo de registro '3.12.2021.H_C21_5_REV_AZ_D8_B1.docx'
            direccion=registro.split("/")[-1:][0].split(".")
            
            # '3' '12' '2021'
            dia.append(int(direccion[0]))
            mes.append(int(direccion[1]))
            año.append(int(direccion[2]))
            
            # 'H_C21_5_REV_AZ_D8_B1'
            metadata=[]
            for i in direccion[3].split('_'):
                i = i.strip()
                if ' ' in i.strip():
                    for j in i.split(' '):
                        if j!='':
                            metadata.append(j)
                else:
                    metadata.append(i)
                        
            
            if sexChar in metadata[0]:
                sexo.append(metadata.pop(0).strip())
            else:
                sexo.append(sexChar)
                # print("Error al leer el sexo del animal: "+registro)
                
            if 'C' in metadata[0]:
                caja.append(metadata.pop(0).strip()[1:])
            else:
                caja.append(-1)
                print("Error al leer el identificador de la caja: "+registro)
                
            try:
                int(metadata[0])
                marca.append(metadata.pop(0).strip())
            except:
                marca.append(-1)
                print("Error al leer el numero del animal: "+registro)
                
            if 'B' in metadata[-1]:
                bloque.append(metadata.pop().strip()[1:])
            else:
                bloque.append(-1)
                print("Error al leer el bloque: "+registro)
                
            if 'D' in metadata[-1]:
                diaEnsayo.append(metadata.pop().strip()[1:])
            else:
                diaEnsayo.append(-1)
                print("Error al leer el bloque: "+registro)
            
            tipo=""
            for i in metadata:
                tipo+=(i.strip()+'_')
            tipoPrueba.append(tipo.strip()[:-1])
            
            if len(direccion)==6:
                etiqueta.append(direccion[4])
            else:
                etiqueta.append('')
            
            nombreArchivo.append(registro)
            
        except:
            print("Error adicional: "+registro)
    d={'dia':dia, 'mes':mes, 'año':año, 'sexo':sexo, 'caja':caja,
       'marca':marca, 'tipoPrueba':tipoPrueba, 'diaEnsayo':diaEnsayo,
       'bloque':bloque, "nombreArchivo":nombreArchivo, 'etiqueta':etiqueta}
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
# Se recorre el directorio de las hembras
base="D:/Users/USER/OneDrive - Universidad de los Andes/REGISTRO APRENDIZAJE/HEMBRAS/"
nombreSalida='registrosHembras.xlsx'
estandarizarTerminosTipoDePrueba(listaDeAnimales(listaDeRegistros(base), 'H')).to_excel(nombreSalida)

# Se recorre el directorio de los machos
base="D:/Users/USER/OneDrive - Universidad de los Andes/REGISTRO APRENDIZAJE/MACHOS/"
nombreSalida='registrosMachos.xlsx'
estandarizarTerminosTipoDePrueba(listaDeAnimales(listaDeRegistros(base), 'M')).to_excel(nombreSalida)

# Se exporta la información a archivos de Excel, uno para hembras, uno para machos y una unión de ambos
registrosMachos=pd.read_excel("registrosMachos.xlsx", index_col=0)
registrosHembras=pd.read_excel("registrosHembras.xlsx", index_col=0)
registros=pd.concat([registrosMachos, registrosHembras], ignore_index=True)
registros['IdAnimal']=registros.apply(lambda fila: f"{fila.sexo}-{fila.caja}-{fila.marca}", axis=1)
registros.to_excel("registrosMachosYHembras.xlsx")