# -*- coding: utf-8 -*-
import sys
import spyral
import spyral.debug
import pygame
import math
import random
pygame.mixer.init()

class Elemento1(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(100,100)).fill((255,0,0))
        self.pos = (200,200)

    def comportamiento1(self):
        # Aquí colocar comportamientos, animaciones, etc.
        pass

class Juego(spyral.Scene):
    def __init__(self, activity=None, SIZE=None, callback=None):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=self.size).fill((255,255,255))

        self.elemento1 = Elemento1(self)

        # Define la función "chequea" para determinar el estado del juego
        spyral.event.register("director.update", self.chequea)
        
        # Esto es para poder salir correctamente del juego
        spyral.event.register("system.quit", spyral.director.pop)

        # Este código es para salir de la imagen de inicio del juego
        if activity:
            self.activity = activity

        if callback:
            callback()

    def chequea(self):
        # Aquí se revisa el estado de los elementos, por ejemplo colisiones.
        pass

    def get_frame(self):
        # esto es necesario para que la consola funcione
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame
        return frame

if __name__ == "__main__":
    size = (800, 600)
    spyral.director.init( size )
    spyral.director.push( Juego(SIZE=size) )
    spyral.director.run()
