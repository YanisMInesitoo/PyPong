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
import json
from pelota import Pelota
from raqueta import Raqueta

tk = Tk()
tk.title("PyPong")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# --- Sistema de Monedas, Logros y Guardado ---
monedas = 0
puntuacion_maxima = 0
items_comprados = ["raqueta_azul", "pelota_blanca"]
tienda_items = {
    "raqueta_azul": {"nombre": "Raqueta Azul", "precio": 0, "tipo": "raqueta", "color": "blue"},
    "raqueta_verde": {"nombre": "Raqueta Verde", "precio": 100, "tipo": "raqueta", "color": "green"},
    "raqueta_dorada": {"nombre": "Raqueta Dorada", "precio": 500, "tipo": "raqueta", "color": "gold"},
    "pelota_blanca": {"nombre": "Pelota Blanca", "precio": 0, "tipo": "pelota", "color": "white"},
    "pelota_amarilla": {"nombre": "Pelota Amarilla", "precio": 75, "tipo": "pelota", "color": "yellow"},
    "pelota_rosa": {"nombre": "Pelota Rosa", "precio": 150, "tipo": "pelota", "color": "pink"},
    "pelota_roja": {"nombre": "Pelota Roja", "precio": 250, "tipo": "pelota", "color": "red"}
}

logros = {
    "primer_golpe": {"nombre": "Primer Golpe", "descripcion": "Golpea la pelota una vez", "completado": False},
    "cien_puntos": {"nombre": "Experto en rebotes", "descripcion": "Consigue 100 puntos en un solo juego", "completado": False},
    "comprador_novato": {"nombre": "Mi primera compra", "descripcion": "Compra un artículo en la tienda", "completado": False},
    "coleccionista": {"nombre": "Coleccionista", "descripcion": "Compra todos los artículos de la tienda", "completado": False}
}

def guardar_progreso():
    datos = {
        "monedas": monedas,
        "items": items_comprados,
        "logros": logros,
        "puntuacion_maxima": puntuacion_maxima
    }
    with open("progreso.json", "w") as archivo:
        json.dump(datos, archivo)

def cargar_progreso():
    global monedas, items_comprados, logros, puntuacion_maxima
    try:
        with open("progreso.json", "r") as archivo:
            # Revisa si el archivo está vacío
            contenido = archivo.read()
            if contenido:
                datos = json.loads(contenido)
                monedas = datos.get("monedas", 0)
                items_comprados = datos.get("items", [])
                logros_guardados = datos.get("logros", {})
                puntuacion_maxima = datos.get("puntuacion_maxima", 0)
                for key, value in logros_guardados.items():
                    if key in logros:
                        logros[key]["completado"] = value.get("completado", False)
            else:
                print("Archivo de progreso vacío. Se creará uno nuevo.")
    except FileNotFoundError:
        print("Archivo de progreso no encontrado. Se creará uno nuevo.")
    except json.JSONDecodeError:
        print("Error al leer el archivo de progreso. Se creará uno nuevo.")
    
    # Asegúrate de que el estado inicial se establece si el archivo no existe o está mal
    if "raqueta_azul" not in items_comprados:
        items_comprados.append("raqueta_azul")
    if "pelota_blanca" not in items_comprados:
        items_comprados.append("pelota_blanca")

def chequear_logro(logro_id):
    if not logros[logro_id]["completado"]:
        logros[logro_id]["completado"] = True
        guardar_progreso()
        mostrar_notificacion_logro(logros[logro_id]["nombre"])

def chequear_logro_coleccionista():
    items_disponibles = [item_id for item_id, item_info in tienda_items.items() if item_info["precio"] > 0]
    items_comprados_pagados = [item_id for item_id in items_comprados if tienda_items[item_id]["precio"] > 0]
    if len(items_comprados_pagados) == len(items_disponibles):
        chequear_logro("coleccionista")

