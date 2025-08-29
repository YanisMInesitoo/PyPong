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

raqueta = Raqueta(canvas, 'blue')
pelota = Pelota(canvas, raqueta, 'red')

while 1:
    if pelota.golpea_fondo == False and raqueta.empezado == True:
        pelota.dibujar()
        raqueta.dibujar()
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)