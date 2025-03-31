import tkinter as tk
from tkinter import ttk, simpledialog, colorchooser, filedialog, messagebox
import pygame
import time
from threading import Thread
import random
from PIL import Image, ImageTk
import requests
from io import BytesIO
from pydub import AudioSegment

# Inicializar Pygame
pygame.mixer.init()

# Lista para almacenar las mejores puntuaciones
mejores_puntuaciones = []

# Cargar sonidos
sonidos = {
    "Do": pygame.mixer.Sound("sonidos/C.wav"),
    "Re": pygame.mixer.Sound("sonidos/D.wav"),
    "Mi": pygame.mixer.Sound("sonidos/E.wav"),
    "Fa": pygame.mixer.Sound("sonidos/F.wav"),
    "Sol": pygame.mixer.Sound("sonidos/G.wav"),
    "La": pygame.mixer.Sound("sonidos/A.wav"),
    "Si": pygame.mixer.Sound("sonidos/B.wav"),
}

from letras_canciones import letras_canciones

canciones = {
    "Estrellita, ¿Dónde Estás?": ["Do", "Do", "Sol", "Sol", "La", "La", "Sol",
                                    "Fa", "Fa", "Mi", "Mi", "Re", "Re", "Do",
                                    "Sol", "Sol", "Fa", "Fa", "Mi", "Mi", "Re",
                                    "Sol", "Sol", "Fa", "Fa", "Mi", "Mi", "Re",
                                    "Do", "Do", "Sol", "Sol", "La", "La", "Sol",
                                    "Fa", "Fa", "Mi", "Mi", "Re", "Re", "Do"],
    "Abrázame Más": ["Do", "Mi", "Sol", "Do", "Si", "La", "Sol",
                    "La", "Sol", "Fa", "Mi", "Re", "Do",
                    "Do", "Mi", "Sol", "Do", "Si", "La", "Sol",
                    "La", "Sol", "Fa", "Mi", "Re", "Do",
                    "Sol", "La", "Si", "Do", "Si", "La",
                    "La", "Sol", "Fa", "Mi", "Re", "Do",
                    "Sol", "La", "Si", "Do", "Si", "La",
                    "La", "Sol", "Fa", "Mi", "Re", "Do",
                    "Do", "Mi", "Sol", "Do", "Si", "La", "Sol",
                    "La", "Sol", "Fa", "Mi", "Re", "Do",
                    "Sol", "La", "Si", "Do", "Si", "La",
                    "La", "Sol", "Fa", "Mi", "Re", "Do"],
    "Otra canción": ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si", "Do"],
    "Feliz Cumpleaños": ["Sol", "Sol", "La", "Sol", "Do", "Si",
                        "Sol", "Sol", "La", "Sol", "Re", "Do",
                        "Sol", "Sol", "Sol", "Mi", "Do", "Si", "La",
                        "Fa", "Fa", "Mi", "Do", "Re", "Do"],
    "Jingle Bells": ["Mi", "Mi", "Mi", "Mi", "Mi", "Mi", "Mi", "Sol", "Do", "Re", "Mi",
                    "Fa", "Fa", "Fa", "Fa", "Fa", "Mi", "Mi", "Mi", "Mi", "Sol", "Sol", "Mi", "Re", "Sol"],
    "Twinkle Twinkle Little Star": ["Do", "Do", "Sol", "Sol", "La", "La", "Sol",
                                        "Fa", "Fa", "Mi", "Mi", "Re", "Re", "Do"],
    "Mary Had a Little Lamb": ["Mi", "Re", "Do", "Re", "Mi", "Mi", "Mi",
                                "Re", "Re", "Re", "Mi", "Sol", "Sol",
                                "Mi", "Re", "Do", "Re", "Mi", "Mi", "Mi",
                                "Re", "Re", "Mi", "Re", "Do"],
    "London Bridge is Falling Down": ["Sol", "La", "Sol", "Fa", "Mi", "Fa", "Sol",
                                        "Mi", "Fa", "Sol", "Re", "Mi", "Fa",
                                        "Sol", "La", "Sol", "Fa", "Mi", "Fa", "Sol",
                                        "Mi", "Sol", "Do"],
    "Old MacDonald Had a Farm": ["Do", "Do", "Sol", "Sol", "La", "La", "Sol",
                                    "Fa", "Fa", "Mi", "Mi", "Re", "Re", "Do",
                                    "Sol", "Sol", "Do", "Do", "Sol", "Sol", "Do"],
    "Row, Row, Row Your Boat": ["Do", "Do", "Do", "Re", "Mi", "Mi", "Re", "Mi", "Fa", "Sol",
                                "Do", "Do", "Do", "Sol", "Sol", "Sol", "Do", "Re", "Mi", "Fa", "Sol"],
    "Are You Sleeping?": ["Do", "Re", "Mi", "Do", "Do", "Re", "Mi", "Do",
                            "Mi", "Fa", "Sol", "Mi", "Fa", "Sol",
                            "Sol", "La", "Sol", "Fa", "Mi", "Do",
                            "Sol", "La", "Sol", "Fa", "Mi", "Do",
                            "Do", "Sol", "Do", "Do", "Sol", "Do"]
}

