import tkinter as tk
from baraja import Mazo
from mezclador import mezclar
from PIL import Image, ImageTk

repeticiones = 5

mazo = Mazo()
mezclar(mazo, repeticiones)

def distribucionConsecutiva(mazo):
    """
    Se ingresan 4 cartas en una posicion, de la sola.
    """
    # Validar que el mazo tenga suficientes cartas
    if len(mazo.cartas) < 52:
        raise ValueError("El mazo debe contener al menos 52 cartas para esta distribución.")
    
    coordenadas = generar_posiciones()
    posiciones = {i + 1: coordenadas[i] for i in range(len(coordenadas))}

    # Crear el diccionario para almacenar las cartas en cada posición
    distribucion = {i: [] for i in posiciones.keys()}

    # Asignar cartas a cada posición
    index = 0
    for posicion in distribucion.keys():
        for _ in range(4):  # Cada posición recibe 4 cartas
            distribucion[posicion].append(mazo.cartas[index])
            index += 1

    # Verificar que todas las posiciones tengan exactamente 4 cartas
    for posicion, cartas in distribucion.items():
        if len(cartas) != 4:
            raise ValueError(f"Error: La posición {posicion} tiene {len(cartas)} cartas en lugar de 4.")

    return distribucion, posiciones

def distribucionSecuencial(mazo):
    """
    Distribuye las cartas en una mesa de forma cíclica:
    - Recorre todas las posiciones, asignando una carta a cada una en orden.
    - Cada posición tendrá 4 cartas al final.
    """
    # Validar que el mazo tenga suficientes cartas
    if len(mazo.cartas) < 52:
        raise ValueError("El mazo debe contener al menos 52 cartas para esta distribución.")
    
    # Generar las posiciones dinámicamente
    coordenadas = generar_posiciones()
    posiciones = {i + 1: coordenadas[i] for i in range(len(coordenadas))}

    # Crear el diccionario para almacenar las cartas en cada posición
    distribucion = {i: [] for i in posiciones.keys()}

    # Asignar las cartas de forma cíclica
    index = 0
    while index < len(mazo.cartas):
        for posicion in distribucion.keys():
            if len(distribucion[posicion]) < 4:  # Solo asignar si hay espacio
                distribucion[posicion].append(mazo.cartas[index])
                index += 1
                if index >= len(mazo.cartas):  # Si se acaban las cartas, detener
                    break

    # Verificar que todas las posiciones tengan exactamente 4 cartas
    for posicion, cartas in distribucion.items():
        if len(cartas) != 4:
            raise ValueError(f"Error: La posición {posicion} tiene {len(cartas)} cartas en lugar de 4.")

    return distribucion, posiciones

    #return distribucion
def imprimir_distribucion(distribucion, posiciones):
    """
    Imprime la distribución de las cartas con un contador para cada posición y un índice junto a cada carta.
    """
    for posicion, cartas in distribucion.items():
        print(f"Posición {posicion} ({posiciones[posicion]})")
        for idx, carta in enumerate(cartas, start=1):  # Agregar índice de carta
            print(f"  [{idx}] {carta.valor} de {carta.palo}")
        print()  # Línea en blanco para separar las posiciones

#distribucion, posiciones = distribucionConsecutiva(mazo)
#distribucion, posiciones = distribucionSecuencial(mazo)
#imprimir_distribucion(distribucion, posiciones)
def generar_posiciones():
    x_inicial = 70
    y_inicial = 10
    ancho = 220  # Incrementa el espacio horizontal entre columnas
    alto = 180   # Incrementa el espacio vertical entre filas

    posiciones = [
        (x_inicial, y_inicial), (x_inicial + ancho, y_inicial), 
        (x_inicial + 2 * ancho, y_inicial), (x_inicial + 3 * ancho, y_inicial),
        (x_inicial + 3 * ancho, y_inicial + alto), (x_inicial + 3 * ancho, y_inicial + 2 * alto), 
        (x_inicial + 3 * ancho, y_inicial + 3 * alto),
        (x_inicial + 2 * ancho, y_inicial + 3 * alto), (x_inicial + ancho, y_inicial + 3 * alto), 
        (x_inicial, y_inicial + 3 * alto),
        (x_inicial, y_inicial + 2 * alto), (x_inicial, y_inicial + alto),
        (x_inicial + 1.5 * ancho, y_inicial + 1.5 * alto),  # Centro
    ]
    return posiciones


def obtener_posicion_por_valor(valor):
    """
    Convierte el valor de una carta en un índice de posición (0-12).
    Maneja tanto valores numéricos como los valores especiales de la baraja.
    """
    # Diccionario para valores especiales
    valores = {'As': 1, 'Jota': 11, 'Reina': 12, 'Rey': 13}
    
    # Si el valor es un número en cadena ('2', '3', ..., '10'), conviértelo a entero
    if valor.isdigit():
        return int(valor) - 1  # Ajusta para índices de 0 a 12
    else:
        # Si es un valor especial ('As', 'Jota', etc.), mapea usando el diccionario
        return valores.get(valor, 0) - 1  # Ajusta para índices de 0 a 12
    
def distribucion_carta(carta_textos, ventana, frames_cartas):
    """
    Coloca las cartas en la interfaz inicial, apilándolas con desplazamiento dentro de los frames.
    """
    # Dimensiones fijas para las cartas y desplazamientos
    ancho_carta = 90
    alto_carta = 120
    desplazamiento_horizontal = 10  # Separación horizontal entre cartas apiladas
    desplazamiento_vertical = 5   # Separación vertical entre cartas apiladas
    
    for i, frame in enumerate(frames_cartas):
        # Limpiar cualquier contenido previo del frame
        for widget in frame.winfo_children():
            widget.destroy()

        for j, carta in enumerate(carta_textos[i]):
            # Redimensionar la imagen de la carta
            imagen_ruta = carta.obtener_imagen()
            imagen_original = Image.open(imagen_ruta)
            imagen_redimensionada = imagen_original.resize((ancho_carta, alto_carta))
            imagen_carta = ImageTk.PhotoImage(imagen_redimensionada)

            # Crear una etiqueta para cada carta, apilada con desplazamientos dentro del frame
            etiqueta_carta = tk.Label(frame, image=imagen_carta, bg="green")
            etiqueta_carta.image = imagen_carta  # Mantener referencia para el recolector de basura
            etiqueta_carta.place(
                x=j * desplazamiento_horizontal,  # Desplazamiento dentro del frame
                y=j * desplazamiento_vertical
            )