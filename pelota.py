from tkinter import *
import random

class Pelota:
    def __init__(self, canvas, raqueta, color):
        self.canvas = canvas
        self.raqueta = raqueta
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        empezar = [-3, -2, -1, 1, 2, 3]
        random.shuffle(empezar)
        self.x = empezar[0]
        self.y = -3
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.golpea_fondo = False
        self.puntuacion = 0

    def golpea_raqueta(self, pos):
        raqueta_pos = self.canvas.coords(self.raqueta.id)
        if pos[2] >= raqueta_pos[0] and pos[0] <= raqueta_pos[2]:
            if pos[3] >= raqueta_pos[1] and pos[3] <= raqueta_pos[3]:
                return True
                self.x += self.raqueta.x
        return False

    def dibujar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 2
        if pos[3] >= self.canvas_height:
            self.golpea_fondo = True
            self.canvas.create_text(250, 200, font=('Barbieri Book', 34), text='Fin del Juego :c', state='normal')
        
        if self.golpea_raqueta(pos) == True:
            self.y = -2
            self.puntuacion += 1  # Aumenta la puntuación

        if self.golpea_raqueta(pos) == True:
            self.y = -2
        if pos[0] <= 0:
            self.x = 2
        if pos[2] >= self.canvas_width:
            self.x = -2