temas_color = {
    "Retro": {
        "fondo_general": "#F0E68C",
        "fondo_piano": "#8B4513",
        "teclas_blancas": "#FFF8DC",
        "teclas_negras": "#A0522D"
    },
    "Naturaleza": {
        "fondo_general": "#B0E57C",
        "fondo_piano": "#228B22",
        "teclas_blancas": "#F5FFFA",
        "teclas_negras": "#2E8B57"
    },
    "Futurista": {
        "fondo_general": "#1A1A1A",
        "fondo_piano": "#4B0082",
        "teclas_blancas": "#E6E6FA",
        "teclas_negras": "#9370DB"
    },
    "Estándar": {"fondo_general": "#282828", "fondo_piano": "#383838", "teclas_blancas": "white", "teclas_negras": "black"},
    "Oscuro": {"fondo_general": "#121212", "fondo_piano": "#212121", "teclas_blancas": "#E0E0E0", "teclas_negras": "#424242"},
    "Claro": {"fondo_general": "#E0E0E0", "fondo_piano": "#F0F0F0", "teclas_blancas": "white", "teclas_negras": "black"},
    "Azulados": {"fondo_general": "#1C2833", "fondo_piano": "#2E4053", "teclas_blancas": "#A9CCE3", "teclas_negras": "#21618C"},
    "Kawaii": {"fondo_general": "#FCE4EC", "fondo_piano": "#F8BBD0", "teclas_blancas": "#E1BEE7", "teclas_negras": "#8E24AA"}
}

# Variables de control
volumen = 0.5
pausado = False
reproduciendo = False
color_fondo_general = "#282828"
color_fondo_piano = "#383838"
color_teclas_blancas = "white"
color_teclas_negras = "black"

# Variables del juego
secuencia_juego = []
indice_secuencia = 0
puntuacion = 0
juego_en_curso = False
modo_juego = "raton"
tiempo_inicio = 0
pausado = False
niveles = {"Fácil": 3, "Medio": 4, "Difícil": 5}
nivel_actual = "Fácil"
longitud_secuencia = niveles[nivel_actual]
puntuaciones = []
modo_libre = False
secuencia_replicar = []
indice_replicar = 0
puntuacion_replicar = 0
juego_replicar = False
velocidad_actual = 1.0

def generar_secuencia():
    """Genera una secuencia aleatoria de teclas para el juego."""
    global secuencia_juego
    notas_disponibles = list(sonidos.keys())
    for _ in range(longitud_secuencia):
        secuencia_juego.append(random.choice(notas_disponibles))

def iluminar_tecla(nota):
    """Ilumina la tecla especificada con efecto de profundidad"""
    tema = temas_color[tema_actual]
    canvas.itemconfig(nota, fill=tema['teclas_blancas'], outline=tema['teclas_negras'], width=2)
    canvas.create_rectangle(canvas.bbox(nota), fill='', outline=tema['teclas_negras'], width=1, stipple='gray12')
    sonidos[nota].play()
    ventana.after(200, lambda n=nota: apagar_tecla(n))

def apagar_tecla(nota):
    """Restaura el estilo original de la tecla"""
    tema = temas_color[tema_actual]
    if nota in ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]:
        canvas.itemconfig(nota, fill=tema['teclas_blancas'], outline='')
    else:
        canvas.itemconfig(nota, fill=tema['teclas_negras'], outline='')

def iniciar_juego():
    """Inicia el juego de tocar las teclas."""
    global secuencia_juego, indice_secuencia, puntuacion, juego_en_curso, tiempo_inicio, pausado, juego_replicar
    secuencia_juego = []
    indice_secuencia = 0
    puntuacion = 0
    juego_en_curso = True
    tiempo_inicio = time.time()
    pausado = False
    actualizar_puntuacion()
    generar_secuencia()
    mostrar_secuencia(velocidad_actual)
    juego_replicar = False

def verificar_tecla(nota):
    """Verifica si la tecla tocada es la correcta."""
    if juego_replicar:
        verificar_tecla_replicar(nota)
    elif juego_en_curso and not pausado:
        if nota == secuencia_juego[indice_secuencia]:
            puntuacion += 1
            actualizar_puntuacion()
            indice_secuencia += 1
            if indice_secuencia == len(secuencia_juego):
                messagebox.showinfo("¡Correcto!", f"¡Has completado la secuencia! Puntuación: {puntuacion}")
                puntuaciones.append(puntuacion)
                puntuaciones.sort(reverse=True)
                puntuaciones[:] = puntuaciones[:3]
                iniciar_juego()
        else:
            messagebox.showerror("¡Incorrecto!", "Has tocado la tecla equivocada.")
            iniciar_juego()

def pausar_juego():
    """Pausa o reanuda el juego."""
    global pausado
    pausado = not pausado
    if pausado:
        boton_pausa.config(text="Reanudar Juego")
    else:
        boton_pausa.config(text="Pausar Juego")
        mostrar_secuencia(velocidad_actual)

