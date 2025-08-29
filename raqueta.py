from tkinter import *

class Raqueta:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.empezado = False
        self.canvas.bind_all('<KeyPress-Left>', self.ir_izq)
        self.canvas.bind_all('<KeyPress-Right>', self.ir_der)
        self.canvas.bind_all('<Button-1>', self.empezar_juego)

    def dibujar(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        elif pos[0] < 0:
            self.x = 1
        elif pos[2] == self.canvas_width:
            self.x = 0
        elif pos[2] > self.canvas_width:
            self.x = -1

    def ir_izq(self, evt):
        self.x = -2

    def ir_der(self, evt):
        self.x = 2

    def empezar_juego(self, evt):
        self.empezado = True