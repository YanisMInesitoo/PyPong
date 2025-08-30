from tkinter import *
import random

class Pelota:
    def __init__(self, canvas, raquetas, color, modo_juego):
        self.canvas = canvas
        self.raquetas = raquetas
        self.modo_juego = modo_juego
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        
        if self.modo_juego == 1 or self.modo_juego == 3:
            self.canvas.move(self.id, 245, 100)
            self.y = -3
        elif self.modo_juego == 2:
            self.canvas.move(self.id, 245, 150)
            self.y = -3

        empezar = [-3, -2, -1, 1, 2, 3]
        random.shuffle(empezar)
        self.x = empezar[0]
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.golpea_fondo = False
        self.puntuacion_jugador1 = 0
        self.puntuacion_jugador2 = 0

    def golpea_raqueta(self, pos):
        if self.modo_juego == 1:
            raqueta_pos = self.canvas.coords(self.raquetas[0].id)
            if pos[2] >= raqueta_pos[0] and pos[0] <= raqueta_pos[2]:
                if pos[3] >= raqueta_pos[1] and pos[3] <= raqueta_pos[3]:
                    return True
        elif self.modo_juego == 2:
            raqueta1_pos = self.canvas.coords(self.raquetas[0].id)
            if pos[2] >= raqueta1_pos[0] and pos[0] <= raqueta1_pos[2]:
                if pos[3] >= raqueta1_pos[1] and pos[3] <= raqueta1_pos[3]:
                    return True, 1
            raqueta2_pos = self.canvas.coords(self.raquetas[1].id)
            if pos[2] >= raqueta2_pos[0] and pos[0] <= raqueta2_pos[2]:
                if pos[3] >= raqueta2_pos[1] and pos[3] <= raqueta2_pos[3]:
                    return True, 2
        elif self.modo_juego == 3:
            raqueta1_pos = self.canvas.coords(self.raquetas[0].id) # Jugador humano
            raqueta2_pos = self.canvas.coords(self.raquetas[1].id) # IA
            if pos[2] >= raqueta1_pos[0] and pos[0] <= raqueta1_pos[2]:
                if pos[3] >= raqueta1_pos[1] and pos[3] <= raqueta1_pos[3]:
                    return True, 1
            if pos[2] >= raqueta2_pos[0] and pos[0] <= raqueta2_pos[2]:
                if pos[3] >= raqueta2_pos[1] and pos[3] <= raqueta2_pos[3]:
                    return True, 2
        return False, 0

    def dibujar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        # Lógica de rebote en la parte superior e inferior
        if pos[1] <= 0:
            self.y = abs(self.y)
        if pos[3] >= self.canvas_height:
            if self.modo_juego == 1:
                self.golpea_fondo = True
                self.canvas.create_text(self.canvas_width/2, self.canvas_height/2, font=('Barbieri Book', 34), text='Fin del Juego :c', state='normal')
            else:
                self.y = -abs(self.y)
        
        # Lógica de rebote en los lados y puntuación
        if self.modo_juego == 1 or self.modo_juego == 3: # En estos modos, las raquetas estan arriba y abajo
            if self.golpea_raqueta(pos)[0]: # Chequea colisión con raqueta de jugador
                self.y = -abs(self.y)
                self.puntuacion_jugador1 += 1
            if self.modo_juego == 3:
                if self.golpea_raqueta(pos)[0] and self.golpea_raqueta(pos)[1] == 2: # Chequea colisión con raqueta de IA
                     self.y = -abs(self.y)
            if pos[0] <= 0 or pos[2] >= self.canvas_width:
                self.x = -self.x
        elif self.modo_juego == 2: # En este modo, las raquetas están a los lados
            rebotar, jugador_que_reboto = self.golpea_raqueta(pos)
            if rebotar:
                if jugador_que_reboto == 1:
                    self.x = abs(self.x)
                elif jugador_que_reboto == 2:
                    self.x = -abs(self.x)
            
            if pos[0] <= 0:
                self.puntuacion_jugador2 += 1
                self.golpea_fondo = True # ¡CORREGIDO!
            if pos[2] >= self.canvas_width:
                self.puntuacion_jugador1 += 1
                self.golpea_fondo = True # ¡CORREGIDO!