def mostrar_secuencia(velocidad=1.0):
    """Muestra la secuencia de teclas al usuario con la velocidad especificada."""
    global indice_secuencia, tiempo_inicio, pausado
    if juego_en_curso and not pausado:
        if indice_secuencia < len(secuencia_juego):
            nota_actual = secuencia_juego[indice_secuencia]
            iluminar_tecla(nota_actual)
            tiempo_transcurrido = time.time() - tiempo_inicio
            velocidad_ajustada = max(0.7, 1 - tiempo_transcurrido / 120) * velocidad
            ventana.after(int(1200 * velocidad_ajustada), lambda: apagar_tecla(nota_actual))
            ventana.after(int(1800 * velocidad_ajustada), mostrar_secuencia, velocidad)
            indice_secuencia += 1
        else:
            indice_secuencia = 0
            if modo_juego == "raton":
                habilitar_teclas_raton()
            else:
                habilitar_teclas_teclado()

def cambiar_modo_juego(modo):
    """Cambia el modo de juego."""
    global modo_juego
    modo_juego = modo
    if modo == "teclado":
        habilitar_teclas_teclado()
    else:
        habilitar_teclas_raton()

def habilitar_teclas_raton():
    """Habilita la interacción con las teclas usando el ratón."""
    for nota in sonidos.keys():
        canvas.tag_bind(nota, "<Button-1>", lambda event, n=nota: verificar_tecla(n))

def habilitar_teclas_teclado():
    """Habilita la interacción con las teclas usando el teclado."""
    teclas_notas = {"z": "Do", "x": "Re", "c": "Mi", "v": "Fa", "b": "Sol", "n": "La", "m": "Si"}
    for tecla, nota in teclas_notas.items():
        ventana.bind(tecla, lambda event, n=nota: verificar_tecla(n))

def actualizar_puntuacion():
    """Actualiza la puntuación y la muestra en la etiqueta."""
    puntaje_label.config(text=f"Puntaje: {puntuacion}")

def mostrar_mejores_puntuaciones():
    """Muestra las mejores puntuaciones en un mensaje."""
    if puntuaciones:
        mensaje = "Mejores Puntuaciones:\n"
        for i, puntaje in enumerate(puntuaciones):
            mensaje += f"{i + 1}. {puntaje}\n"
        messagebox.showinfo("Mejores Puntuaciones", mensaje)
    else:
        messagebox.showinfo("Mejores Puntuaciones", "Aún no hay puntuaciones.")

def cambiar_sonido(nota, archivo_sonido):
    """Cambia el sonido de la nota especificada."""
    sonidos[nota] = pygame.mixer.Sound(archivo_sonido)

def cambiar_color_tecla(nota, color):
    """Cambia el color de la tecla especificada."""
    canvas.itemconfig(nota, fill=color)

def cambiar_color_fondo(color):
    """Cambia el color de fondo del juego."""
    canvas.config(bg=color)

def activar_modo_libre():
    """Activa el modo de juego libre."""
    global modo_libre
    modo_libre = True
    messagebox.showinfo("Modo Libre", "¡Ahora puedes tocar el piano libremente!")

def desactivar_modo_libre():
    """Desactiva el modo de juego libre."""
    global modo_libre
    modo_libre = False

def iniciar_cancion_conocida(nombre_cancion):
    """Inicia el modo de juego con una canción conocida."""
    global secuencia_juego, indice_secuencia, puntuacion, juego_en_curso, juego_replicar, canciones_conocidas
    secuencia_juego = canciones_conocidas[nombre_cancion]
    indice_secuencia = 0
    puntuacion = 0
    juego_en_curso = True
    mostrar_secuencia(velocidad_actual)
    juego_replicar = False

def iniciar_modo_replicar():
    """Inicia el modo de juego de replicar canciones."""
    global secuencia_replicar, indice_replicar, puntuacion_replicar, juego_replicar, juego_en_curso
    secuencia_replicar = generar_cancion_aleatoria()
    indice_replicar = 0
    puntuacion_replicar = 0
    juego_replicar = True
    reproducir_cancion_replicar()
    juego_en_curso = False

def generar_cancion_aleatoria():
    """Genera una canción aleatoria para replicar."""
    notas_disponibles = list(sonidos.keys())
    return [random.choice(notas_disponibles) for _ in range(5)]

def reproducir_cancion_replicar():
    """Reproduce la canción que el jugador debe replicar."""
    global indice_replicar
    if juego_replicar and indice_replicar < len(secuencia_replicar):
        sonidos[secuencia_replicar[indice_replicar]].play()
        ventana.after(1000, reproducir_cancion_replicar)
        indice_replicar += 1
    else:
        indice_replicar = 0
        habilitar_teclas_raton()

def verificar_tecla_replicar(nota):
    """Verifica si la tecla tocada es la correcta en el modo replicar."""
    global indice_replicar, puntuacion_replicar, juego_replicar
    if juego_replicar:
        if nota == secuencia_replicar[indice_replicar]:
            puntuacion_replicar += 1
            indice_replicar += 1
        if indice_replicar == len(secuencia_replicar):
            messagebox.showinfo("¡Correcto!", f"¡Has replicado la canción! Puntuación: {puntuacion_replicar}")
            juego_replicar = False
        else:
            messagebox.showerror("¡Incorrecto!", "Has tocado la tecla equivocada.")
            juego_replicar = False

