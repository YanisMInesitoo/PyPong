from tkinter import *
import random
import pygame

class Pelota:
    def __init__(self, canvas, raquetas, color, modo_juego, golpe_sonido, derrota_sonido):
        self.canvas = canvas
        self.raquetas = raquetas
        self.modo_juego = modo_juego
        self.golpe_sonido = golpe_sonido
        self.derrota_sonido = derrota_sonido
        
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
                    if self.golpe_sonido:
                        self.golpe_sonido.play()
                    return True, 1
        elif self.modo_juego == 2:
            raqueta1_pos = self.canvas.coords(self.raquetas[0].id)
            if pos[2] >= raqueta1_pos[0] and pos[0] <= raqueta1_pos[2]:
                if pos[3] >= raqueta1_pos[1] and pos[3] <= raqueta1_pos[3]:
                    if self.golpe_sonido:
                        self.golpe_sonido.play()
                    return True, 1
            raqueta2_pos = self.canvas.coords(self.raquetas[1].id)
            if pos[2] >= raqueta2_pos[0] and pos[0] <= raqueta2_pos[2]:
                if pos[3] >= raqueta2_pos[1] and pos[3] <= raqueta2_pos[3]:
                    if self.golpe_sonido:
                        self.golpe_sonido.play()
                    return True, 2
        elif self.modo_juego == 3:
            raqueta1_pos = self.canvas.coords(self.raquetas[0].id)
            raqueta2_pos = self.canvas.coords(self.raquetas[1].id)
            if pos[2] >= raqueta1_pos[0] and pos[0] <= raqueta1_pos[2]:
                if pos[3] >= raqueta1_pos[1] and pos[3] <= raqueta1_pos[3]:
                    if self.golpe_sonido:
                        self.golpe_sonido.play()
                    return True, 1
            if pos[2] >= raqueta2_pos[0] and pos[0] <= raqueta2_pos[2]:
                if pos[3] >= raqueta2_pos[1] and pos[3] <= raqueta2_pos[3]:
                    if self.golpe_sonido:
                        self.golpe_sonido.play()
                    return True, 2
        return False, 0

    def dibujar(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id)
        
        if pos[1] <= 0:
            self.y = abs(self.y)
            if self.golpe_sonido:
                self.golpe_sonido.play()
        
        if pos[3] >= self.canvas_height:
            if self.derrota_sonido:
                self.derrota_sonido.play()
            self.golpea_fondo = True
        
        if self.modo_juego == 1 or self.modo_juego == 3:
            rebotar, jugador_que_reboto = self.golpea_raqueta(pos)
            if rebotar:
                self.y = -abs(self.y)
                self.puntuacion_jugador1 += 1
                if self.puntuacion_jugador1 == 1:
                    # El logro "Primer Golpe" se activa en pong.py
                    pass
            if self.modo_juego == 3:
                if rebotar and jugador_que_reboto == 2:
                     self.y = -abs(self.y)
            if pos[0] <= 0:
                self.x = abs(self.x)
                if self.golpe_sonido:
                    self.golpe_sonido.play()
            if pos[2] >= self.canvas_width:
                self.x = -abs(self.x)
                if self.golpe_sonido:
                    self.golpe_sonido.play()
        elif self.modo_juego == 2:
            rebotar, jugador_que_reboto = self.golpea_raqueta(pos)
            if rebotar:
                if jugador_que_reboto == 1:
                    self.x = abs(self.x)
                elif jugador_que_reboto == 2:
                    self.x = -abs(self.x)
            
            if pos[0] <= 0:
                self.puntuacion_jugador2 += 1
                self.golpea_fondo = True
                if self.derrota_sonido:
                    self.derrota_sonido.play()
            if pos[2] >= self.canvas_width:
                self.puntuacion_jugador1 += 1
                self.golpea_fondo = True
                if self.derrota_sonido:
                    self.derrota_sonido.play()