import sys
import math
import random
import copy

class Nodo:
    def _init_(self, tablero, cartas):
        self.tablero = tablero
        self.cartas = cartas
    
# Representa una carta de movimiento, que contiene el propietario, un identificador y una lista de movimientos.
class Carta:
    def _init_(self, owner, id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4):
        self.owner = owner
        self.id = id
        # Cada carta tiene 4 posibles movimientos
        self.movimientos = [[dx_1, dy_1], [dx_2, dy_2], [dx_3, dy_3], [dx_4, dy_4]]
        
# Movimiento concreto en el juego
class Movimiento:
    def _init_(self, id, posicion_ficha, posicion_carta, movimiento):
        self.id = id
        self.posicion_ficha = posicion_ficha    # posicion donde vamos a poner la ficha
        self.posicion_carta = posicion_carta    # posicion de la carta usada
        self.movimiento = movimiento            # lista donde guardamos los movimientos

# Optimizacion del algoritmo MiniMax implementando poda Alfa-Beta
def alfa_beta(nodo, profundidad, alfa, beta, jugadorMax):
    # Caso base: evaluamos el nodo si alcazamos la profundidad cero o llegamos al final
    if ((profundidad == 0) or (esFinal(nodo))):
        return heuristica(nodo), None

    # Caso jugador Max
    else:
        if jugadorMax:
            valor = float('-inf')
            for movimiento in posibles_movimientos(nodo, jugadorMax):
                nuevoNodo = aplica(movimiento, nodo)    # aplicamos el movimiento al nodo
                valNuevoNodo, sigMov = alfa_beta(nuevoNodo, profundidad, alfa, beta, False)
                if valNuevoNodo > valor:
                    valor = valNuevoNodo
                    mejorMovimiento = movimiento
                    alfa = valor
                if alfa >= beta:
                    break
            
            return valor, mejorMovimiento

        # Caso jugador Min
        else:
            valor = float('inf')
            for movimiento in posibles_movimientos(nodo, jugadorMax):
                nuevoNodo = aplica(movimiento, nodo)
                valNuevoNodo, sigMov = alfa_beta(nuevoNodo, profundidad -1, alfa, beta, True)
                if valNuevoNodo < valor:
                    valor = valNuevoNodo
                    mejorMovimiento = movimiento
                    beta = valor
                if alfa >= beta:
                    break
            
            return valor, mejorMovimiento

# Funcion minimax sin optimizar (sin poda)            
def minimax(nodo, profundidad, jugadorMax):
    if ((profundidad == 0) or (esFinal(nodo))):
        return heuristica(nodo), None

    else:
        if jugadorMax:
            valor = float('-inf')

            for movimiento in posibles_movimientos(nodo, jugadorMax):
                nuevoNodo = aplica(movimiento, nodo)
                valNuevoNodo, sigMov = minimax(nuevoNodo, profundidad, False)

                if valNuevoNodo > valor:
                    valor = valNuevoNodo
                    mejorMovimiento = movimiento

            return valor, mejorMovimiento
        
        else: 
            valor = float('inf')

            for movimiento in posibles_movimientos(nodo, jugadorMax):
                nuevoNodo = aplica(movimiento, nodo)
                valNuevoNodo, sigMov = minimax(nuevoNodo, profundidad - 1 , True)

                if valNuevoNodo < valor:
                    valor = valNuevoNodo
                    mejorMovimiento = movimiento

            return valor, mejorMovimiento

def esFinal(nodo):
    maestro1_vivo = False
    maestro0_vivo = False
    
    # Cuenta cuantos chamanes quedan en el tablero
    contador_maestros = 0

    # Verifica si el chaman del primer jugador esta en su posicion, B de Black 
    if nodo.tablero[4][2] == 'B':
        maestro0_vivo = True
    # Verficia si el chaman del otro jugador esta en su posicion, W de White 
    if nodo.tablero[0][2] == 'W':
        maestro1_vivo = True
      
    # Contamos las fichas de ambos jugadores en el tablero
    for i in range(5):
        for j in range(5):
            if nodo.tablero[i][j] == 'W' or nodo.tablero[i][j] == 'B':
                contador_maestros += 1
    
    return (maestro0_vivo or maestro1_vivo or (contador_maestros < 2))