def cambiar_velocidad(velocidad):
    """Cambia la velocidad del juego."""
    global velocidad_actual
    velocidad_actual = velocidad
    messagebox.showinfo("Velocidad", f"Velocidad cambiada a {velocidad_actual}.")

def mostrar_tutorial():
    """Muestra un tutorial interactivo."""
    messagebox.showinfo("Tutorial", "¡Bienvenido al juego de piano!\n\nSigue la secuencia de teclas que se iluminan para ganar puntos.\n\nPuedes usar el ratón o el teclado para tocar las teclas.\n\n¡Diviértete!")

def cambiar_nivel(nivel):
    """Cambia el nivel de dificultad del juego."""
    global nivel_actual, longitud_secuencia
    nivel_actual = nivel
    longitud_secuencia = niveles[nivel_actual]
    messagebox.showinfo("Nivel", f"Nivel cambiado a {nivel_actual}.")

# Función para mostrar el tutorial (ahora en la ventana principal)
def mostrar_tutorial():
    """Muestra un tutorial del piano virtual."""
    tutorial_texto = """
    **Menú de Ayuda del Piano Virtual**

    ¡Bienvenido al piano virtual! Este menú te guiará a través de todas las funciones y opciones disponibles.

    **Tocar el Piano**
    * **Con el ratón**: Haz clic en las teclas del piano para reproducir los sonidos correspondientes a cada nota.
    * **Con el teclado**: Usa las teclas 'z', 'x', 'c', 'v', 'b', 'n' y 'm' para tocar las notas Do, Re, Mi, Fa, Sol, La y Si, respectivamente.

    **Modos de Juego**
    * **Modo Ratón**: Ideal para tocar el piano de forma intuitiva haciendo clic en las teclas.
    * **Modo Teclado**: Perfecto para practicar y tocar melodías usando el teclado de tu ordenador.

    **Juego de Memoria Musical**
    1.  Ve a "Ajustes" > "Iniciar Juego".
    2.  Observa la secuencia de teclas que se iluminan.
    3.  Toca las teclas en el mismo orden en que se iluminaron.
    4.  Gana puntos por cada secuencia correcta. Si te equivocas, el juego se reinicia.
    5.  Puedes pausar el juego en cualquier momento desde "Ajustes" > "Pausar Juego".
    6.  Tu puntuación se muestra en la parte superior de la pantalla.
    7.  A medida que avances, la velocidad de la secuencia aumentará.

    **Ajustes y Personalización**
    * **Volumen**: Ajusta el volumen del piano con el control deslizante.
    * **Temas**: Cambia la apariencia del piano seleccionando un tema predeterminado en el menú desplegable.
    * **Editor de música**: Crea tus propias canciones seleccionando las notas y guardándolas.
    * **Cargar Sonido**: Añade tus propios sonidos al piano cargando archivos de audio.
    * **Exportar a MP3**: Guarda tus creaciones musicales en formato MP3 para compartirlas.
    * **Colores Aleatorios**: Cambia los colores del piano y el fondo de forma aleatoria para una apariencia divertida.
    * **Personalizar Colores**: Elige los colores que más te gusten para el fondo, las teclas y otros elementos del piano.
    * **Estilo Grafico**: Te permite cambiar los temas del piano.

    **Otras Funciones**
    * **Tutorial**: Vuelve a este menú de ayuda en cualquier momento para recordar cómo usar las funciones del piano.
    * **Salir**: Cierra el piano virtual cuando hayas terminado de usarlo.

    ¡Diviértete creando música y explorando todas las posibilidades del piano virtual!
    """
    messagebox.showinfo("Tutorial del Piano Virtual", tutorial_texto)

def cambiar_tema(event):
    """Cambia los colores de la interfaz según el tema seleccionado."""
    tema = combobox_temas.get()
    colores = temas_color[tema]
    ventana.config(bg=colores["fondo_general"])
    canvas.config(bg=colores["fondo_piano"])
    dibujar_teclas(colores["teclas_blancas"], colores["teclas_negras"])

# Variables para mantener los colores actuales
color_teclas_blancas = "white"
color_teclas_negras = "black"

def dibujar_teclas(color_blancas, color_negras):
    """Dibuja las teclas del piano con los colores especificados."""
    global color_teclas_blancas, color_teclas_negras
    color_teclas_blancas = color_blancas
    color_teclas_negras = color_negras
    canvas.delete("all")
    notas_blancas = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
    notas_negras = [("Do#", 1), ("Re#", 2), ("Fa#", 4), ("Sol#", 5), ("La#", 6)]
    for i, nota in enumerate(notas_blancas):
        x = 20 + i * 100
        canvas.create_rectangle(x, 150, x + 90, 350, fill=color_teclas_blancas, tags=nota)
        canvas.tag_bind(nota, "<Button-1>", lambda e, n=nota: sonidos[n].play())
    for nota, pos in notas_negras:
        x = 20 + pos * 100 - 30
        canvas.create_rectangle(x, 150, x + 60, 270, fill=color_teclas_negras, tags=nota)

