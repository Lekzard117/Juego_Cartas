from baraja import Carta,Mazo
import random

def dividir_mazo(mazo):
    """Divide el mazo en dos mitades."""
    mitad = len(mazo.cartas) // 2
    return mazo.cartas[:mitad], mazo.cartas[mitad:]


def mezclar(mazo, repeticiones):
    mezclar_intercalado_aleatorio(mazo, repeticiones)

def mezclar_intercalado(mazo):
    """Mezcla las cartas del mazo intercalando las mitades."""
    mitad1, mitad2 = dividir_mazo(mazo)
    mazo.cartas = []  # Vaciar el mazo antes de mezclar
    while mitad1 or mitad2:
        if mitad1:
            mazo.cartas.append(mitad1.pop(0))
        if mitad2:
            mazo.cartas.append(mitad2.pop(0))

def mezclar_intercalado_aleatorio(mazo, repeticiones):
    """Mezcla las cartas del mazo intercalando con comportamiento aleatorio varias veces."""
    for _ in range(repeticiones):  # Realizar la mezcla la cantidad de veces especificada
        mitad1, mitad2 = dividir_mazo(mazo)  # Dividir el mazo en dos mitades
        mazo.cartas = []  # Vaciar el mazo principal antes de empezar a mezclar
        while mitad1 or mitad2:  # Continuar mientras haya cartas en cualquiera de las mitades
            if not mitad1:  # Si la primera mitad está vacía
                mazo.cartas.append(mitad2.pop(0))  # Tomar la primera carta de mitad2 y añadirla al mazo
            elif not mitad2:  # Si la segunda mitad está vacía
                mazo.cartas.append(mitad1.pop(0))  # Tomar la primera carta de mitad1 y añadirla al mazo
            else:  # Si ambas mitades tienen cartas
                probabilidad = random.random()  # Generar un número aleatorio entre 0 y 1
                if probabilidad < 0.7:  # Probabilidad alta (70%) de alternar cartas entre ambas mitades
                    mazo.cartas.append(mitad1.pop(0))  # Tomar una carta de mitad1
                    mazo.cartas.append(mitad2.pop(0))  # Tomar una carta de mitad2
                elif probabilidad < 0.9:  # Probabilidad media (20%) de añadir 2 cartas seguidas de la misma mitad
                    if random.choice([True, False]):  # Decidir aleatoriamente entre mitad1 y mitad2
                        mazo.cartas.append(mitad1.pop(0))  # Tomar una carta de mitad1
                        if mitad1:  # Verificar si mitad1 aún tiene cartas
                            mazo.cartas.append(mitad1.pop(0))  # Tomar otra carta de mitad1















                            
                    else:  # Si no se eligió mitad1, trabajar con mitad2
                        mazo.cartas.append(mitad2.pop(0))  # Tomar una carta de mitad2
                        if mitad2:  # Verificar si mitad2 aún tiene cartas
                            mazo.cartas.append(mitad2.pop(0))  # Tomar otra carta de mitad2
                else:  # Probabilidad baja (10%) de añadir 3 cartas seguidas de la misma mitad
                    if random.choice([True, False]):  # Decidir aleatoriamente entre mitad1 y mitad2
                        mazo.cartas.append(mitad1.pop(0))  # Tomar una carta de mitad1
                        if mitad1:  # Verificar si mitad1 aún tiene cartas
                            mazo.cartas.append(mitad1.pop(0))  # Tomar otra carta de mitad1
                        if mitad1:  # Verificar si mitad1 aún tiene más cartas
                            mazo.cartas.append(mitad1.pop(0))  # Tomar otra carta de mitad1
                    else:  # Si no se eligió mitad1, trabajar con mitad2
                        mazo.cartas.append(mitad2.pop(0))  # Tomar una carta de mitad2
                        if mitad2:  # Verificar si mitad2 aún tiene cartas
                            mazo.cartas.append(mitad2.pop(0))  # Tomar otra carta de mitad2
                        if mitad2:  # Verificar si mitad2 aún tiene más cartas
                            mazo.cartas.append(mitad2.pop(0))  # Tomar otra carta de mitad2