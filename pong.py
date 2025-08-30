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

def dibujar_degradado(canvas, color1, color2):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    for i in range(height):
        r1, g1, b1 = canvas.winfo_rgb(color1)
        r2, g2, b2 = canvas.winfo_rgb(color2)
        r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
        r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256
        r = int(r1 + (r2 - r1) * i / height)
        g = int(g1 + (g2 - g1) * i / height)
        b = int(b1 + (b2 - b1) * i / height)
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, i, width, i, fill=color)

def iniciar_juego(ancho, alto, modo_juego):
    tk.geometry(f"{ancho}x{alto}")
    canvas.config(width=ancho, height=alto)
    canvas.delete("all")
    dibujar_degradado(canvas, "#00008B", "#4169E1")

    if modo_juego == 1:
        raqueta = Raqueta(canvas, 'blue', 1)
        pelota = Pelota(canvas, [raqueta], 'white', 1)
        score_display = canvas.create_text(ancho * 0.5, 20, text="Score: 0", font=('Arial', 16), fill='white')
        while 1:
            if raqueta.empezado:
                pelota.dibujar()
            raqueta.dibujar()
            canvas.itemconfig(score_display, text="Score: " + str(pelota.puntuacion_jugador1))
            if pelota.golpea_fondo == True:
                pelota.golpea_fondo = False
                pelota.canvas.coords(pelota.id, ancho // 2 - 7, alto // 2 - 7, ancho // 2 + 8, alto // 2 + 8)
                empezar = [-3, -2, -1, 1, 2, 3]
                random.shuffle(empezar)
                pelota.x = empezar[0]
                pelota.y = -3
                raqueta.empezado = False
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

    elif modo_juego == 2:
        puntuacion_j1_display = canvas.create_text(ancho * 0.1, 20, text="J1: 0", font=('Arial', 16), fill='white')
        puntuacion_j2_display = canvas.create_text(ancho * 0.9, 20, text="J2: 0", font=('Arial', 16), fill='white')
        raqueta1 = Raqueta(canvas, 'blue', 2, "humano", 1)
        raqueta2 = Raqueta(canvas, 'red', 2, "humano", 2)
        pelota = Pelota(canvas, [raqueta1, raqueta2], 'white', 2)
        while 1:
            pelota.dibujar()
            raqueta1.dibujar()
            raqueta2.dibujar()
            canvas.itemconfig(puntuacion_j1_display, text="J1: " + str(pelota.puntuacion_jugador1))
            canvas.itemconfig(puntuacion_j2_display, text="J2: " + str(pelota.puntuacion_jugador2))
            if pelota.golpea_fondo == True:
                pelota.golpea_fondo = False
                pelota.canvas.coords(pelota.id, ancho // 2 - 7, alto // 2 - 7, ancho // 2 + 8, alto // 2 + 8)
                empezar = [-3, -2, -1, 1, 2, 3]
                random.shuffle(empezar)
                pelota.x = empezar[0]
                pelota.y = -3
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

    elif modo_juego == 3:
        raqueta_jugador = Raqueta(canvas, 'blue', 3, "humano")
        raqueta_ia = Raqueta(canvas, 'red', 3, "ia")
        pelota = Pelota(canvas, [raqueta_jugador, raqueta_ia], 'white', 3)
        score_display_j1 = canvas.create_text(ancho * 0.5, 20, text="Score: 0", font=('Arial', 16), fill='white')
        
        while 1:
            if raqueta_jugador.empezado:
                pelota_pos = pelota.canvas.coords(pelota.id)
                raqueta_ia.dibujar(pelota_pos)
                pelota.dibujar()
            raqueta_jugador.dibujar()
            
            canvas.itemconfig(score_display_j1, text="Score: " + str(pelota.puntuacion_jugador1))
            
            if pelota.golpea_fondo == True:
                pelota.golpea_fondo = False
                pelota.canvas.coords(pelota.id, ancho // 2 - 7, alto // 2 - 7, ancho // 2 + 8, alto // 2 + 8)
                empezar = [-3, -2, -1, 1, 2, 3]
                random.shuffle(empezar)
                pelota.x = empezar[0]
                pelota.y = -3
                raqueta_jugador.empezado = False
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

def pantalla_de_inicio():
    canvas.delete("all")
    dibujar_degradado(canvas, "#303030", "#101010")
    
    canvas.create_text(250, 50, text="PyPong", font=('Arial', 50, 'bold'), fill="white")
    canvas.create_text(250, 120, text="Selecciona el modo y la resolución", font=('Arial', 14), fill="white")
    
    button_style = {'font': ('Arial', 14), 'bg': '#4CAF50', 'fg': 'white', 'activebackground': '#45a049', 'activeforeground': 'white', 'relief': 'raised', 'bd': 3}

    boton_1p = Button(tk, text="1 Jugador", command=lambda: mostrar_opciones_resolucion(1), **button_style)
    canvas.create_window(80, 180, window=boton_1p, width=150, height=40)
    
    boton_vs_ia = Button(tk, text="U vs. AI", command=lambda: mostrar_opciones_resolucion(3), **button_style)
    canvas.create_window(250, 180, window=boton_vs_ia, width=150, height=40)

    boton_2p = Button(tk, text="2 Jugadores", command=lambda: mostrar_opciones_resolucion(2), **button_style)
    canvas.create_window(420, 180, window=boton_2p, width=150, height=40)
    
def mostrar_opciones_resolucion(modo_juego):
    canvas.delete("all")
    dibujar_degradado(canvas, "#303030", "#101010")
    
    canvas.create_text(250, 50, text="Selecciona Resolución", font=('Arial', 24, 'bold'), fill="white")

    resoluciones = [(500, 400), (640, 480), (800, 600)]
    y_pos = 150
    for ancho, alto in resoluciones:
        boton = Button(tk, text=f"{ancho}x{alto}", command=lambda a=ancho, b=alto: iniciar_juego(a, b, modo_juego), font=('Arial', 14), bg='#4CAF50', fg='white')
        canvas.create_window(250, y_pos, window=boton, width=150, height=40)
        y_pos += 60

pantalla_de_inicio()
tk.mainloop()