def cambiar_tema(tema):
    """Cambia los colores de la interfaz según el tema seleccionado."""
    colores = temas_color[tema]
    ventana.config(bg=colores["fondo_general"])
    canvas.config(bg=colores["fondo_piano"])
    dibujar_teclas(colores["teclas_blancas"], colores["teclas_negras"])

def exportar_como_mp3(nombre_cancion):
    notas = canciones[nombre_cancion]
    audio_completo = AudioSegment.silent(duration=0)  # Audio inicial vacío

    for nota in notas:
        if nota in sonidos:
            sonido_pygame = sonidos[nota]
            # Convertir el sonido de pygame a pydub
            samples = pygame.sndarray.array(sonido_pygame)
            audio_segment = AudioSegment(samples.tobytes(), frame_rate=44100, sample_width=samples.dtype.itemsize, channels=1)
            audio_completo += audio_segment
            audio_completo += AudioSegment.silent(duration=500)  # Pausa entre notas

    archivo_mp3 = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Archivos MP3", "*.mp3")])
    if archivo_mp3:
        audio_completo.export(archivo_mp3, format="mp3")
        messagebox.showinfo("Exportación exitosa", f"La canción se ha exportado como {archivo_mp3}")
        
# puntuacion test
def verificar_tecla(nota):
    """Verifica si la tecla tocada es la correcta."""
    global indice_secuencia, puntuacion, juego_en_curso
    if juego_en_curso and not pausado:
        if nota == secuencia_juego[indice_secuencia]:
            sonidos[nota].play()
            puntuacion += 1
            puntaje_label.config(text=f"Puntaje: {puntuacion}")
            indice_secuencia += 1
            if indice_secuencia == len(secuencia_juego):
                messagebox.showinfo("¡Correcto!", f"¡Has completado la secuencia! Puntuación: {puntuacion}")
                mejores_puntuaciones.append(puntuacion)  # Agregar puntuación a la lista
                mejores_puntuaciones.sort(reverse=True)  # Ordenar de mayor a menor
                mejores_puntuaciones[:] = mejores_puntuaciones[:3]  # Mantener solo las 3 mejores
                iniciar_juego()
        else:
            messagebox.showerror("¡Incorrecto!", "Has tocado la tecla equivocada.")
            iniciar_juego()

# Función para reproducir canción
def reproducir_cancion():
    global pausado, reproduciendo
    pausado = False
    reproduciendo = True
    cancion_seleccionada = canciones_combobox.get()
    if cancion_seleccionada in canciones:
        notas = canciones[cancion_seleccionada]
        tiempo_inicio = time.time()
        letra_index = 0
        puntuacion_karaoke = 0
        
        # Mostrar el área de letras y puntuación si no existen
        if not hasattr(ventana, 'letra_label'):
            ventana.letra_label = tk.Label(ventana, text="", font=("Arial", 14), bg=color_fondo_general, fg="white")
            ventana.letra_label.pack(pady=10)
        
        if not hasattr(ventana, 'puntuacion_karaoke_label'):
            ventana.puntuacion_karaoke_label = tk.Label(ventana, text="Puntuación Karaoke: 0", font=("Arial", 12), bg=color_fondo_general, fg="white")
            ventana.puntuacion_karaoke_label.pack(pady=5)
        
        # Actualizar letras si están disponibles
        if cancion_seleccionada in letras_canciones:
            letras = letras_canciones[cancion_seleccionada]
            def actualizar_letra():
                nonlocal letra_index, puntuacion_karaoke
                if letra_index < len(letras) and reproduciendo and not pausado:
                    tiempo_actual = time.time() - tiempo_inicio
                    if tiempo_actual >= letras[letra_index][1]:
                        # Resaltar la letra actual
                        letra_actual = letras[letra_index][0]
                        ventana.letra_label.config(text=letra_actual, fg="yellow")
                        
                        # Programar el cambio de color después de un tiempo
                        ventana.after(1000, lambda: ventana.letra_label.config(fg="white"))
                        
                        # Actualizar puntuación basada en la sincronización
                        diferencia_tiempo = abs(tiempo_actual - letras[letra_index][1])
                        if diferencia_tiempo < 0.2:
                            puntuacion_karaoke += 100
                        elif diferencia_tiempo < 0.5:
                            puntuacion_karaoke += 50
                        else:
                            puntuacion_karaoke += 25
                        
                        ventana.puntuacion_karaoke_label.config(text=f"Puntuación Karaoke: {puntuacion_karaoke}")
                        letra_index += 1
                    ventana.after(100, actualizar_letra)
            actualizar_letra()
        
        def reproducir_notas():
            nonlocal letra_index
            for i, nota in enumerate(notas):
                if not reproduciendo:
                    break
                if pausado:
                    continue
                    
                sonidos[nota].play()
                # Ajustar el tiempo entre notas según el índice de la letra
                if letra_index < len(letras_canciones.get(cancion_seleccionada, [])):
                    siguiente_tiempo = letras_canciones[cancion_seleccionada][letra_index][1]
                    tiempo_actual = time.time() - tiempo_inicio
                    tiempo_espera = max(0.3, (siguiente_tiempo - tiempo_actual) / 2)
                    time.sleep(tiempo_espera)
                else:
                    time.sleep(0.3)
                    
        # Iniciar la reproducción en un hilo separado
        Thread(target=reproducir_notas).start()
        
        # Mostrar puntuación final
        if hasattr(ventana, 'puntuacion_karaoke_label'):
            messagebox.showinfo("¡Puntuación Final!", f"Tu puntuación en el karaoke: {puntuacion_karaoke}")
            ventana.puntuacion_karaoke_label.config(text="Puntuación Karaoke: 0")
        
        # Limpiar letra al finalizar
        if hasattr(ventana, 'letra_label'):
            ventana.letra_label.config(text="")


