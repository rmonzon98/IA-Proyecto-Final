## Algoritmo para verificar cuantos cuadros cerrados hay en el tablero con el protocolo definido para el Proyecto

## Aqui defino algunas variables para que les haga sentido el algoritmo, pero son cosas que pueden sacar del board que van a recibir de parte del servidor

# N es la dimension del board, donde el número representa la cantidad de puntos horizontal y vertical que conforma la dimension del tablero
# En este caso el tablero es de 6 PUNTOS por 6 PUNTOS
#   *   *   *   *   *   * 
#   *   *   *   *   *   *
#   *   *   *   *   *   *
#   *   *   *   *   *   *
#   *   *   *   *   *   *
#   *   *   *   *   *   *

N = 6

# Variable para identificar espacios vacios
EMPTY = 99

# Como se había acordado en el protocolo, el tableto que recibiran es un arreglo que contiene 2 arreglos
# El primer arreglo es para las lineas horizontales que se dibujan en el tablero, iniciando desde la esquina superior izquierda y contando las posiciones de arriba hacia abajo
# El segundo arreglo es para las lineas verticales que se dibujan en el tablero, iniciando desde la esquina superior izquierda y contando las posiciones de izquierda a derecha
board = [
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99],
    [99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99]
]

# Estas son variables que nos sirven para iterar sobre cada renglon del tablero y poder llevar las cuentas de cuando nos pasemos al siguiente renglon de revision
# Es parte del algoritmo de revison, y deben ir seteadas a cero antes de hacer el ciclo for que viene a continuacion que es quien hace la revision de cuantos cuadros
# cerrados hay en el tablero
acumulador = 0
contador = 0
contadorPuntos = 0
  
# Primero hacemos un recorrido sobre el largo de uno de los 2 arreglos (esto es debido a que ambos arreglos son del mismo tamaño, porque asi será en el torneo)
for i in range(len(board[0])):
    # La logica de esto si alguien tiene alguna duda se los puedo mandar en una demostración que hice a papel de la simetría de los tableros cuadrados en totito chino
    # Pero en general se revisa si la posicion siguiente de la que se tiene actualmente en la iteracion del arreglo se sale de la fila "física" que se está revisando
    # para hacer un "salto de fila" ya que los cuadrados nunca se pueden formar con lineas horizontales o verticales que esten en lados opuestos del tablero
    if ((i + 1) % N) != 0:
        # En caso no estemos haciendo un "salto de linea" se revisa si hay un cuadrado formado alrededor de la posicion sobre la que se esta iterando
        # Si alguien tiene duda de como funciona saber cuales son los otras 3 posiciones que formarian el cuadrado, avisenme para que les pase la demostración
        if board[0][i] != EMPTY and board[0][i + 1] != EMPTY and board[1][contador + acumulador] != EMPTY and board[1][contador + acumulador + 1] != EMPTY:
            # En caso de que las 4 posiciones revisadas esten llenas, eso significa que se ha realizado un punto y se acumula
            contadorPuntos = contadorPuntos + 1
        # Variable que ayuda a determinar 2 posiciones para formar un cuadrado en la siguiente iteración
        acumulador = acumulador + N
    # En caso de que se tenga que hacer un "salto de linea"
    else:
        # Variable que ayuda a determinar 2 posiciones para formar un cuadrado en la siguiente iteración
        contador = contador + 1
        acumulador = 0

print("Cantidad de cuadritos cerrados: ", contadorPuntos)

## Nota: Este algoritmo solo cuenta cuantos cuadros hay cerrados en el tablero actual
## El arbitro lo que hace básicamente es revisar esto con el tablero actual, cuenta el punteo actual
## lanza la movida que mando el jugador, repite el algoritmo contando nuevamente los cuadrados cerrados 
## con el tablero con su movida y si el número de cuadrados cerrados aumenta en 1 o 2, esos son puntos 
## para el jugador que hizo la movida.

## Ustedes deben de averiguar como su algoritmo va a predecir cual es el mejor tiro que puede hacer.



## Aqui está como se cuentan los puntos de cada jugador cuando reciben el tablero
player1 = 0
player2 = 0
FILLEDP11 = 1
FILLEDP12 = 2
FILLEDP21 = -1
FILLEDP22 = -2


for i in range(len(board[0])):
    if board[0][i] == FILLEDP12:
        player1 = player1 + 2
    elif board[0][i] == FILLEDP11:
        player1 = player1 + 1
    elif board[0][i] == FILLEDP22:
        player2 = player2 + 2
    elif board[0][i] == FILLEDP21:
        player2 = player2 + 1

for j in range(len(board[1])):
    if board[1][j] == FILLEDP12:
        player1 = player1 + 2
    elif board[1][j] == FILLEDP11:
        player1 = player1 + 1
    elif board[1][j] == FILLEDP22:
        player2 = player2 + 2
    elif board[1][j] == FILLEDP21:
        player2 = player2 + 1

## Aqui imprimimos los punteos de cada jugador
print("Punteo Jugador 1: ", player1)
print("Punteo Jugador 2: ", player2)