def mostrar_notificacion_logro(nombre_logro):
    global canvas
    canvas.create_rectangle(150, 150, 350, 250, fill="yellow", outline="black")
    canvas.create_text(250, 180, text="¡LOGRO DESBLOQUEADO!", font=('Arial', 12, 'bold'))
    canvas.create_text(250, 210, text=nombre_logro, font=('Arial', 16, 'bold'))
    tk.update()
    time.sleep(2)
    canvas.delete("all")
    pantalla_de_inicio()

def ganar_monedas(cantidad):
    global monedas
    monedas += cantidad

def comprar_item(item_id):
    global monedas
    item = tienda_items[item_id]
    if monedas >= item["precio"] and item_id not in items_comprados:
        monedas -= item["precio"]
        items_comprados.append(item_id)
        guardar_progreso()
        chequear_logro("comprador_novato")
        chequear_logro_coleccionista()
        pantalla_tienda()
# --- Fin Sistema de Monedas, Logros y Guardado ---

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
    global puntuacion_maxima
    tk.geometry(f"{ancho}x{alto}")
    canvas.config(width=ancho, height=alto)
    canvas.delete("all")
    dibujar_degradado(canvas, "#00008B", "#4169E1")

    monedas_display = canvas.create_text(ancho * 0.9, 20, text="Monedas: " + str(monedas), font=('Arial', 16), fill='white')
    puntuacion_maxima_display = canvas.create_text(ancho * 0.5, 50, text="Puntuación máxima: " + str(puntuacion_maxima), font=('Arial', 12), fill='white')
    
    # Colores por defecto y seleccionados
    raqueta_color = "blue"
    pelota_color = "white"
    for item_id in items_comprados:
        if tienda_items[item_id]["tipo"] == "raqueta":
            raqueta_color = tienda_items[item_id]["color"]
        elif tienda_items[item_id]["tipo"] == "pelota":
            pelota_color = tienda_items[item_id]["color"]

    juego_en_curso = True

    if modo_juego == 1:
        raqueta = Raqueta(canvas, raqueta_color, 1)
        pelota = Pelota(canvas, [raqueta], pelota_color, 1)
        score_display = canvas.create_text(ancho * 0.5, 20, text="Score: 0", font=('Arial', 16), fill='white')
        
        while juego_en_curso:
            if raqueta.empezado:
                pelota.dibujar()
                ganar_monedas(1)
            raqueta.dibujar()
            canvas.itemconfig(score_display, text="Score: " + str(pelota.puntuacion_jugador1))
            canvas.itemconfig(monedas_display, text="Monedas: " + str(monedas))
            if pelota.golpea_fondo == True:
                juego_en_curso = False
                if pelota.puntuacion_jugador1 > puntuacion_maxima:
                    puntuacion_maxima = pelota.puntuacion_jugador1
                if pelota.puntuacion_jugador1 >= 100:
                    chequear_logro("cien_puntos")
                guardar_progreso()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

    elif modo_juego == 2:
        puntuacion_j1_display = canvas.create_text(ancho * 0.1, 20, text="J1: 0", font=('Arial', 16), fill='white')
        puntuacion_j2_display = canvas.create_text(ancho * 0.9, 20, text="J2: 0", font=('Arial', 16), fill='white')
        raqueta1 = Raqueta(canvas, raqueta_color, 2, "humano", 1)
        raqueta2 = Raqueta(canvas, raqueta_color, 2, "humano", 2)
        pelota = Pelota(canvas, [raqueta1, raqueta2], pelota_color, 2)
        
        while juego_en_curso:
            pelota.dibujar()
            raqueta1.dibujar()
            raqueta2.dibujar()
            ganar_monedas(1)
            canvas.itemconfig(puntuacion_j1_display, text="J1: " + str(pelota.puntuacion_jugador1))
            canvas.itemconfig(puntuacion_j2_display, text="J2: " + str(pelota.puntuacion_jugador2))
            canvas.itemconfig(monedas_display, text="Monedas: " + str(monedas))
            if pelota.golpea_fondo == True:
                juego_en_curso = False
                guardar_progreso()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)

    elif modo_juego == 3:
        raqueta_jugador = Raqueta(canvas, raqueta_color, 3, "humano")
        raqueta_ia = Raqueta(canvas, "red", 3, "ia")
        pelota = Pelota(canvas, [raqueta_jugador, raqueta_ia], pelota_color, 3)
        score_display_j1 = canvas.create_text(ancho * 0.5, 20, text="Score: 0", font=('Arial', 16), fill='white')
        
        while juego_en_curso:
            if raqueta_jugador.empezado:
                pelota_pos = pelota.canvas.coords(pelota.id)
                raqueta_ia.dibujar(pelota_pos)
                pelota.dibujar()
                ganar_monedas(1)
            raqueta_jugador.dibujar()
            
            canvas.itemconfig(score_display_j1, text="Score: " + str(pelota.puntuacion_jugador1))
            canvas.itemconfig(monedas_display, text="Monedas: " + str(monedas))
            
            if pelota.golpea_fondo == True:
                juego_en_curso = False
                if pelota.puntuacion_jugador1 > puntuacion_maxima:
                    puntuacion_maxima = pelota.puntuacion_jugador1
                if pelota.puntuacion_jugador1 >= 100:
                    chequear_logro("cien_puntos")
                guardar_progreso()
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
    
    pantalla_de_inicio()