# Función pausar/reanudar
def pausar_o_reanudar():
    global pausado
    pausado = not pausado
    boton_pausa.config(text="Reanudar" if pausado else "Pausar")

# Función detener canción
def detener_cancion():
    global reproduciendo
    reproduciendo = False

# Ajuste de volumen
def ajustar_volumen(valor):
    global volumen
    volumen = float(valor)
    for sonido in sonidos.values():
        sonido.set_volume(volumen)

# Editor de música
def editor_musica():
    editor_ventana = tk.Toplevel(ventana)
    editor_ventana.title("Editor de Música")
    editor_ventana.config(bg=color_fondo_general)

    teclas_frame = tk.Frame(editor_ventana, bg=color_fondo_general)
    teclas_frame.pack(pady=10)

    notas_seleccionadas = []

    def agregar_nota(nota):
        notas_seleccionadas.append(nota)
        notas_label.config(text=", ".join(notas_seleccionadas))

    teclas_blancas = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
    teclas_negras = [("Do#", 1), ("Re#", 2), ("Fa#", 4), ("Sol#", 5), ("La#", 6)]

    for i, nota in enumerate(teclas_blancas):
        boton_nota = tk.Button(teclas_frame, text=nota, command=lambda n=nota: agregar_nota(n), font=("Arial", 12))
        boton_nota.grid(row=0, column=i, padx=5, pady=5)

    for nota, pos in teclas_negras:
        boton_nota = tk.Button(teclas_frame, text=nota, command=lambda n=nota: agregar_nota(n), font=("Arial", 12))
        boton_nota.grid(row=1, column=pos, padx=5, pady=5)

    notas_label = tk.Label(editor_ventana, text="", bg=color_fondo_general, fg="white", font=("Arial", 12))
    notas_label.pack(pady=10)

    def guardar_cancion():
        nombre_cancion = simpledialog.askstring("Nombre de la canción", "¿Cómo quieres llamar a la canción?", parent=editor_ventana)
        if nombre_cancion:
            canciones[nombre_cancion] = notas_seleccionadas[:]
            canciones_combobox['values'] = list(canciones.keys())
            editor_ventana.destroy()

    guardar_boton = tk.Button(editor_ventana, text="Guardar canción", command=guardar_cancion, font=("Arial", 12))
    guardar_boton.pack(pady=10)

#mejores puntuaciones
def mostrar_mejores_puntuaciones():
    """Muestra las 3 mejores puntuaciones del jugador."""
    if mejores_puntuaciones:
        mensaje = "Mejores Puntuaciones:\n"
        for i, puntuacion in enumerate(mejores_puntuaciones):
            mensaje += f"{i + 1}. {puntuacion}\n"
        messagebox.showinfo("Mejores Puntuaciones", mensaje)
    else:
        messagebox.showinfo("Mejores Puntuaciones", "Aún no hay puntuaciones registradas.")

# Cargar sonido
def cargar_sonido():
    """Carga un archivo de sonido seleccionado por el usuario."""
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de audio", "*.wav;*.mp3")])
    if archivo:
        try:
            sonido = pygame.mixer.Sound(archivo)
            # Asigna el sonido a una nota específica, por ejemplo:
            nota = simpledialog.askstring("Nota", "¿A qué nota le asignamos este sonido?")
            if nota:
                sonidos[nota] = sonido
                print(f"Sonido cargado para la nota {nota}: {archivo}")
        except pygame.error:
            print(f"Error al cargar el sonido: {archivo}")

# crear ventana para estilo grafico
def abrir_ventana_estilo():
    """Abre una nueva ventana para cambiar el estilo gráfico."""
    ventana_estilo = tk.Toplevel(ventana)
    ventana_estilo.title("Estilo Gráfico")
    ventana_estilo.config(bg=color_fondo_general)

    # Combobox para seleccionar temas
    combobox_temas_estilo = ttk.Combobox(ventana_estilo, values=list(temas_color.keys()), state="readonly")
    combobox_temas_estilo.set(combobox_temas.get())  # Establecer tema actual
    combobox_temas_estilo.bind("<<ComboboxSelected>>", lambda eventvent: cambiar_tevent, ema(event, combobox_tstilo))
    combobox_temas_estilo.pack(pady=10)

    # Botones para cambiar colores
    tk.Button(ventana_estilo, text="Color Fondo App", command=cambiar_color_fondo_app).pack(pady=5)
    tk.Button(ventana_estilo, text="Color Fondo Piano", command=cambiar_color_fondo_piano).pack(pady=5)
    tk.Button(ventana_estilo, text="Color Teclas", command=cambiar_color_teclas).pack(pady=5)
    tk.Button(ventana_estilo, text="Colores Aleatorios", command=colores_aleatorios).pack(pady=5)
    tk.Button(ventana_estilo, text="Personalizar Tema", command=personalizar_tema).pack(pady=5)

