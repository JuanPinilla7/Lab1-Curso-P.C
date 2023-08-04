import numpy as np

archivo = open("UNI_CORR_500_01.txt","r")

lista = []
contador = 0
for lineas in archivo.readlines():
    if contador>4: #las primeras 4 lineas no sirven
        datos = lineas.split()
        lista.append(datos)
    contador += 1

filas = len(lista)
matriz = np.zeros([filas,5])

diccionarioX = {}
diccionarioY = {}
diccionarioXY = {}

for i in range(len(lista)):
    #llenar la matriz con el peatón, el frame y sus tres coordenadas
    matriz[i][0]=lista[i][0]
    matriz[i][1]=lista[i][1]
    matriz[i][2]=float(lista[i][2])
    matriz[i][3]=float(lista[i][3])
    matriz[i][4]=float(lista[i][4])
    
    if matriz[i][2] not in diccionarioX: #aquí se llenan los diccionarios con las coordenadas y la cantidad de veces que salen
        diccionarioX[matriz[i][2]] = 1
    else:
        diccionarioX[matriz[i][2]] += 1
        
    if matriz[i][3] not in diccionarioY:
        diccionarioY[matriz[i][3]] = 1
    else:
        diccionarioY[matriz[i][3]] += 1    
    
    coordenadaXY = str(matriz[i][2]),str(matriz[i][3])
    
    if coordenadaXY not in diccionarioXY:
        diccionarioXY[coordenadaXY] = 1
    else:
        diccionarioXY[coordenadaXY] += 1

#buscar la coordenada máx repetida en cada eje
masX = 0
for coordenada in diccionarioX:
    if diccionarioX[coordenada]>masX:
        masX = diccionarioX[coordenada]

masY = 0
for coordenada in diccionarioY:
    if diccionarioY[coordenada]>masY:
        masY = diccionarioY[coordenada]

masXY = 0
for coordenada in diccionarioXY:
    if diccionarioXY[coordenada]>masXY:
        masXY = diccionarioXY[coordenada]
        
repetidosX = []
repetidosY = []
repetidosXY = []

#encontrar las coordenadas más repetidas según el valor máximo
for coordenada in diccionarioX:
    if diccionarioX[coordenada]==masX:
         repetidosX.append(coordenada)  

for coordenada in diccionarioY:
    if diccionarioY[coordenada]==masY:
        repetidosY.append(coordenada)

for coordenada in diccionarioXY:
    if diccionarioXY[coordenada]==masXY:
        repetidosXY.append(coordenada)        

print ("La/s coordenada/s más repetida/s en el eje x es/son:",repetidosX,"con",masX,"apariciones")
print()
print ("La/s coordenada/s más repetida/s en el eje y es/son:",repetidosY,"con",masY,"apariciones") 
print()
print ("La/s coordenada/s más repetida/s en el eje y es/son:",repetidosXY,"con",masXY,"apariciones")