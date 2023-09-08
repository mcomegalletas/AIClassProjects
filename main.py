import random
import copy
import math
import matplotlib.pyplot as plt

Size_Poblacion = 20
Size_Nodo = 20
Size_Recorrido = Size_Nodo+1
Numero_Ejecucion = 9999
poblacion = []
x = []
y = []
trayectoria = [[0 for x in range(Size_Recorrido)] for y in range(Size_Recorrido)]
dCidade = [[0 for x in range(Size_Poblacion)] for y in range(Size_Poblacion)]
distancia = [0 for x in range(Size_Poblacion)]
Padres_Uno = None
Padres_Dos = None
costByExecution = []

"""
    Generar primera poblacion
"""
def generarPrimeraPoblacion():
    # For each position, generates a new possible path
    for _ in range(1, Size_Poblacion + 1):
        generarPosibleCamino()

"""
    Método llamado en generarPrimeraPoblacion() para generar
    posible nueva trayectoria para la poblacion
"""
def generarPosibleCamino():
    path = []
    for _ in range(1, Size_Nodo + 1):
            # Generar nuevo número entre 1 y el tamaño de la población
        randomNum = random.randint(1, Size_Poblacion)
        # Mientras el número generado existe en la lista, se genera uno nuevo
        while(numeroExisteEnCamino(path, randomNum)):
            randomNum = random.randint(1, Size_Poblacion)
        path.append(randomNum)
    poblacion.append(path)

"""
    Método para verificar si número ya está en trayectoria
"""
def numeroExisteEnCamino(path, number):
    for i in path:
        if i == number:
            return True
    return False

"""
    Generar arreglos X y Y que representan distancia en eje "x" y "y" usados para
    calcular la matriz identidad de función fitness
"""
def generarX_Y():
    for _ in range(Size_Nodo):
        randomNumber = random.random()
        randomNumber = round(randomNumber, 2)
        x.append(randomNumber)

        randomNumber = random.random()
        randomNumber = round(randomNumber, 2)
        y.append(randomNumber)

"""
Hacer cambio entre dos ciudades en el camino, 5% de chance de mutación (No sé si se puede cambiar)
"""
def mutar(matrix):
    for i in range(0, len(matrix)):
        for _ in range(0, len(matrix[i])):
            ranNum = random.randint(1, 100)
            if ranNum >= 1 and ranNum <= 5:
                indexOne = random.randint(0, 19)
                indexTwo = random.randint(0, 19)
                auxOne = matrix[i][indexOne]
                auxTwo = matrix[i][indexTwo]
                matrix[i][indexOne] = auxTwo
                matrix[i][indexTwo] = auxOne

"""
    Generar matriz trayectoria, que es la misma matriz de población pero con primera columna duplicada
    el carrito debe llegar al mismo lugar donde empieza
"""
def generarTrayectoria():
    global trayectoria
    trayectoria = copy.deepcopy(poblacion)
    for ways in trayectoria:
        first = ways[0]
        ways.append(first)

"""
    Generar arreglo con suma de cada parte en arreglo de la población basado en matriz de la trayectoria
"""
def calcularDistancias():
    global distancia
    distancia = [0 for x in range(Size_Poblacion)]
    for i in range(len(poblacion)):
        for j in range(len(poblacion[i])):
            firstPos = 19 if trayectoria[i][j] == 20 else trayectoria[i][j]
            secondPos = 19 if trayectoria[i][j+1] == 20 else trayectoria[i][j+1]
            distancia[i] += round(dCidade[firstPos][secondPos], 4)
    dict_dist = {i: distancia[i] for i in range(0, len(distancia))}
    distancia = copy.deepcopy(dict_dist)
    return sorted(distancia.items(), key=lambda kv: kv[1])

"""

    Generar matriz identidad (dCidade) basado en arreglos X y Y, luego llama calcularDistancias() para generar arreglo
    con suma de cada trayectoria 
    which will be used later to do the cycle process
"""
def fitnessFunction():
    for i in range(len(poblacion)):
        for j in range(len(poblacion)):
            dCidade[i][j] = round(math.sqrt(((x[i] - x[j])**2) + ((y[i] - y[j])**2)), 4)
    return calcularDistancias()

