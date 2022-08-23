# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:52:48 2022

@author: jm.rivera@uniandes.edu.co
"""

import os
import pandas as pd
import docx2txt
from datetime import datetime

registros=pd.read_excel("registrosMachosYHembras.xlsx", index_col=0)


def extraerDatosHabituacion(texto, fileName,logFile, diaEnsayo, bloque):
    """
    Se carga el registro de cada animal en formato de texto y se realiza la 
    extracción de datos
    
    Parameters:
    texto (String): Cadena de texto con los datos del ensayo
    fileName (String): dirección del archivo de registro
    logFile (File): archivo donde se escriben los errores de ejecución
    diaEnsayo (Int): día del ensyo en que se tomaron los datos
    bloque (Int): bloque dentro del día en que se tomaron los datos

    Returns:
    dataDict (Dictionary): diccionario con los datos del ensayo
    """
    # Se divide la cadena de texto por cada línea en un array
    texto=texto.split('\n')
    texto= list(filter(None, texto))
    
    dataDict={"Dirección":fileName, "Tipo de prueba": "Habituación", "Día":diaEnsayo, "Bloque": bloque}
    horaInicio=""
    inicioLogged=True
    horaFin=""
    i=0
    # Si el archivo está vacío genera un error
    if len(texto)==0:
        logFile.write(fileName +", Archivo vacío\n")
    else:
        while i < len(texto):
            linea=texto[i]
            # Cada línea se espera que tenga la siguiente estructura "12:20:12.886 -> Transmitiendo"
            if len(linea.split('->'))==2:
                hora=linea.split('->')[0]
                registro=linea.split('->')[1]
                if registro.find("Van a empezar los 50 ensayos")>-1 or inicioLogged:
                    horaInicio=datetime.strptime(hora.split('.')[0],"%H:%M:%S")
                    inicioLogged=False
                elif registro.find("El lado preferente es el")>-1 :
                    horaFin=datetime.strptime(hora.split('.')[0],"%H:%M:%S")
                elif len(registro.split(','))==11 and registro.split(',')[0].find("Ensayo")==-1:
                    datos=registro.split(',')
                    # Solo se toman los registros del ensayo 15, 35 y 50
                    if float(datos[0])==15 or float(datos[0])==35 or float(datos[0])==50:
                        dataDict["Aciertos_"+datos[0]]=[float(datos[1])]
                        dataDict["PorcentajeAciertos_"+datos[0]]=[((float(datos[1])/float(datos[0]))*100)]
                        dataDict["TiempoRespuestasImpulsivas_"+datos[0]]=[datos[3]]
                        dataDict["Omisiones_"+datos[0]]=[float(datos[4])]
                        dataDict["PorcentajeOmisiones_"+datos[0]]=[((float(datos[4])/float(datos[0]))*100)]
                        dataDict["Categorias_"+datos[0]]=[float(datos[6])]
                        dataDict["CorrectasDerecha_"+datos[0]]=[float(datos[7])]
                        dataDict["CorrectasIzquierda_"+datos[0]]=[float(datos[8])]
                        dataDict["LatenciaPromedio_"+datos[0]]=[datos[9]]
                        dataDict["MaximoAciertosSeguidos_"+datos[0]]=[float(datos[10])]
                elif registro.find("Ensayo numero:")>-1 and (registro.find("15")>-1 or registro.find("35")>-1 or registro.find("50")>-1):
                    numReg=float(registro.split(':')[1])
                    while True:
                        if registro.find("Aciertos")>-1:
                            break
                        else:
                            i+=1
                            linea=texto[i]
                            registro=linea.split('->')[1]
                    dataDict["Aciertos_"+str(numReg)]=[float(registro.split(':')[1])]
                    dataDict["PorcentajeAciertos_"+str(numReg)]=[((float(registro.split(':')[1])/numReg)*100)]
                    i+=2
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["TiempoRespuestasImpulsivas_"+str(numReg)]=[registro.split(':')[1]]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["Omisiones_"+str(numReg)]=[float(registro.split(':')[1])]
                    dataDict["PorcentajeOmisiones_"+str(numReg)]=[((float(registro.split(':')[1])/numReg)*100)]
                    i+=2
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["Categorias_"+str(numReg)]=[float(registro.split(':')[1])]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["CorrectasDerecha_"+str(numReg)]=[float(registro.split(':')[1])]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["CorrectasIzquierda_"+str(numReg)]=[float(registro.split(':')[1])]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["LatenciaPromedio_"+str(numReg)]=[registro.split(':')[1]]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["MaximoAciertosSeguidos_"+str(numReg)]=[float(registro.split(':')[1])]
                
            i+=1
        
        try:
            dataDict["segundosTotales"]=[(horaFin-horaInicio).total_seconds()]
        except:
            dataDict["segundosTotales"]=[-1]
            logFile.write(fileName +", No se puede calcular el tiempo total del experimento\n")
    return dataDict

def extraerDatosSeriesMotorasAdquisicion(texto, fileName,logFile, diaEnsayo, bloque):
    """
    Se carga el registro de cada animal en formato de texto y se realiza la 
    extracción de datos
    
    Parameters:
    texto (String): Cadena de texto con los datos del ensayo
    fileName (String): dirección del archivo de registro
    logFile (File): archivo donde se escriben los errores de ejecución
    diaEnsayo (Int): día del ensyo en que se tomaron los datos
    bloque (Int): bloque dentro del día en que se tomaron los datos

    Returns:
    dataDict (Dictionary): diccionario con los datos del ensayo
    """
    # Se divide la cadena de texto por cada línea en un array
    texto=texto.split('\n')
    texto= list(filter(None, texto))
    
    dataDict={"Dirección":fileName, "Tipo de prueba": "Series motoras adquisición", "Día":diaEnsayo, "Bloque": bloque}
    horaInicio=""
    inicioLogged=True
    horaFin=""
    i=0
    # Si el archivo está vacío genera un error
    if len(texto)==0:
        logFile.write(fileName +", Archivo vacío\n")
    else:
        while i < len(texto):
            linea=texto[i]
            # Cada línea se espera que tenga la siguiente estructura "12:20:12.886 -> Transmitiendo"
            if len(linea.split('->'))==2:
                hora=linea.split('->')[0]
                registro=linea.split('->')[1]
                if registro.find("Van a empezar los 50 ensayos")>-1 or inicioLogged:
                    horaInicio=datetime.strptime(hora.split('.')[0],"%H:%M:%S")
                    inicioLogged=False
                elif registro.find("Terminan bloque de 50 ensayos")>-1 :
                    horaFin=datetime.strptime(hora.split('.')[0],"%H:%M:%S")
                elif len(registro.split(','))==14 and registro.split(',')[0].find("Ensayo")==-1:
                    datos=registro.split(',')
                    # Solo se toman los registros del ensayo 15, 35 y 50
                    if float(datos[0])==15 or float(datos[0])==35 or float(datos[0])==50:
                        dataDict["Aciertos_"+datos[0]]=[float(datos[1])]
                        dataDict["PorcentajeAciertos_"+datos[0]]=[((float(datos[1])/float(datos[0]))*100)]
                        dataDict["TiempoRespuestasImpulsivas_"+datos[0]]=[datos[3]]
                        dataDict["Omisiones_"+datos[0]]=[float(datos[4])]
                        dataDict["PorcentajeOmisiones_"+datos[0]]=[((float(datos[4])/float(datos[0]))*100)]
                        dataDict["Categorias_"+datos[0]]=[float(datos[6])]
                        dataDict["LatenciaPromedio_"+datos[0]]=[datos[7]]
                        dataDict["Errores_"+datos[0]]=[datos[8]]
                        dataDict["PorcentajeErrores_"+datos[0]]=[((float(datos[8])/float(datos[0]))*100)]
                        dataDict["AdquisicionReglas_"+datos[0]]=[float(datos[10])]
                        dataDict["EstablecimientoReglas_"+datos[0]]=[float(datos[11])]
                        dataDict["MantenimientoReglas_"+datos[0]]=[float(datos[12])]
                        dataDict["MaximoAciertosSeguidos_"+datos[0]]=[float(datos[13])]
                elif registro.find("Ensayo numero:")>-1 and (registro.find("15")>-1 or registro.find("35")>-1 or registro.find("50")>-1):
                    numReg=float(registro.split(':')[1])
                    while True:
                        if registro.find("Aciertos")>-1:
                            break
                        else:
                            i+=1
                            linea=texto[i]
                            registro=linea.split('->')[1]
                    dataDict["Aciertos_"+str(numReg)]=[float(registro.split(':')[1])]
                    dataDict["PorcentajeAciertos_"+str(numReg)]=[((float(registro.split(':')[1])/numReg)*100)]
                    i+=2
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["TiempoRespuestasImpulsivas_"+str(numReg)]=[registro.split(':')[1]]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["Omisiones_"+str(numReg)]=[float(registro.split(':')[1])]
                    dataDict["PorcentajeOmisiones_"+str(numReg)]=[((float(registro.split(':')[1])/numReg)*100)]
                    i+=2
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["Categorias_"+str(numReg)]=[float(registro.split(':')[1])]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["LatenciaPromedio_"+str(numReg)]=[float(registro.split(':')[1])]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["Errores_"+str(numReg)]=[float(registro.split(':')[1])]
                    dataDict["PorcentajeErrores_"+str(numReg)]=[((float(registro.split(':')[1])/numReg)*100)]
                    i+=2
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["AdquisicionReglas_"+str(numReg)]=[registro.split(':')[1]]
                    i+=1
                    linea=texto[i]
                    registro=linea.split('->')[1]
                    dataDict["MaximoAciertosSeguidos_"+str(numReg)]=[float(registro.split(':')[1])]
                
            i+=1
        
        try:
            dataDict["segundosTotales"]=[(horaFin-horaInicio).total_seconds()]
        except:
            dataDict["segundosTotales"]=[-1]
            logFile.write(fileName +", No se puede calcular el tiempo total del experimento\n")
    return dataDict
def extraerDatos(registros):
    """
    Se cargan los datos de cada registro que se tomó del animal y se extraen los
    datos dependiendo del tipo de prueba a la que fue sometido
    
    Parameters:
    registros (Pandas Dataframe): tabla con la dirección de los archivos de 
    registro

    Returns:
     ( ): 
    """
    # Añadiremos un archivo que usaremos para guardar los archivos que tuvieron errores
    log=open("log.txt", "w")
    #Vamos a ver los datos que se tienen por cada animal
    for animal in habituacion['IdAnimal'].unique():
        output=pd.DataFrame()
        for indice, fila in registros[ registros['IdAnimal']==animal].iterrows():
            try:
                # Datos que queremos guardar de cada registro
                fileName=fila['nombreArchivo']
                tipoPrueba=fila['tipoPrueba']
                diaEnsayo=fila['diaEnsayo']
                bloque=fila['bloque']
                
                # Convertimos el .docx a texto
                
                if tipoPrueba == 'HAB':
                    text=docx2txt.process(fileName)
                    datos_dict=extraerDatosHabituacion(text, fileName,log, diaEnsayo, bloque)
                    registroSesion=pd.DataFrame.from_dict(datos_dict)
                    output=pd.concat([output, registroSesion],  ignore_index=True)
                elif tipoPrueba=="SM_ADQ_DER" or tipoPrueba=="SM_ADQ_IZQ":
                    text=docx2txt.process(fileName)
                    datos_dict=extraerDatosSeriesMotorasAdquisicion(text, fileName,log, diaEnsayo, bloque)
                    registroSesion=pd.DataFrame.from_dict(datos_dict)
                    output=pd.concat([output, registroSesion],  ignore_index=True)
            except:
                log.write(fileName+", Error al leer el archivo\n")
        output.to_excel(animal+".xlsx")
    log.close()

extraerDatos(registros)