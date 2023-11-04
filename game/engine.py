import os
import pygame
from game.utils import get_distance
from game.controller import Controller

from game.scenes.game import GameScene
from game.scenes.intro import IntroScene
from game.scenes.chapther_selecter import ChaptherSelectorScene

import random
import time

all_scenes = {
    "INTRO": IntroScene,
    "CHAPTHER_SELECTER": ChaptherSelectorScene,
    "GAME": GameScene,
}
class Engine():
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.HALF_WIDTH = WIDTH // 2
        self.HALF_HEIGHT = HEIGHT // 2
        
        self.controller = Controller(self)

        # for renderer
        self.sprites = {}
        self.dt_draw  = 0
        self.dt_clear = 0
        self._tick = 0

        self.music = None
        self.sounds = None
        self.scenes = {}

        for [scene, Scene] in all_scenes.items():
            self.scenes[scene] = Scene(self)
        # INTRO, CHAPTHER_SELECTER, GAME
        self.current_scene = None

    def init(self,music,sounds):
        self.dt_draw = get_distance([self.HALF_WIDTH,self.HALF_HEIGHT], [self.WIDTH,0]) * 1.02
        self.dt_clear = self.dt_draw * 1.3
        self.load_sprites()
        self.music = music
        self.sounds = sounds
        self.change_scene("INTRO")
    
    def load_sprites(self):
        all_imgs = os.listdir("images")
        for img in all_imgs:
            image = pygame.image.load("images/"+img)
            image_rect = image.get_rect()
            image_center = (image_rect.width // 2, image_rect.height // 2)
            img = img.split('.', 1)[0]
            self.sprites[img] = {
                "image": image,
                "rect": image_rect,
                "center": image_center
            }
    def change_scene(self, new_scene, **scene_data):
        self.scenes[new_scene].init(**scene_data)
        self.current_scene = new_scene

    def draw(self, screen):
        scence = self.scenes[self.current_scene]
        scence.draw(screen)
    
    def update(self, pygame):
        self.controller.update(pygame)
        scence = self.scenes[self.current_scene]
        scence.update(pygame)
    
    def set_mouse_pos(self, pos):
        self.controller.update_mouse_pos(pos)

    def on_key_down(self, key, mod, unicode, pygame):
        self.scenes[self.current_scene].on_key_down(key, mod, unicode, pygame)