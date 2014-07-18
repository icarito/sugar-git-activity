# -*- coding: utf-8 -*-
import spyral
import spyral.debug
import pygame
import math
import random

splash_done = False

class Fondo(spyral.Sprite):
    def __init__(self, scene, lugar):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/bg_shroom_slim.png")
        self.image.scale( (scene.width, self.image.height) )
        self.layer = "fondo"

        self.avanzando = False
        self.lugar = lugar
        self.y = 200

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
        self.pos = (0, scene.height - self.height)

        self.estado = "normal"
        self.cajita = spyral.Rect(0, 60, scene.width-self.width, scene.height-self.height)
        self.vida = 100

        spyral.event.register("input.keyboard.down.space", self.salto)
        spyral.event.register("input.keyboard.down.up", self.salto)
        spyral.event.register("Comodo.y.animation.end", self.fin_salto)
        spyral.event.register("Comodo.muere", self.muere)

        spyral.event.register("director.update", self.chequea)
        pygame.mixer.init()
        pygame.mixer.music.load("sounds/Harp.ogg")
        pygame.mixer.music.play(-1)
        self.flap = pygame.mixer.Sound('sounds/bird_flap.ogg')
        #fin constructor

    def salto(self):
        self.stop_all_animations()
        self.estado = "saltando"
        animacion = spyral.Animation("y", spyral.easing.CubicOut(self.y, self.y-100), duration=1)
        self.animate(animacion)
        self.flap.play()

    def fin_salto(self):
        self.estado = "normal"

    def cae(self):
        if not self.estado == "cayendo":
            self.estado = "cayendo"
            animacion = spyral.Animation("y", spyral.easing.QuadraticIn(self.y, self.cajita.height), duration=2)
            self.animate(animacion)

    def muere(self):
        self.scene.fondo1.stop_all_animations()
        self.scene.fondo2.stop_all_animations()
        spyral.event.unregister("director.update", self.chequea)
        spyral.event.unregister("input.keyboard.down.space", self.salto)
        spyral.event.unregister("input.keyboard.down.up", self.salto)
        if not self.estado=="muerto":
            try:
                animacion = spyral.Animation("scale", spyral.easing.QuadraticInOut(0.5, 0.01), duration=3)
                self.animate(animacion)
            except ValueError:
                pass
        self.estado = "muerto"

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
            self.actualiza()


class Mostro(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/ninjastar_dave_pena_01.png")
        self.layer = "frente"
        self.ouch = pygame.mixer.Sound('sounds/confusion.ogg')

        self.pos = (scene.width + 2, random.randint(60, scene.height - self.height))

        spyral.event.register ("director.update", self.chequea)
        spyral.event.register("Comodo.muere", self.fin)

        self.timer = 0
        self.freq = random.random()*2
        self.duration = random.random()*2+4

    def mover(self):
        self.traslacion = spyral.Animation("x", spyral.easing.Linear(self.x, 0 - self.width), duration=self.duration)
        try:
            self.animate(self.traslacion)
        except ValueError:
            pass
        #rotacion = spyral.Animation("angle", spyral.easing.Linear(2*math.pi,0), duration=1, loop=True)
        #self.animate(rotacion)

    def fin(self):
        self.stop_all_animations()

    def reset(self):
        self.stop_animation(self.traslacion)
        self.x = self.scene.width + 2
        self.y = random.randint(60, self.scene.height - self.height)
        self.timer = 0

    def chequea(self, delta):
        if self.collide_sprite(self.scene.comodo):
            self.reset()
            self.ouch.play()
            self.scene.comodo.vida -= 20
        if self.x==0 - self.width:
            self.reset()
        if self.x==self.scene.width + 2:
            self.timer = self.timer + delta
            if self.timer > self.freq:
                self.mover()


class Premio(spyral.Sprite):
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(filename="images/love-shield.png")
        self.layer = "frente"

        self.yay = pygame.mixer.Sound('sounds/heal.ogg')

        self.pos = (scene.width + 2, random.randint(60, scene.height - self.height))
        self.timer = 0
        self.freq = random.random()*2
        self.duration = random.random()*2+4

        self.estado = "normal"

        spyral.event.register ("director.update", self.chequea)
        #spyral.event.register ("Premio.pos.animation.end", self.desaparecer)
        spyral.event.register("Comodo.muere", self.fin)

    def mover(self):
        self.traslacion = spyral.Animation("x", spyral.easing.Linear(self.x, 0 - self.width), duration=self.duration)
        try:
            self.animate(self.traslacion)
        except ValueError:
            pass

    def fin(self):
        self.stop_all_animations()

    def ascender(self):
        animacion = spyral.Animation("pos", spyral.easing.LinearTuple(self.pos, (-1*self.width, 0)), duration=1)
        try:
            self.animate(animacion)
        except ValueError:
            pass

    def reset(self):
        self.stop_animation(self.traslacion)
        self.x = self.scene.width + 2
        self.y = random.randint(60, self.scene.height - self.height)
        self.timer = 0

    def chequea(self, delta):
        if self.collide_sprite(self.scene.comodo):
            self.reset()
            self.yay.play()
            if self.scene.comodo.vida <= 75:
                self.scene.comodo.vida += 25
            else:
                self.scene.comodo.vida = 100
        if self.x==0 - self.width:
            self.reset()
        if self.x==self.scene.width + 2:
            self.timer = self.timer + delta
            if self.timer > self.freq:
                self.mover()


class Juego(spyral.Scene):
    def __init__(self, activity=None, SIZE=None, *args, **kwargs):
        spyral.Scene.__init__(self, SIZE)

        # Estrategia para ganar rendimiento en la XO:
        # En vez de deslizar todo el fondo de la pantalla, hemos escogido una
        # imagen que podemos recortar como una franja, dejando colores sólidos
        # arriba y abajo.
        self.background = spyral.Image(size=self.size).fill((109,164,26))
        self.layers = ["fondo", "frente"]

        # Este es el fondo móvil.
        self.fondo1 = Fondo(self, 1)
        self.fondo2 = Fondo(self, 2)

        # Fondo inmóvil en la franja superior
        bloque_verde = spyral.Sprite(self)
        bloque_verde.layer = "fondo"
        bloque_verde.image = spyral.Image(size=(self.width, 200)).fill((122,183,30))

        self.comodo = Comodo(self)
        self.barra = Barra_de_Vida(self)

        self.tick=0

        # Esto es para poder salir correctamente del juego
        spyral.event.register("system.quit", spyral.director.pop)

        spyral.event.register("director.scene.enter", self.wave)
        self.spawned = False

        # Este código es para salir de la imagen de inicio del juego
        if activity:
            activity.game_button.set_active(True)
            activity.box.next_page()
            activity._pygamecanvas.grab_focus()
            activity.window.set_cursor(None)
            self.activity = activity

    def wave(self):
        if not self.spawned:
            for i in range(0,6):
                m = Mostro(self)
            p = Premio(self)
        self.spawned = True


if __name__ == "__main__":
    size = (800, 600)
    spyral.director.init( size )
    spyral.director.push( Juego(SIZE=size) )
    spyral.director.run()
