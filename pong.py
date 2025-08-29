""" 
    PyPong
    Juego de Pong escrito en Python con Tkinter
    Autor: ItzYanisMine
    Fecha: Julio 2025
    Youtube: https://www.youtube.com/@itzyanismine.oficial
    Reddit: www.reddit.com/user/ItzYanisMinesitoo12/

    Creditos a:
       nadie xd

    Version: 1.0
    Licencia: GPLv3
    Descripcion: Un simple juego de Pong donde controlas una raqueta para evitar que la pelota toque el fondo.
    Instrucciones:
       - Usa las flechas izquierda y derecha para mover la raqueta.
       - Haz clic con el ratón para iniciar el juego.
       - Evita que la pelota toque el fondo de la ventana.
    Mejoras futuras:
         - Añadir puntuacion
         - Mejorar la interfaz grafica
         - Añadir niveles de dificultad
         - Sonidos y musica de fondo
         - Modo multijugador
         - Guardar la puntuacion mas alta
    
"""

from tkinter import *
import random
import time
from pelota import Pelota
from raqueta import Raqueta

tk = Tk()
tk.title("PyPong")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

def leer_puntuacion_mas_alta():
    try:
        with open('hi-score.txt', 'r') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def guardar_puntuacion_mas_alta(puntuacion):
    with open('hi-score.txt', 'w') as file:
        file.write(str(puntuacion))

puntuacion_mas_alta = leer_puntuacion_mas_alta()
score_display = canvas.create_text(450, 20, text="Score: 0", font=('Arial', 16), fill='black')
hi_score_display = canvas.create_text(450, 40, text="Hi-Score: " + str(puntuacion_mas_alta), font=('Arial', 12), fill='gray')

puntuacion = 0
score_display = canvas.create_text(450, 20, text="Score: " + str(puntuacion), font=('Arial', 16), fill='black')

raqueta = Raqueta(canvas, 'blue')
pelota = Pelota(canvas, raqueta, 'red')

while 1:
    if pelota.golpea_fondo == False and raqueta.empezado == True:
        pelota.dibujar()
        raqueta.dibujar()
        canvas.itemconfig(score_display, text="Score: " + str(pelota.puntuacion))
    
    if pelota.golpea_fondo == True and pelota.puntuacion > puntuacion_mas_alta:
        puntuacion_mas_alta = pelota.puntuacion
        canvas.itemconfig(hi_score_display, text="Hi-Score: " + str(puntuacion_mas_alta))
        guardar_puntuacion_mas_alta(puntuacion_mas_alta)

    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)