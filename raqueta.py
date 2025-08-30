from tkinter import *

class Raqueta:
    def __init__(self, canvas, color, modo_juego, tipo="humano", jugador=None):
        self.canvas = canvas
        self.modo_juego = modo_juego
        self.tipo = tipo
        self.jugador = jugador
        self.empezado = False
        self.color = color

        if self.modo_juego == 1 or self.modo_juego == 3:
            self.id = canvas.create_rectangle(0, 0, 100, 10, fill=self.color)
            self.canvas.move(self.id, 200, 300)
            self.x = 0
            if self.tipo == "humano":
                self.canvas.bind_all('<KeyPress-Left>', self.ir_izq)
                self.canvas.bind_all('<KeyPress-Right>', self.ir_der)
                self.canvas.bind_all('<Button-1>', self.empezar_juego)
        elif self.modo_juego == 2:
            self.id = canvas.create_rectangle(0, 0, 10, 100, fill=self.color)
            if self.jugador == 1:
                self.canvas.move(self.id, 50, 150)
                self.canvas.bind_all('<KeyPress-w>', self.ir_arriba)
                self.canvas.bind_all('<KeyPress-s>', self.ir_abajo)
            elif self.jugador == 2:
                self.canvas.move(self.id, 450, 150)
                self.canvas.bind_all('<KeyPress-Up>', self.ir_arriba)
                self.canvas.bind_all('<KeyPress-Down>', self.ir_abajo)
            self.y = 0

    def dibujar(self, pelota_pos=None):
        if self.modo_juego == 1 or (self.modo_juego == 3 and self.tipo == "humano"):
            self.canvas.move(self.id, self.x, 0)
            pos = self.canvas.coords(self.id)
            if pos[0] <= 0:
                self.x = 0
            elif pos[2] >= self.canvas.winfo_width():
                self.x = 0
        elif self.modo_juego == 2:
            self.canvas.move(self.id, 0, self.y)
            pos = self.canvas.coords(self.id)
            if pos[1] <= 0:
                self.y = 0
            elif pos[3] >= self.canvas.winfo_height():
                self.y = 0
        elif self.modo_juego == 3 and self.tipo == "ia" and pelota_pos:
            self.mover_ia(pelota_pos)
            pos = self.canvas.coords(self.id)
            if pos[0] <= 0:
                self.x = 0
            elif pos[2] >= self.canvas.winfo_width():
                self.x = 0
            self.canvas.move(self.id, self.x, 0)

    def ir_izq(self, evt):
        self.x = -2

    def ir_der(self, evt):
        self.x = 2
    
    def empezar_juego(self, evt):
        self.empezado = True

    def ir_arriba(self, evt):
        self.y = -3

    def ir_abajo(self, evt):
        self.y = 3
        
    def mover_ia(self, pelota_pos):
        pos_raqueta = self.canvas.coords(self.id)
        centro_raqueta = (pos_raqueta[0] + pos_raqueta[2]) / 2
        centro_pelota = (pelota_pos[0] + pelota_pos[2]) / 2
        
        if centro_pelota > centro_raqueta:
            self.x = 2
        elif centro_pelota < centro_raqueta:
            self.x = -2
        else:
            self.x = 0