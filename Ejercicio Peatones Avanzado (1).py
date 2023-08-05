import numpy as np
import matplotlib.pyplot as plt
import time
import psutil

tiempo_inicio=time.time()

def programa():

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
    masX = max(diccionarioX.values())
    masY = max(diccionarioY.values())
    masXY = max(diccionarioXY.values())
            
    repetidosX = []
    repetidosY = []
    repetidosXY = []

    #encontrar las coordenadas más repetidas según el valor máximo
    repetidosX = [coordenada for coordenada in diccionarioX if diccionarioX[coordenada]==masX]
    repetidosY = [coordenada for coordenada in diccionarioY if diccionarioY[coordenada]==masY]
    repetidosXY = [coordenada for coordenada in diccionarioXY if diccionarioXY[coordenada]==masXY]      

    print ("La/s coordenada/s más repetida/s en el eje x es/son:",repetidosX,"con",masX,"apariciones")
    print()
    print ("La/s coordenada/s más repetida/s en el eje y es/son:",repetidosY,"con",masY,"apariciones") 
    print()
    print ("El/los par/es de coordenada/s más repetido/s es/son:",repetidosXY,"con",masXY,"apariciones")
    print()

    #calcular maximos, minimos y varianza
    listaX = []
    listaY = []

    for i in range(filas):
        listaX.append(matriz[i][2])
        listaY.append(matriz[i][3])

    print("Máximo de las coordenadas en el eje X:",max(listaX))
    print()
    print("Máximo de las coordenadas en el eje Y:",max(listaY))
    print()
    print("Mínimo de las coordenadas en el eje X:",min(listaX))
    print()
    print("Mínimo de las coordenadas en el eje Y:",min(listaY))
    print()
    print("Varianza de las coordenadas en el eje X:",round(np.var(listaX),2))
    print()
    print("Varianza de las coordenadas en el eje Y:",round(np.var(listaY),2))
    print()

    #pasar a pixeles
    matriz2 = matriz[:,2:4]

    for i in range(filas):
        matriz2[i][0] = int(matriz2[i][0]*35.6+320)
        matriz2[i][1] = int(matriz2[i][1]*-96+480)

    #matriz de frecuencia
    matrizFrecuencia = np.zeros([640,480])

    for i in range(filas):
        coordenadaX = int(matriz2[i][0])
        coordenadaY = int(matriz2[i][1])
        matrizFrecuencia[coordenadaX][coordenadaY] += 1

    #graficar
    matrizFrecuencia_rotada = np.rot90(matrizFrecuencia)
    plt.imshow(matrizFrecuencia_rotada, cmap="hot", aspect="auto", origin='lower')
    plt.show()

def get_resource_info(code_to_measure):
    resources_save_data = get_resource_usage(code_to_measure=code_to_measure)
    print(f"Tiempo de CPU: {resources_save_data['tiempo_cpu']} segundos")
    print(f"Uso de memoria virtual: {resources_save_data['memoria_virtual']} MB")
    print(f"Uso de memoria residente: {resources_save_data['memoria_residente']} MB")
    print(f"Porcentaje de uso de CPU: {resources_save_data['%_cpu']} %")


# Función que devuelve el tiempo de CPU y el uso de memoria para un código dado
def get_resource_usage(code_to_measure):
    process = psutil.Process()
    #get cpu status before running the code
    cpu_percent = psutil.cpu_percent()
    start_time = time.time()
    code_to_measure#()
    end_time = time.time()
    end_cpu_percent = psutil.cpu_percent() 
    cpu_percent = end_cpu_percent - cpu_percent
    cpu_percent = cpu_percent / psutil.cpu_count()
    
    return {
        'tiempo_cpu': end_time - start_time,
        'memoria_virtual': process.memory_info().vms / (1024 * 1024),  # Convertir a MB
        'memoria_residente': process.memory_info().rss / (1024 * 1024),  # Convertir a MB
        '%_cpu': cpu_percent # Porcentaje de uso de CPU
    }

#Ejecutar programa y medir sus recursos
get_resource_info(programa())

fin_tiempo = time.time()

#Calculo del tiempo utilizado
tiempo_transcurrido = fin_tiempo - tiempo_inicio
print("Tiempo de ejecución: ",round(tiempo_transcurrido*1000,2)," milisegundos")