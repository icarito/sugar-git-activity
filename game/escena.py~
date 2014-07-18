# -*- coding: utf-8 -*-
import spyral
import spyral.debug
import pygame
import math
import random
pygame.mixer.init()

class Fondo(spyral.Sprite):
    def __init__(self, scene, lugar):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/bg_shroom.png").scale(scene.size)
        self.layer = "fondo"

        self.avanzando = False
        self.lugar = lugar

        if self.lugar == 2:
            self.x = self.scene.width

        spyral.event.register ("director.scene.enter", self.avanzo)
        spyral.event.register ("director.update", self.chequea)

    def avanzo(self):
        if not self.avanzando:
            animacion = spyral.Animation("x", spyral.easing.Linear(self.x, self.x - self.scene.width), duration=10)
            self.animate(animacion)
            self.avanzando = True

    def chequea(self):
        target = 0 if self.lugar==2 else (-1 * self.scene.width)
        if self.x == target:
            self.reset()

    def reset(self):
        self.avanzando = False
        if self.lugar == 2:
            self.x = self.scene.width
        elif self.lugar == 1:
            self.x = 0
        self.avanzo()


class Comodo(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/comodo.png")
        self.layer = "frente"
        self.scale = 0.5
        self.pos = (0, scene.height - self.height)

        self.estado = "normal"
        self.cajita = spyral.Rect(0, 60, scene.width-self.width, scene.height-self.height)
        self.vida = 100

        spyral.event.register("input.keyboard.down.space", self.salto)
        spyral.event.register("input.keyboard.down.up", self.salto)
        spyral.event.register("input.keyboard.down.down", self.picada)
        spyral.event.register("input.keyboard.down.left", self.izquierda)
        spyral.event.register("input.keyboard.down.right", self.derecha)
        spyral.event.register("Comodo.y.animation.end", self.fin_salto)
        spyral.event.register("Comodo.muere", self.muere)

        spyral.event.register("director.update", self.chequea)
        #fin constructor

    def salto(self):
        self.stop_all_animations()
        self.estado = "saltando"
        animacion = spyral.Animation("y", spyral.easing.CubicOut(self.y, self.y-100), duration=1)
        self.animate(animacion)

    def picada(self):
        self.stop_all_animations()
        self.estado = "picada"
        animacion = spyral.Animation("y", spyral.easing.CubicOut(self.y, self.y+50), duration=0.2)
        self.animate(animacion)

    def izquierda(self):
        self.stop_all_animations()
        self.estado = "izquierda"
        animacion = spyral.Animation("x", spyral.easing.CubicOut(self.x, self.x-50), duration=0.5)
        self.animate(animacion)

    def derecha(self):
        self.stop_all_animations()
        self.estado = "derecha"
        animacion = spyral.Animation("x", spyral.easing.CubicOut(self.x, self.x+50), duration=0.5)
        self.animate(animacion)

    def fin_salto(self):
        self.estado = "normal"

    def cae(self):
        if not self.estado == "cayendo":
            self.estado = "cayendo"
            animacion = spyral.Animation("y", spyral.easing.QuadraticIn(self.y, self.cajita.height), duration=2)
            self.animate(animacion)

    def muere(self):
        self.stop_all_animations()
        self.scene.fondo1.stop_all_animations()
        self.scene.fondo2.stop_all_animations()
        spyral.event.unregister("director.update", self.chequea)

    def chequea(self):
        if self.estado == "normal":
            self.cae()
        if self.y < self.cajita.y:
            self.stop_all_animations()
            self.cae()


class Barra_de_Vida (spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(scene.width-20, 40)).fill((0,0,255))
        self.layer = "frente"
        self.pos = (10, 10)

        spyral.event.register ("director.update", self.chequea)

    def actualiza(self):
        if self.scene.comodo.vida < 61:
            self.image.fill((255,255,0))
        if self.scene.comodo.vida < 11:
            self.image.fill((255,0,0))
        if self.scene.comodo.vida > 61:
            self.image.fill((0,0,255))

        try:
            animacion = spyral.Animation( "scale_x", spyral.easing.Linear( self.scale_x,
                                                            self.scene.comodo.vida/100.0),
                                                            duration=0.5)
            self.animate(animacion)
        except ValueError:
            pass # No se puede animar dos veces la misma propiedad

    def chequea(self):
        if self.scene.comodo.vida <= 0:
            self.visible = False
            spyral.event.queue ("Comodo.muere")
        else:
            #self.scale_x = self.scene.comodo.vida/100.0
            self.actualiza()


class Mostro(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(50,50)).fill((255,0,0))
        self.layer = "frente"

        self.pos = (scene.width, random.randint(0, scene.height - self.height))

        spyral.event.register ("director.update", self.chequea)
        spyral.event.register("Comodo.muere", self.fin)

    def mover(self):
        animacion = spyral.Animation("x", spyral.easing.Linear(self.x, 0 - self.width), duration=5)
        self.animate(animacion)

    def fin(self):
        self.stop_all_animations()

    def desaparecer(self):
        self.kill()
        del(self)

    def chequea(self):
        if self.collide_sprite(self.scene.comodo):
            spyral.event.unregister("director.update", self.chequea)
            self.desaparecer()
            self.scene.comodo.vida -= 5 
        if self.x==0 - self.width:
            self.desaparecer()


class Premio(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(50,50)).fill((0,0,255))
        self.layer = "frente"

        self.pos = (scene.width, random.randint(0, scene.height - self.height))

        spyral.event.register ("director.update", self.chequea)
        spyral.event.register("Comodo.muere", self.fin)

    def mover(self):
        animacion = spyral.Animation("x", spyral.easing.Linear(self.x, 0 - self.width), duration=5)
        self.animate(animacion)

    def fin(self):
        self.stop_all_animations()

    def desaparecer(self):
        self.kill()
        del(self)

    def chequea(self):
        if self.collide_sprite(self.scene.comodo):
            spyral.event.unregister("director.update", self.chequea)
            self.desaparecer()
            if self.scene.comodo.vida <= 95:
                self.scene.comodo.vida += 5 
        if self.x==0 - self.width:
            self.desaparecer()


class Juego(spyral.Scene):
    def __init__(self, activity=None, SIZE=None, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=self.size).fill((255,255,255))
        self.layers = ["fondo", "frente"]

        self.fondo1 = Fondo(self, 1)
        self.fondo2 = Fondo(self, 2)

        self.comodo = Comodo(self)
        self.barra = Barra_de_Vida(self)

        # Define la función "chequea" para determinar el estado del juego
        spyral.event.register("director.update", self.chequea)

        # Esto es para poder salir correctamente del juego
        spyral.event.register("system.quit", spyral.director.pop)

        # Este código es para salir de la imagen de inicio del juego
        if activity:
            activity.game_button.set_active(True)
            activity.box.next_page()
            activity._pygamecanvas.grab_focus()
            activity.window.set_cursor(None)
            self.activity = activity

    def chequea(self):
        # Aquí creamos los objetos que van apareciendo
        posibilidad = random.random()
        if posibilidad > 0.95:
            nuevomostro = Mostro(self)
            nuevomostro.mover()
        if posibilidad < 0.01:
            nuevopremio = Premio(self)
            nuevopremio.mover()
