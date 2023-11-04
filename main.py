import pygame
import pgzrun
import os
import random
import math
from game.engine import Engine

WIDTH, HEIGHT = 1280, 720

engine = Engine(WIDTH, HEIGHT)

def on_key_down(key, mod, unicode):
    engine.on_key_down(key, mod, unicode, pygame)
def on_mouse_move(pos,rel, buttons):
    engine.set_mouse_pos(pos)
def draw():
    engine.draw(screen)
def update():
    engine.update(pygame)
engine.init(music,sounds)
pgzrun.go()