# --- Pantalla de la Tienda ---
def pantalla_tienda():
    canvas.delete("all")
    dibujar_degradado(canvas, "#303030", "#101010")

    canvas.create_text(250, 50, text="TIENDA", font=('Arial', 40, 'bold'), fill="white")
    monedas_display = canvas.create_text(400, 20, text="Monedas: " + str(monedas), font=('Arial', 16), fill='yellow')
    
    y_pos = 120
    for item_id, item_info in tienda_items.items():
        if item_info["precio"] == 0:
            continue
        
        estado = "COMPRADO" if item_id in items_comprados else f"{item_info['precio']} MONEDAS"
        
        canvas.create_text(150, y_pos, text=item_info["nombre"], font=('Arial', 14), fill='white', anchor='w')
        
        if item_id in items_comprados:
            boton = Button(tk, text="COMPRADO", state="disabled", font=('Arial', 12))
        else:
            boton = Button(tk, text=estado, command=lambda id=item_id: comprar_item(id), font=('Arial', 12))
        
        canvas.create_window(400, y_pos, window=boton, width=120)
        y_pos += 50
    
    boton_volver = Button(tk, text="Volver", command=pantalla_de_inicio, font=('Arial', 14))
    canvas.create_window(250, y_pos + 30, window=boton_volver, width=150)
    
def pantalla_logros():
    canvas.delete("all")
    dibujar_degradado(canvas, "#303030", "#101010")
    
    canvas.create_text(250, 50, text="LOGROS", font=('Arial', 40, 'bold'), fill="white")
    
    y_pos = 120
    for logro_id, logro_info in logros.items():
        estado = "DESBLOQUEADO" if logro_info["completado"] else "BLOQUEADO"
        color = "green" if logro_info["completado"] else "red"
        
        canvas.create_text(150, y_pos, text=logro_info["nombre"], font=('Arial', 14), fill='white', anchor='w')
        canvas.create_text(150, y_pos + 20, text=logro_info["descripcion"], font=('Arial', 10), fill='gray', anchor='w')
        canvas.create_text(400, y_pos, text=estado, font=('Arial', 12), fill=color)
        y_pos += 60
    
    boton_volver = Button(tk, text="Volver", command=pantalla_de_inicio, font=('Arial', 14))
    canvas.create_window(250, y_pos + 30, window=boton_volver, width=150)

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
    
    boton_tienda = Button(tk, text="TIENDA", command=pantalla_tienda, font=('Arial', 14), bg='purple', fg='white')
    canvas.create_window(150, 250, window=boton_tienda, width=150, height=40)
    
    boton_logros = Button(tk, text="LOGROS", command=pantalla_logros, font=('Arial', 14), bg='gold', fg='black')
    canvas.create_window(350, 250, window=boton_logros, width=150, height=40)

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

cargar_progreso()
pantalla_de_inicio()
tk.mainloop()