# Cambiar colores
def cambiar_tema(event):
    """Cambia los colores de la interfaz según el tema seleccionado."""
    tema = combobox_temas.get()
    colores = temas_color[tema]
    ventana.config(bg=colores["fondo_general"])
    canvas.config(bg=colores["fondo_piano"])
    dibujar_teclas(colores["teclas_blancas"], colores["teclas_negras"])

def cambiar_color_fondo_piano():
    """Cambia el color de fondo del piano."""
    global color_fondo_piano
    color_fondo_piano = colorchooser.askcolor()[1]
    canvas.config(bg=color_fondo_piano)

def cambiar_color_fondo_app():
    """Cambia el color de fondo de la aplicación."""
    global color_fondo_general
    color_fondo_general = colorchooser.askcolor()[1]
    ventana.config(bg=color_fondo_general)

def cambiar_color_teclas():
    """Cambia el color de las teclas del piano."""
    global color_teclas_blancas
    color_teclas_blancas = colorchooser.askcolor()[1]
    dibujar_teclas(color_teclas_blancas, color_teclas_negras)

def colores_aleatorios():
    """Asigna colores aleatorios a la interfaz."""
    global color_teclas_blancas, color_fondo_piano, color_fondo_general
    color_teclas_blancas = random.choice(["white", "pink", "lightcyan", "lavender", "lightyellow",
                                        "lightgreen", "thistle", "plum", "seashell", "beige"])
    color_fondo_piano = random.choice(["lightblue", "peachpuff", "lavenderblush", "lemonchiffon", "mistyrose",
                                    "honeydew", "mintcream", "papayawhip", "lightgoldenrodyellow", "aliceblue"])
    color_fondo_general = random.choice(["black", "darkslategray", "midnightblue", "darkmagenta",
                                        "darkred", "indigo", "darkolivegreen", "saddle"])
    ventana.config(bg=color_fondo_general)
    canvas.config(bg=color_fondo_piano)
    dibujar_teclas(color_teclas_blancas, color_teclas_negras)

def personalizar_tema():
    """Permite personalizar los colores de un tema predeterminado."""
    tema_seleccionado = combobox_temas.get()
    if tema_seleccionado in temas_color:
        colores = temas_color[tema_seleccionado]
        colores["fondo_general"] = colorchooser.askcolor(title="Fondo de la aplicación", initialcolor=colores["fondo_general"])[1]
        colores["fondo_piano"] = colorchooser.askcolor(title="Fondo del piano", initialcolor=colores["fondo_piano"])[1]
        colores["teclas_blancas"] = colorchooser.askcolor(title="Teclas blancas", initialcolor=colores["teclas_blancas"])[1]
        colores["teclas_negras"] = colorchooser.askcolor(title="Teclas negras", initialcolor=colores["teclas_negras"])[1]
        cambiar_tema(None)  # Actualizar la interfaz con los nuevos colores

# Crear teclas
def dibujar_teclas():
    canvas.delete("all")
    notas_blancas = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
    notas_negras = [("Do#", 1), ("Re#", 2), ("Fa#", 4), ("Sol#", 5), ("La#", 6)]
    for i, nota in enumerate(notas_blancas):
        x = 20 + i * 100
        canvas.create_rectangle(x, 150, x + 90, 350, fill=color_teclas_blancas, tags=nota)
        canvas.tag_bind(nota, "<Button-1>", lambda e, n=nota: sonidos[n].play())
    for nota, pos in notas_negras:
        x = 20 + pos * 100 - 30
        canvas.create_rectangle(x, 150, x + 60, 270, fill=color_teclas_negras, tags=nota)

# Crear ventana
ventana = tk.Tk()
ventana.title("Piano Test")
ventana.config(bg=color_fondo_general)
ventana.geometry("900x600")

# Crear Combobox para seleccionar temas
combobox_temas = ttk.Combobox(ventana, values=list(temas_color.keys()), state="readonly")
combobox_temas.set("Estándar")  # Establecer tema inicial
combobox_temas.bind("<<ComboboxSelected>>", cambiar_tema)

