import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from baraja import Mazo, Carta
from menu import validar_entrada
from mezclador import mezclar
from distribucion import distribucionSecuencial, distribucionConsecutiva, imprimir_distribucion, generar_posiciones, obtener_posicion_por_valor, distribucion_carta

cartas_repartidas = None
pausa = False

def preparar_mazo(repeticiones):
    mazo = Mazo()
    mezclar(mazo, repeticiones)
    #distribucion, posiciones = distribucionSecuencial(mazo)
    distribucion, posiciones = distribucionConsecutiva(mazo)
    imprimir_distribucion(distribucion, posiciones)
    return [distribucion[posicion] for posicion in sorted(distribucion.keys())]

def distribuir():
    global cartas_repartidas
    try:
        # Obtener el valor del campo de texto
        repeticiones = int(entrada_repeticiones.get())
        if repeticiones <= 0:
            raise ValueError("El número de repeticiones debe ser mayor a 0.")

        # Preparar el mazo y actualizar las cartas repartidas
        cartas_repartidas = preparar_mazo(repeticiones)
        distribucion_carta(cartas_repartidas, ventana, frames_cartas)

        # Habilitar el botón "Iniciar Juego"
        btn_iniciar.config(state="normal")


    except ValueError as e:
        print("Error", f"Entrada inválida: {e}")

def iniciar_juego(cartas, actualizar_ui_callback, ventana, numero_move_label, carta_label, win_label, lose_label, posicion_label):
    velocidad = 2000  # Intervalo de tiempo entre movimientos
    tiempo_volteo = 4000  # Tiempo antes de mover la carta
    posiciones_cartas = cartas
    posicion_actual = 12  # Comienza desde la posición inicial (13)

    def mover_carta():
        nonlocal posicion_actual
        movimiento_contador = 0  # Inicializar el contador de movimientos

        def verificar_estado():
            """Verifica el estado global de las cartas para determinar si se gana o se pierde."""
            cartas_por_voltear = any(
                any(carta.volteado for carta in posicion) for posicion in posiciones_cartas
            )
            if cartas_por_voltear:
                lose_label.config(text="Ha perdido, su predicción no se cumplirá")
            else:
                win_label.config(text="¡Ha ganado! su predicción se cumplirá")

        def realizar_movimiento():
            nonlocal posicion_actual, movimiento_contador

            # Verificar si la simulación está en pausa
            if pausa:
                ventana.after(100, realizar_movimiento)
                return

            if not posiciones_cartas[posicion_actual]:
                verificar_estado()
                return

            carta = posiciones_cartas[posicion_actual][0]
            if not carta.volteado:
                posiciones_cartas[posicion_actual].pop(0)
                actualizar_ui_callback(posiciones_cartas)
                ventana.after(velocidad, realizar_movimiento)
                return

            carta.voltear()
            actualizar_ui_callback(posiciones_cartas)
            carta_label.config(text=f"En posición: {posicion_actual + 1} se voltea carta con valor de: {carta.valor}")
            carta_label.config(text=f"Carta de valor: {carta.valor} en posición: {posicion_actual + 1} ")
            posicion_label.config(text="")

            def mover_y_actualizar():
                nonlocal posicion_actual, movimiento_contador

                posiciones_cartas[posicion_actual].pop(0)
                movimiento_contador += 1
                nueva_posicion = obtener_posicion_por_valor(carta.valor)

                numero_move_label.config(text=f"Movimiento: #{movimiento_contador}")
                posicion_label.config(text=f"Se ubica en la posición: {nueva_posicion + 1}")
                posiciones_cartas[nueva_posicion].append(carta)
                actualizar_ui_callback(posiciones_cartas)
                posicion_actual = nueva_posicion

                if not any(c.volteado for c in posiciones_cartas[posicion_actual]):
                    verificar_estado()
                else:
                    ventana.after(velocidad, realizar_movimiento)

            ventana.after(tiempo_volteo, mover_y_actualizar)

        realizar_movimiento()

    mover_carta()

