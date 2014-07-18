import spyral
import escena

def main(activity=None):
    spyral.director.push(escena.Juego(activity))
