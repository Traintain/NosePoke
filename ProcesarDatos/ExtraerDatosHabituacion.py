# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 15:52:48 2022

@author: jm.rivera@uniandes.edu.co
"""

import os
import pandas as pd
import docx2txt
from datetime import datetime, timedelta

registros=pd.read_excel("registrosMachosYHembras.xlsx", index_col=0)

medidas={"HAB":[["Ensayo_", "Aciertos_",
                        "PorcentajeAciertos_","TiempoRespuestasImpulsivas_", 
                        "Omisiones_", "PorcentajeOmisiones_", "Categorias_",
                        "CorrectasDerecha_","CorrectasIzquierda_","LatenciaPromedio_",
                        "MaximoAciertosSeguidos_"],
                        # 0: Numero, 1: porcentaje, 2: tiempo con "ms", -1: número de ensayo
                        [-1, 0, 1, 0, 0, 1, 0, 0, 0, 2, 0],
                        "Ensayo,Aciertos,Porcentaje aciertos,Tiempo total en Respuestas impulsivas,Omisiones,Porcentaje omisiones,Categorias,Total correctas a la derecha,Total correctas a la izquierda,Latencia promedio,Maximo de aciertos seguidos"],
         "SM_ADQ":[["Ensayo_", "Aciertos_",
                           "PorcentajeAciertos_", "TiempoRespuestasImpulsivas_",
                           "Omisiones_", "PorcentajeOmisiones_","Categorias_",
                           "LatenciaPromedio_", "Errores_", "PorcentajeErrores_",
                           "AdquisicionReglas_", "EstablecimientoReglas_", 
                           "MantenimientoReglas_","MaximoAciertosSeguidos_"],
                          [-1, 0, 1, 0, 0, 1, 0, 2, 0, 1, 0, 0, 0, 0],
                          "Ensayo,Aciertos,Porcentaje aciertos,Tiempo total en Respuestas impulsivas,Omisiones,Porcentaje omisiones,Categorias,Latencia promedio,Errores,Porcentaje errores,Adquisicion de reglas,Establecimiento de reglas,Mantenimiento de reglas,Maximo de aciertos seguidos"],
         }
                          
def separarLinea(linea):
    if len(linea.split('->'))==2:
        hora=linea.split('->')[0]
        registro=linea.split('->')[1]
    else:
        hora=-1
        registro=linea
    return hora, registro

def extraerDatosEnsayo(texto, fileName,logFile, diaEnsayo, bloque, idAnimal, tipoPrueba):
    """
    Se carga el registro de cada animal en formato de texto y se realiza la 
    extracción de datos
    
    Parameters:
    texto (String): Cadena de texto con los datos del ensayo
    fileName (String): dirección del archivo de registro
    logFile (File): archivo donde se escriben los errores de ejecución
    diaEnsayo (Int): día del ensyo en que se tomaron los datos
    bloque (Int): bloque dentro del día en que se tomaron los datos
    tipoPrueba (String): Cadena de texto con el nombre de la prueba

    Returns:
    dataDict (Dictionary): diccionario con los datos del ensayo
    """
    texto=texto.split('\n')
    texto= list(filter(None, texto))
    dataDict={"Dirección":fileName, "Tipo de prueba": tipoPrueba, "Día":diaEnsayo, "Bloque": bloque, "IdAnimal":idAnimal}
    if tipoPrueba=='SM_ADQ_DER' or tipoPrueba=='SM_ADQ_IZQ':
        tipoPrueba='SM_ADQ'
    
    # Variables para registrar el tiempo
    horaInicio=""
    horaFin=""
    inicioLogged=True
    finLogged=True
    
    # Se usará como contador del número de líneas
    i=0
    
    # Se usará para comprobar que no haya archivos con 2 bloques
    lastReg=-1
    
    # Si el archivo está vacío genera un error
    if len(texto)==0:
        logFile.write(fileName +", Archivo vacío\n")
    else:
        # Se lee el archivo línea a línea
        while i < len(texto):
            linea=texto[i]
            # Cada línea se espera que tenga la siguiente estructura "12:20:12.886 -> Transmitiendo"
            hora, registro = separarLinea(linea)
                
            # Registra el primer timestamp del archivo. En caso de que encuentre la marca de inicio lo sobreescribe
            if (registro.find("Van a empezar los 50 ensayos")>-1 or inicioLogged) and hora!=-1:
                horaInicio=datetime.strptime(hora.split('.')[0],"%H:%M:%S")
                inicioLogged=False
                
            # Asume que los datos están de la siguiente manera: "1.00,1,2.00,0.00,0,0.00,0,0,1,8388.00,1"
            elif len(registro.split(','))==(len(medidas[tipoPrueba][0])):
                encabezadoOk=False
                while i < len(texto):
                    linea=texto[i]
                    hora, registro = separarLinea(linea)
                    # Se revisará que el archivo tenga el encabezado esperado
                    if medidas[tipoPrueba][2] in registro:
                        encabezadoOk=True
                    else:
                        datos=registro.split(',')
                        # Solo se toman los registros del ensayo 15, 35 y 50
                        numReg=float(datos[0])
                        if numReg==15 or numReg==35 or numReg==50:
                            for j in range( 1, (len(medidas[tipoPrueba][0])) ):
                                try:
                                    nombreColumna=medidas[tipoPrueba][0][j]
                                    # Este dato es un número o una marca de tiempo SIN unidades ("ms")
                                    if medidas[tipoPrueba][1][j]==0 or medidas[tipoPrueba][1][j]==2:
                                        dataDict[nombreColumna+str(numReg)]=[float(datos[j])]
                                    # Este dato es un porcentaje
                                    elif medidas[tipoPrueba][1][j]==1:
                                        dataDict[nombreColumna+str(numReg)]=[((float(datos[j-1])/numReg)*100)]
                                except:
                                    logFile.write(fileName +", El tipo de dato no fue el esperado\n")
                    
                        if lastReg > numReg:
                            logFile.write(fileName +", El archivo contiene dos o más registros\n")
                            lastReg=numReg
                        else:
                            lastReg=numReg
                        
                        if numReg == 50:
                            break
                    
                    i+=1
            elif registro.find("Ensayo numero:")>-1:
                numReg=float(registro.split(':')[1])
                if lastReg > numReg:
                    logFile.write(fileName +", El archivo contiene dos o más registros\n")
                    lastReg=numReg
                else:
                    lastReg=numReg
                
                if (numReg==15 or numReg==35 or numReg==50) and numReg != lastReg:
                    while True:
                        if registro.find("Aciertos")>-1:
                            break
                        else:
                            i+=1
                            linea=texto[i]
                            hora, registro = separarLinea(linea)
                    registroAnterior=-1
                    for j in range( 1, (len(medidas[tipoPrueba][0])) ):
                        linea=texto[i]
                        hora, registro = separarLinea(linea)
                        try:
                            nombreColumna=medidas[tipoPrueba][0][j]
                            # Este dato es un número
                            if medidas[tipoPrueba][1][j]==0:
                                dataDict[nombreColumna+str(numReg)]=[float(registro.split(':')[1])]
                                registroAnterior=float(registro.split(':')[1])
                            # Este dato es un porcentaje
                            elif medidas[tipoPrueba][1][j]==1:
                                dataDict[nombreColumna+str(numReg)]=[((registroAnterior/numReg)*100)]
                            # Este dato es una marca de tiempo CON unidades ("ms")
                            elif medidas[tipoPrueba][1][j]==2:
                                data=registro.split(':')[1].strip().split(" ")[0]
                                dataDict[nombreColumna+str(numReg)]=[data]
                        except:
                            logFile.write(fileName +", El tipo de dato no fue el esperado\n")
                        i+=1
                    i-=1
            i+=1
        
        try:
            horaFin=datetime.strptime(hora.split('.')[0],"%H:%M:%S")
            segundosTotales=(horaFin-horaInicio).total_seconds()
            if segundosTotales < 0:
                horaFin -= timedelta(hours=1)
                horaInicio -= timedelta(hours=1)
                segundosTotales=(horaFin-horaInicio).total_seconds()
            dataDict["segundosTotales"]=[segundosTotales]
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
    outputEnsayo=pd.DataFrame()
    for animal in registros['IdAnimal'].unique():
        output=pd.DataFrame()
        for indice, fila in registros[ registros['IdAnimal']==animal].iterrows():
            try:
                # Datos que queremos guardar de cada registro
                fileName=fila['nombreArchivo']
                tipoPrueba=fila['tipoPrueba']
                diaEnsayo=fila['diaEnsayo']
                bloque=fila['bloque']
                sexo=fila['sexo']
                idAnimal=fila['IdAnimal']
                
                # Convertimos el .docx a texto
                
                if tipoPrueba == 'HAB' and sexo=="M":
                    text=docx2txt.process(fileName)
                    datos_dict=extraerDatosEnsayo(text, fileName,log, diaEnsayo, bloque, idAnimal, tipoPrueba)
                    registroSesion=pd.DataFrame.from_dict(datos_dict)
                    output=pd.concat([output, registroSesion],  ignore_index=True)                    
                #if (tipoPrueba=="SM_ADQ_DER" or tipoPrueba=="SM_ADQ_IZQ") and sexo=="M":
                #    text=docx2txt.process(fileName)
                #    datos_dict=extraerDatosEnsayo(text, fileName,log, diaEnsayo, bloque, idAnimal, 'SM_ADQ')
                #    registroSesion=pd.DataFrame.from_dict(datos_dict)
                #    output=pd.concat([output, registroSesion],  ignore_index=True)
            except:
                log.write(fileName+", Error al leer el archivo\n")
        output.to_excel(animal+".xlsx")
        outputEnsayo=pd.concat([outputEnsayo, output],  ignore_index=True)
    outputEnsayo.to_excel("datosHabituacionMachos.xlsx")
    log.close()

extraerDatos(registros)