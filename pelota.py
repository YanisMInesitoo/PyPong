from tkinter import *
import random

class Pelota:
    def __init__(self, canvas, raqueta1, raqueta2, color):
        self.canvas = canvas
        self.raqueta1 = raqueta1
        self.raqueta2 = raqueta2
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 150)
        empezar = [-3, -2, -1, 1, 2, 3]
        random.shuffle(empezar)
        self.x = empezar[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.golpea_fondo = False
        self.puntuacion_jugador1 = 0
        self.puntuacion_jugador2 = 0

    def golpea_raqueta(self, pos):
        raqueta1_pos = self.canvas.coords(self.raqueta1.id)
        if pos[2] >= raqueta1_pos[0] and pos[0] <= raqueta1_pos[2]:
            if pos[3] >= raqueta1_pos[1] and pos[3] <= raqueta1_pos[3]:
                return True, 1
        raqueta2_pos = self.canvas.coords(self.raqueta2.id)
        if pos[2] >= raqueta2_pos[0] and pos[0] <= raqueta2_pos[2]:
            if pos[3] >= raqueta2_pos[1] and pos[3] <= raqueta2_pos[3]:
                return True, 2
        return False, 0

    def dibujar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        # Rebotes en el techo y el suelo
        if pos[1] <= 0:
            self.y = abs(self.y)
        if pos[3] >= self.canvas_height:
            self.y = -abs(self.y)

        # Rebotes en las raquetas
        rebotar, jugador_que_reboto = self.golpea_raqueta(pos)
        if rebotar:
            if jugador_que_reboto == 1:
                self.x = abs(self.x)
            elif jugador_que_reboto == 2:
                self.x = -abs(self.x)

        # Puntos y fin de juego
        if pos[0] <= 0:
            self.puntuacion_jugador2 += 1
            self.golpea_fondo = True
        if pos[2] >= self.canvas_width:
            self.puntuacion_jugador1 += 1
            self.golpea_fondo = True