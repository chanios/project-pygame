import os
import pygame
from game.utils import get_distance
from game.camera import Camera
from game.controller import Controller
from game.objects.player import Player
from game.objects.enemys.koishi_komeiji import KoishiKomeiji
from game.objects.enemys.yukari_yakumo import YukariYakumo

import random
import time
class Engine():
    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.HALF_WIDTH = WIDTH // 2
        self.HALF_HEIGHT = HEIGHT // 2
        
        self.controller = Controller(self)

        # for renderer
        self.sprites = {}
        self.camera = Camera(self)
        self.dt_draw  = 0
        self.dt_clear = 0
        self._tick = 0

        # game objects
        self.player = None
        self.enemys = []
        self.bullets = []
        self.items = []

        self.music = None
        self.sounds = None
    def init(self,music,sounds):
        self.player = Player(self)
        self.player.set_position(2000,2000)
        self.dt_draw = get_distance([self.HALF_WIDTH,self.HALF_HEIGHT], [self.WIDTH,0]) * 1.02
        self.dt_clear = self.dt_draw * 1.3
        self.load_sprites()
        self.music = music
        self.sounds = sounds
        self.music.play('bg-1')
    
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
    def draw_main_game(self, screen):
        screen.blit("background", (-self.camera.x / 7, -self.camera.y / 7))
        self.player.draw(screen)
        cam_x_start = self.camera.x - 100
        cam_y_start = self.camera.y - 100
        cam_y_end = self.camera.y + self.HEIGHT + 100
        cam_x_end = self.camera.x + self.WIDTH + 100
        for obj in self.enemys:
            obj.draw(screen)
        for obj in self.items+self.bullets:
            if obj.x > cam_x_start and obj.x < cam_x_end and obj.y > cam_y_start and obj.y < cam_y_end:
                obj.draw(screen)
            
        self.player.draw_ui(screen)
    
    def draw(self, screen):
        self.draw_main_game(screen)
    
    def update(self, pygame):
        self.controller.update(pygame)
        self.player.update()

        if len(self.enemys) <= 0:
            for i in range(1):
                ENEMY = random.choice([KoishiKomeiji,YukariYakumo])
                e = ENEMY(self)
                e.set_position(self.player.x + 500 + random.randint(-500,500), self.player.y + random.randint(-500,500))
                self.enemys.append(e)
        
        for obj in self.enemys + self.bullets + self.items:
            obj.update()
    
        if self._tick%20==0:
            cam_x_start = self.camera.x - 200
            cam_y_start = self.camera.y - 200
            cam_y_end = self.camera.y + self.HEIGHT + 200
            cam_x_end = self.camera.x + self.WIDTH + 200
            for obj in self.bullets:
                if obj.x < cam_x_start and obj.x > cam_x_end and obj.y < cam_y_start and obj.y > cam_y_end:
                    obj.destroy()

        self._tick+=1
        self.camera.update()
        self.camera.update_world_pos()
    
    def set_mouse_pos(self, pos):
        self.controller.update_mouse_pos(pos)