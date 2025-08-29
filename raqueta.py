from tkinter import *

class Raqueta:
    def __init__(self, canvas, color, jugador):
        self.canvas = canvas
        self.jugador = jugador
        self.id = canvas.create_rectangle(0, 0, 10, 100, fill=color)
        self.canvas_height = self.canvas.winfo_height()
        self.y = 0

        if self.jugador == 1:
            self.canvas.move(self.id, 50, 150)
            self.canvas.bind_all('<KeyPress-w>', self.ir_arriba)
            self.canvas.bind_all('<KeyPress-s>', self.ir_abajo)
        elif self.jugador == 2:
            self.canvas.move(self.id, 450, 150)
            self.canvas.bind_all('<KeyPress-Up>', self.ir_arriba)
            self.canvas.bind_all('<KeyPress-Down>', self.ir_abajo)

    def dibujar(self):
        self.canvas.move(self.id, 0, self.y)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y = 0
        elif pos[3] >= self.canvas_height:
            self.y = 0

    def ir_arriba(self, evt):
        self.y = -3

    def ir_abajo(self, evt):
        self.y = 3