# Comprueba si un posible movimiento es valido
def esPosible(movimiento, ficha, nodo, jugador):
    nuevai = ficha[0] - movimiento[1]
    nuevaj = ficha[1] + movimiento[0]
    # Comprobamos los limites
    if not (0 <= nuevai < len(nodo.tablero) and 0 <= nuevaj < len(nodo.tablero[0])):
        return False
    # Para cada turno evitamos que la ficha quede en una posicion ocupada por otra
    if jugador:
        if player_id == 0:
            if nodo.tablero[nuevai][nuevaj] == 'w' or nodo.tablero[nuevai][nuevaj] == 'W':
                return False
        else:
            if nodo.tablero[nuevai][nuevaj] == 'b' or nodo.tablero[nuevai][nuevaj] == 'B':
                return False

    else:
        if player_id == 0:
            if nodo.tablero[nuevai][nuevaj] == 'b' or nodo.tablero[nuevai][nuevaj] == 'B':
                return False
        else:
            if nodo.tablero[nuevai][nuevaj] == 'w' or nodo.tablero[nuevai][nuevaj] == 'W':
                return False
  
    return True

# Genera los posibles movimientos de todos para el jugador actual
def posibles_movimientos(nodo, jugadorMax):
    sig_movimientos = []

    # Asignamos tanto para el turno del jugador 0 como del jugador 1
    # quienes van a ser sus contrincantes. Si player_id es 0 entonces
    # el contrincante va a ser b y B a quien deben de ganar.
    if player_id == 0:
        ficha = 'w'
        maestro = 'W'
        ficha_enemiga = 'b'
        maestro_enemigo = 'B'
        
    else:
        ficha = 'b'
        maestro = 'B'
        ficha_enemiga = 'w'
        maestro_enemigo = 'W'
    
    if jugadorMax:
        if (player_id == 0):
            for i in range(5):
                for j in range(5):
                    if nodo.tablero[i][j] == ficha or nodo.tablero[i][j] == maestro:
                        for k in range(2):
                            for move in nodo.cartas[k].movimientos:
                                if esPosible(move, [i, j], nodo, True):
                                    siguiente = Movimiento(nodo.cartas[k].id, [i,j], k, move)
                                    sig_movimientos.append(siguiente)
        else:
            for i in range(5):
                for j in range(5):
                    if nodo.tablero[i][j] == ficha or nodo.tablero[i][j] == maestro:
                        for k in range(2, 4):
                            for move in nodo.cartas[k].movimientos:
                                if esPosible(move, [i, j], nodo, True):
                                    siguiente = Movimiento(nodo.cartas[k].id, [i,j], k, move)
                                    sig_movimientos.append(siguiente)

    else:
        if (player_id == 0):
            for i in range(5):
                for j in range(5):
                    if nodo.tablero[i][j] == ficha_enemiga or nodo.tablero[i][j] == maestro_enemigo:
                        for k in range(2, 4):
                            for move in nodo.cartas[k].movimientos:
                                if esPosible(move, (i, j), nodo, False):
                                    siguiente = Movimiento(nodo.cartas[k].id, [i,j], k, move)
                                    sig_movimientos.append(siguiente)
        else:
             for i in range(5):
                for j in range(5):
                    if nodo.tablero[i][j] == ficha_enemiga or nodo.tablero[i][j] == maestro_enemigo:
                        for k in range(2):
                            for move in nodo.cartas[k].movimientos:
                                if esPosible(move, (i, j), nodo, False):
                                    siguiente = Movimiento(nodo.cartas[k].id, [i,j], k, move)
                                    sig_movimientos.append(siguiente)                           
    return sig_movimientos 