"""
    Función ruleta, genera dos arreglos con 5 padres 
    which will be used later to do the cycle process
"""
def rouletteFunction(sorted_x):
    global Padres_Uno
    global Padres_Dos
    arr = []
    rouletteArr = []
    for i in range(10):
        arr.append(sorted_x[i][0])
    for j in range(len(arr)):
        for _ in range(10 - j):
            rouletteArr.append(arr[j])
    Padres_Uno = crearPadres(rouletteArr)
    Padres_Dos = crearPadres(rouletteArr)

"""
    Método auxiliar en rouletteFunction() para generar arreglo de dos padres
"""
def crearPadres(rouletteArr):
    parentArr = []
    for _ in range(5):
        parentArr.append(rouletteArr[random.randint(0, 54)])
    return parentArr

"""
   Método usado en método ciclo para ver si hay ciudades duplicadas
"""
def hayDuplicados(auxArray, usedIndexes):
    for i in range(len(auxArray)):
        for j in range(i, len(auxArray)):
            if i != j and auxArray[i] == auxArray[j]:
                if i in usedIndexes:
                    return j
                else:
                    return i
    return -1

"""

    Método con lógica 'ciclo'
    1. Por cada dos hijos en arreglo de hijos, hace arreglo aleatorio entre los dos hijos hasta que no hay elemento duplicado
    2. Mutar hijos generados
    3. Agregar hijos a arreglo de población
"""
def doCycle(sorted_x):
    global poblacion
    hijos = []

    for i in range(5):
        Padres_Uno_Aux = Padres_Uno[i]
        Padres_Dos_Aux = Padres_Dos[i]
        usedIndexes = []

        randomIndexInsideCromossomus = random.randint(0, Size_Poblacion - 1)

        usedIndexes.append(randomIndexInsideCromossomus)

        hijoUno = copy.deepcopy(poblacion[Padres_Uno_Aux])
        hijoDos = copy.deepcopy(poblacion[Padres_Dos_Aux])

        valAuxOne = hijoUno[randomIndexInsideCromossomus]
        valAuxTwo = hijoDos[randomIndexInsideCromossomus]

        hijoUno[randomIndexInsideCromossomus] = valAuxTwo
        hijoDos[randomIndexInsideCromossomus] = valAuxOne

        while(hayDuplicados(hijoUno, usedIndexes) != -1):
            newIndex = hayDuplicados(hijoUno, usedIndexes)
            usedIndexes.append(newIndex)

            valAuxOne = hijoUno[newIndex]
            valAuxTwo = hijoDos[newIndex]

            hijoUno[newIndex] = valAuxTwo
            hijoDos[newIndex] = valAuxOne

        #  Al generar hijos, agregarlo en arreglo de hijos
        hijos.append(hijoUno)
        hijos.append(hijoDos)

    # Mutar arreglo de hijos
    mutar(hijos)

    # Hacer copia temporal de poblacion antes de cambiarla
    tempPop = copy.deepcopy(poblacion)

    for i in range(10):
        poblacion[i] = copy.deepcopy(tempPop[sorted_x[i][0]])

    # Ajustar población
    for j in range(10, Size_Poblacion):
        poblacion[j] = copy.deepcopy(hijos[j - 10])


def main():
    # Runs only once. Generates the poblacion, x and y, and trayectoria matrix
    generarPrimeraPoblacion()
    generarX_Y()
    generarTrayectoria()

    # Runs in a loop 0 - 9999.
    for _ in range(Numero_Ejecucion):
        sorted_x = fitnessFunction()
        rouletteFunction(sorted_x)
        doCycle(sorted_x)
        generarTrayectoria() # Generate the Tour matrix again, as the poblacion is updated
        costByExecution.append(sorted_x[0][1]) # Appends the cost to the array of costs (plotted at the end)

    # Generates the fitness values for the last poblacion
    sorted_x = fitnessFunction()

    print('Tamaño de Población: %s' % (Size_Poblacion))
    print('Tasa de Mutación: 5%')
    print('Número de Nodos: %s' % (Size_Nodo))
    print('Mejor Costo: %s' % sorted_x[0][1])
    print('Mejor solución : %s' % poblacion[0])

    # Show the path graph
    plt.plot(trayectoria[0])
    plt.plot(trayectoria[0], 'ro')
    plt.axis([0, 20, 0, 20])
    plt.show()

    # Show the cost graph
    plt.plot(costByExecution)
    plt.show()

if __name__ == "__main__":
    main()