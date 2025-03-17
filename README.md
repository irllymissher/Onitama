
# Juego de Chamanes: Minimax con Poda Alfa-Beta

## Descripción

Este proyecto implementa un juego de estrategia en el que dos jugadores compiten con el objetivo de eliminar al Chamán del equipo contrario y alcanzar la casilla del otro Chamán. La inteligencia del juego se basa en el algoritmo **minimax** con **poda alfa-beta** para optimizar las decisiones y reducir el tiempo de cómputo.

## Objetivos del Juego

- **Eliminar al Chamán adversario:** Acercarse y eliminar la pieza clave del oponente.
- **Llegar a la casilla del otro Chamán:** Posicionarse en la casilla objetivo del enemigo para ganar.

## Mecánica del Juego

- **Baraja de Movimientos:** Cada jugador dispone de una baraja de movimientos. En cada turno, se mueven las cartas, intercambiándose con la carta central.
- **Movimiento y Eliminación:** Mover una carta sobre una pieza enemiga permite eliminarla.
- **Carta Inhabilitada:** Cada jugador posee una quinta carta que no se puede utilizar, lo que añade un elemento estratégico a la elección de jugadas.

## Algoritmo y Estrategia

### Minimax con Poda Alfa-Beta

- **Minimax:** Se utiliza para evaluar las jugadas futuras y seleccionar la mejor opción en función de un árbol de decisiones.
- **Poda Alfa-Beta:** Optimiza el algoritmo descartando ramas del árbol que no influirán en la decisión final, mejorando la eficiencia.

### Función Heurística

La función heurística evalúa el estado del juego en cada movimiento, considerando:
- **Proximidad entre chamanes:** Determina qué tan cerca está cada jugador de su objetivo.
- **Amenazas:** Evalúa el riesgo de eliminación en base a la posición de las piezas enemigas.
- **Posicionamiento Global:** Considera la configuración general del tablero para prever jugadas futuras.

Esta heurística nos permite predecir el resultado final de la partida y ajustar la estrategia en tiempo real.

## Evaluación y Puntaje

Para la evaluación de la práctica se tomará en cuenta:

-   Correcta implementación del algoritmo minimax.
-   Uso efectivo de la poda alfa-beta.
-   Explicación clara y detallada de la heurística.
-   Calidad y claridad del código.
-   Posicionamiento global del juego y estrategia implementada.