# Aplicamos un movimiento sobre el nodo actual y nos devuelve un nuevo estado
def aplica(movimiento, nodo_viejo):
    # copiamos para evitar modificar el estado original
    nodo = copy.deepcopy(nodo_viejo)
    i,j = movimiento.posicion_ficha[0], movimiento.posicion_ficha[1]

    # nuevas coordenadas tras aplicar el movimiento
    nuevai = i - movimiento.movimiento[1]
    nuevaj = j + movimiento.movimiento[0]

    # Actualiza el tablero
    # mueve la ficha de su posicino original a la nueva posicion
    nodo.tablero[i][j], nodo.tablero[nuevai][nuevaj] = '.', nodo.tablero[i][j]
    
    # Actualiza cartas
    # intercambiamos con la carta central
    nodo.cartas[movimiento.posicion_carta], nodo.cartas[4] = nodo.cartas[4], nodo.cartas[movimiento.posicion_carta]
    
    return nodo

# evalua el estado del juego
def heuristica(nodo):

    if player_id == 0:
        ficha = 'w'
        maestro = 'W'
        ficha_enemiga = 'b'
        maestro_enemigo = 'B'
        
    else:
        ficha = 'b'
        maestro = 'B'
        ficha_enemiga = 'w'
        maestro_enemigo = 'W'

    # Evaluamos a los chamanes
    maestro0 = nodo.tablero[4][2]
    maestro1 = nodo.tablero[0][2]

    # Posicion objetivo para cada maestro
    objetivo0 = [0, 2]
    objetivo1 = [4, 2]

    # Calcular la distancia de Manhattan entre los maestros y sus objetivos
    dist_maestro0 = abs(4 - objetivo0[0]) + abs(2 - objetivo0[1])
    dist_maestro1 = abs(0 - objetivo1[0]) + abs(2 - objetivo1[1])

    # Cuenta la cnatidad de fichas en el tablero
    fichas_w = 0
    fichas_b = 0
    for i in range(5):
        for j in range(5):
            if (player_id == 0):
                if nodo.tablero[i][j] == ficha or nodo.tablero[i][j] == maestro:
                    fichas_w += 1
                
            else:        
                if nodo.tablero[i][j] == ficha or nodo.tablero[i][j] == maestro:
                    fichas_b += 1
                

    # Calcular la heurística como la diferencia entre las distancias de los maestros a sus objetivos
    # y la diferencia entre la cantidad de fichas de cada jugador en el tablero
    valor_heuristico0 = (dist_maestro1 - dist_maestro0) + (fichas_w - fichas_b)

    return valor_heuristico0


# Convierte un movimiento en una cadena de texto que representa las coordenadas de origen y destino.
def moverFicha(movimiento):
    # Obtiene las coordenadas actuales de la ficha del objeto movimiento
    pos1 = [movimiento.posicion_ficha[0], movimiento.posicion_ficha[1]] 
    # Calcula la pos final despues de aplicar el movimiento
    pos2 = [movimiento.posicion_ficha[0] - movimiento.movimiento[1], movimiento.posicion_ficha[1] + movimiento.movimiento[0]] 
    #Convertimos a un formato bien legible
    return f"{chr(pos1[1]+65)}{5-pos1[0]}{chr(pos2[1]+65)}{5-pos2[0]}"


player_id = int(input())

while True:
    tablero = []
    cartasDisponibles = []
    board = []
    for i in range(5):
        board = list(input())
        tablero.append(board)
    # 5 cartas disponibles
    for i in range(5):
        owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4 = [int(j) for j in input().split()]
        carta = Carta(owner, card_id, dx_1, dy_1, dx_2, dy_2, dx_3, dy_3, dx_4, dy_4)
        cartasDisponibles.append(carta)
    #leemos la cantidad de accions realizadas en cada turno
    action_count = int(input())
    for i in range(action_count):
        inputs = input().split()
        card_id = int(inputs[0])
        move = inputs[1]

    # Creamos el nodo actual apartir del estado del talero y las cartas
    nodo = Nodo(tablero, cartasDisponibles)
    #valor, mejorMov = minimax(nodo, 1, jugador)

    # Usamos poda para mejorar el movimiento, podemos usar minimax tambien
    valor, mejorMov = alfa_beta(nodo, 1, float('-inf'), float('inf'), True)

    # Imprimimos
    print(mejorMov.id, moverFicha(mejorMov),"Estamos jugando")
    
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr, flush=True)