# Menú superior
menu_bar = tk.Menu(ventana)
ajustes_menu = tk.Menu(menu_bar, tearoff=0)
ajustes_menu.add_command(label="Salir", command=ventana.quit)
ajustes_menu.add_separator()
ajustes_menu.add_command(label="Editor de Música", command=editor_musica)
ajustes_menu.add_command(label="Cargar Sonido", command=cargar_sonido)
ajustes_menu.add_command(label="Exportar a MP3", command=lambda: exportar_como_mp3(list(canciones.keys())[-1]))
ajustes_menu.add_separator()
ajustes_menu.add_command(label="Colores Aleatorios", command=colores_aleatorios)
ajustes_menu.add_command(label="Color Fondo App", command=cambiar_color_fondo_app)
ajustes_menu.add_command(label="Color Fondo Piano", command=cambiar_color_fondo_piano)
ajustes_menu.add_command(label="Color Teclas", command=cambiar_color_teclas)
ajustes_menu.add_separator()
ajustes_menu.add_command(label="Juego de velocidad", command=iniciar_juego)
def abrir_ventana_karaoke():
    """Abre una nueva ventana para el modo karaoke."""
    ventana_karaoke = tk.Toplevel(ventana)
    ventana_karaoke.title("Modo Karaoke")
    ventana_karaoke.config(bg=color_fondo_general)

    # Etiqueta para mostrar el estado del karaoke
    estado_label = tk.Label(ventana_karaoke, text="Modo Karaoke", font=("Arial", 14, "bold"), bg=color_fondo_general, fg="white")
    estado_label.pack(pady=10)

    # Botón para activar/desactivar el karaoke
    def toggle_karaoke():
        global reproduciendo
        if not reproduciendo:
            reproducir_cancion()

    boton_karaoke = tk.Button(ventana_karaoke, text="Iniciar Karaoke", command=toggle_karaoke, bg="#4CAF50", fg="white")
    boton_karaoke.pack(pady=10)

    # Mostrar la letra actual
    letra_actual_label = tk.Label(ventana_karaoke, text="", font=("Arial", 12), bg=color_fondo_general, fg="white", wraplength=300)
    letra_actual_label.pack(pady=10)

    # Mostrar la puntuación
    puntuacion_label = tk.Label(ventana_karaoke, text="Puntuación: 0", font=("Arial", 12), bg=color_fondo_general, fg="white")
    puntuacion_label.pack(pady=5)

    # Selector de canciones
    canciones_label = tk.Label(ventana_karaoke, text="Selecciona una canción:", bg=color_fondo_general, fg="white")
    canciones_label.pack(pady=5)
    
    canciones_combobox_karaoke = ttk.Combobox(ventana_karaoke, values=list(canciones.keys()), state="readonly")
    if len(canciones) > 0:
        canciones_combobox_karaoke.set(list(canciones.keys())[0])
    canciones_combobox_karaoke.pack(pady=5)

ajustes_menu.add_command(label="Karaoke", command=abrir_ventana_karaoke)
ajustes_menu.add_separator()
ajustes_menu.add_radiobutton(label="Modo Ratón", variable=tk.StringVar(value=modo_juego), value="raton", command=lambda: cambiar_modo_juego("raton"))
ajustes_menu.add_radiobutton(label="Modo Teclado", variable=tk.StringVar(value=modo_juego), value="teclado", command=lambda: cambiar_modo_juego("teclado"))
ajustes_menu.add_separator()
ajustes_menu.add_command(label="Puntuacion", command=mostrar_mejores_puntuaciones)
ajustes_menu.add_command(label="Tutorial", command=mostrar_tutorial)
ajustes_menu.add_separator()
ajustes_menu.add_command(label="Estilo Gráfico", command=abrir_ventana_estilo)
menu_bar.add_cascade(label="Ajustes", menu=ajustes_menu)
ventana.config(menu=menu_bar)

# Volumen
volumen_slider = tk.Scale(ventana, from_=0, to=1, resolution=0.1, orient="horizontal", label="Volumen", command=ajustar_volumen, font=("Arial", 12))
volumen_slider.set(0.6)
volumen_slider.pack()

# Piano
canvas = tk.Canvas(ventana, width=850, height=400, bg=color_fondo_piano)
canvas.pack(pady=10)
dibujar_teclas()

# Etiqueta para mostrar el puntaje
puntaje_label = tk.Label(ventana, text="Puntaje: 0", font=("Arial", 14), bg=color_fondo_general, fg="white")

# Frame para ajustes
ajustes_frame = tk.Frame(ventana, bg=color_fondo_general)
ajustes_frame.pack(pady=10)

# Canciones
canciones_combobox = ttk.Combobox(ventana, values=list(canciones.keys()), font=("Arial", 14), width=30)
canciones_combobox.pack(pady=5)

# Botones alineados
frame_botones = tk.Frame(ventana, bg=color_fondo_general)
frame_botones.pack(pady=10)
tk.Button(frame_botones, text="Reproducir", command=lambda: Thread(target=reproducir_cancion).start(), font=("Arial", 12), width=15, height=2, padx=10, pady=5).pack(side="left", padx=10)
boton_pausa = tk.Button(frame_botones, text="Pausar", command=pausar_o_reanudar, font=("Arial", 12), width=15, height=2, padx=10, pady=5)
boton_pausa.pack(side="left", padx=10)
tk.Button(frame_botones, text="Detener", command=detener_cancion, font=("Arial", 12), width=15, height=2, padx=10, pady=5).pack(side="left", padx=10)

# Texto divertido
tk.Label(ventana, text="¡Disfruta creando música! 🎶", font=("Arial", 14), bg=color_fondo_general).pack(pady=10)

ventana.mainloop()