def iniciar_juego_wrapper():
    global cartas_repartidas

    # Mostrar los botones Pausar y Continuar
    btn_pausar.pack(side="left", padx=5)
    btn_continuar.pack(side="left", padx=5)
    
    # Deshabilitar los botones Distribuir e Iniciar
    btn_distribuir.config(state="disabled")
    btn_iniciar.config(state="disabled")
    
    iniciar_juego(
        cartas_repartidas, 
        actualizar_ui, 
        ventana, 
        numero_move_label, 
        carta_label, 
        win_label,
        lose_label, 
        posicion_label
    )

def pausar_simulacion():
    global pausa
    pausa = True
    btn_pausar.config(state="disabled")  # Deshabilitar botón Pausar
    btn_continuar.config(state="normal")  # Habilitar botón Continuar

def continuar_simulacion():
    global pausa
    pausa = False
    btn_pausar.config(state="normal")  # Habilitar botón Pausar
    btn_continuar.config(state="disabled")  # Deshabilitar botón Continuar

def actualizar_ui(posiciones_cartas):
    """
    Actualiza la interfaz gráfica para reflejar el estado actual de las cartas en cada posición.
    """
    desplazamiento_horizontal = 10  # Separación horizontal entre cartas apiladas
    desplazamiento_vertical = 5     # Separación vertical entre cartas apiladas

    for i, frame in enumerate(frames_cartas):
        # Limpiar las cartas existentes en la posición
        for widget in frame.winfo_children():
            widget.destroy()
        # Apilar nuevas cartas desde el fondo hacia el frente
        for j, carta in enumerate(reversed(posiciones_cartas[i])):  # Apilar en orden inverso
            # Redimensionar la imagen de la carta
            imagen_ruta = carta.obtener_imagen()
            imagen_original = Image.open(imagen_ruta).resize((90, 120))
            imagen_carta = ImageTk.PhotoImage(imagen_original)
            etiqueta_carta = ttk.Label(frame, image=imagen_carta, bootstyle="success")
            etiqueta_carta.image = imagen_carta  # Mantener referencia para el recolector de basura

            # Posicionar la carta dentro del frame con desplazamiento
            etiqueta_carta.place(
                x=j * desplazamiento_horizontal,
                y=j * desplazamiento_vertical
            )

ventana = ttk.Window(themename="darkly")
ventana.title("Juego de cartas")
ventana.geometry("1360x800")

# Crear los frames para las cartas
frames_cartas = []
posiciones = generar_posiciones()  # Llama a la función para obtener las posiciones

style = Style()
style.configure("Custom.TFrame", background="#5b5b5b")  # Define el color de fondo del menú
style.configure("Position.TFrame", background="#870d55")
style.configure("Custom1.TLabel", background="#5b5b5b", foreground="#f1c232") 
style.configure("Custom2.TLabel", background="#5b5b5b", foreground="#9fc5e8")
style.configure("Tittle.TLabel", background="#5b5b5b", foreground="#ec8817") 
style.configure("Move.TLabel", background="#5b5b5b", foreground="#13e7cc")
style.configure("Win.TLabel", background = "#5b5b5b", foreground = "#43bd0e")
style.configure("Lose.TLabel", background = "#5b5b5b", foreground = "#ff0000")


# Crear el frame del menú con el estilo personalizado
menu_frame = ttk.Frame(ventana, width=250, style="Custom.TFrame")
menu_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)

# Etiqueta para el título del menú
menu_titulo = ttk.Label(
    menu_frame,
    text="Juego del Oráculo",
    font=("CustomFontName", 30, "italic"),
    style="Tittle.TLabel"
)
menu_titulo.pack(pady=20)

# Crear un frame para agrupar la etiqueta, el campo de texto y el botón
# Crear un frame para agrupar la etiqueta, el campo de texto y el botón
frame_repeticiones = ttk.Frame(menu_frame, style="Custom.TFrame")
frame_repeticiones.pack(pady=10)

# Etiqueta para el texto "Repeticiones"
etiqueta_repeticiones = ttk.Label(
    frame_repeticiones,
    text="Repeticiones:",
    font=("Helvetica", 20),
    style="Tittle.TLabel"
)
etiqueta_repeticiones.pack(side=LEFT, padx=5)

# Campo de texto para ingresar el número de repeticiones
entrada_repeticiones = ttk.Entry(frame_repeticiones, font=("Helvetica", 12), width=10)
entrada_repeticiones.pack(side=LEFT, padx=5)
entrada_repeticiones.bind("<KeyPress>", validar_entrada)

# Botón "Distribuir"
btn_distribuir = ttk.Button(
    frame_repeticiones,
    text="DISTRIBUIR",
    command=distribuir,
    bootstyle="success"
)
btn_distribuir.pack(side=LEFT, padx=5)

# Crear un nuevo frame para el label de "Predicción" debajo de los tres elementos
frame_prediccion = ttk.Frame(menu_frame, style="Custom.TFrame")
frame_prediccion.pack(pady=10)

# Etiqueta para el texto "Predicción"
etiqueta_prediccion = ttk.Label(
    frame_prediccion,
    text="Predicción:",
    font=("Helvetica", 20),
    style="Tittle.TLabel"
)
etiqueta_prediccion.pack(side=LEFT, padx=5)
entrada_prediccion = ttk.Entry(frame_prediccion, font=("Helvetica", 12), width=20)
entrada_prediccion.pack(side=LEFT, padx=5)


# Botón "Iniciar Juego"
btn_iniciar = ttk.Button(
    menu_frame,
    text="COMENZAR JUEGO",
    command=iniciar_juego_wrapper,  # Reemplazar con tu lógica
    bootstyle="info",
    state=DISABLED  # Inicialmente deshabilitado hasta que se distribuya el mazo
)
btn_iniciar.pack(pady=20)

# Frame para Pausar y Continuar
frame_pausa_continuar = ttk.Frame(menu_frame, style="Custom.TFrame")
frame_pausa_continuar.pack(pady=10)

btn_pausar = ttk.Button(
    frame_pausa_continuar,
    text="PAUSAR",
    command= pausar_simulacion,
    bootstyle="danger"
)
btn_pausar.pack(side=LEFT, padx=5)
btn_pausar.pack_forget()  # Hacerlo invisible al inicio

btn_continuar = ttk.Button(
    frame_pausa_continuar,
    text="CONTINUAR",
    command= continuar_simulacion,
    bootstyle="success",
    state="disabled"
)
btn_continuar.pack(side=LEFT, padx=5)
btn_continuar.pack_forget()  # Hacerlo invisible al inicio

# Etiquetas de información
numero_move_label = ttk.Label(
    menu_frame,
    text=" ",
    font=("Helvetica", 18, "bold"),
    style="Move.TLabel"
)
numero_move_label.pack(pady=5)

carta_label = ttk.Label(
    menu_frame,
    text=" ",
    font=("Helvetica", 16, "bold"),
    style="Custom1.TLabel"
)
carta_label.pack(pady=5)

posicion_label = ttk.Label(
    menu_frame,
    text=" ",
    font=("Helvetica", 16, "bold"),
    style="Custom2.TLabel"
)
posicion_label.pack(pady=5)

win_label = ttk.Label(
    menu_frame,
    text=" ",
    font=("Helvetica", 16, "bold"),
    style="Win.TLabel"
)
win_label.pack(pady=5)

lose_label = ttk.Label(
    menu_frame,
    text=" ",
    font=("Helvetica", 16, "bold"),
    style="Lose.TLabel"
)
lose_label.pack(pady=5)

for x, y in posiciones:
    frame = ttk.Frame(ventana, style="Position.TFrame", width=135, height=160)
    frame.place(x=x, y=y)
    frames_cartas.append(frame)

ventana.mainloop()
