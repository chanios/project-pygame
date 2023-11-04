from game.objects.generic_object import GenericObject
from game.objects.bullet import Bullet
from game.objects.item import PCoinItem
import pygame
import math
import random

class Enemy(GenericObject):
    def __init__(self, scene):
        super().__init__(scene)
        self.current_sprite_state = None
        self.all_actions = []
        self.current_action = None;
        self._tick = random.randint(0,1000)
        self.max_hp = 1000;
        self.hp = self.max_hp;
        self.star = False
    def spawn_bullets_around(self, num_bullets, offset_angle = 0, bullet_sprite="bullet_red"):
        angle_step = 2 * math.pi / num_bullets
        for i in range(num_bullets):
            angle = i * angle_step
            velocity_x = math.cos(angle+offset_angle) * 10  # Set initial velocity in x direction
            velocity_y = math.sin(angle+offset_angle) * 10  # Set initial velocity in y direction
            
            b = self.new_bullet()
            b.set_position(self.x, self.y)
            b.set_sprite(bullet_sprite)
            b.set_velocity(velocity_x,velocity_y)
    def damage(self, damage):
        self.hp -= damage
        if self.hp % 10 == 0:
            self.drop(PCoinItem,5)
        if self.hp <= 0:
            self.death();
    def death(self):
        r = random.randint(0,2)
        if r == 0:
            self.scene.engine.sounds.tan0.play()
        elif r == 1:
            self.scene.engine.sounds.tan1.play()
        else:
            self.scene.engine.sounds.tan2.play()
    def draw(self,screen):
        
        sprite = self.scene.engine.sprites["star"]
        rotated_image = pygame.transform.rotate(sprite["image"], (self._tick*4)%360)
        rotated_rect = rotated_image.get_rect(center=sprite["center"])
        rotated_center = (rotated_rect.width // 2, rotated_rect.height // 2)
        screen.blit(rotated_image, (self.x - self.scene.camera.x - rotated_center[0], self.y - self.scene.camera.y - rotated_center[1]))
        super().draw(screen);
        # screen.draw.filled_rect(Rect(self.x-camera['x']-90,self.y-camera['y']+100,180,5), 'rosybrown')
        # screen.draw.filled_rect(Rect(self.x-camera['x']-90,self.y-camera['y']+100,180,5), 'firebrick')
        screen.draw.text(str(self.hp)+"/"+str(self.max_hp), (self.x-self.scene.camera.x,self.y-self.scene.camera.y+105), fontname="joystixmonospace", fontsize=16, color="white")
    def damage(self, damage):
        self.hp -= damage
        if self.hp % 10 == 0:
            self.drop(PCoinItem,5)
        if self.hp <= 0:
            self.death();
    def drop(self, ITEM, amount = 1):
        for i in range(amount):
            item = ITEM(self.scene)
            item.set_position(self.x, self.y)
            item.set_velocity(random.randint(-20,20),random.randint(-20,20))
            self.scene.items.append(item)
    def death(self):
        self.drop(PCoinItem,50)
        r = random.randint(0,2)
        if r == 0:
            self.scene.engine.sounds.tan0.play()
        elif r == 1:
            self.scene.engine.sounds.tan1.play()
        else:
            self.scene.engine.sounds.tan2.play()
        self.scene.enemys.remove(self)
    def update(self):
        self._tick += 1;
        super().update()
    def new_bullet(self):
        bullet = Bullet(self.scene,'enemy')
        self.scene.bullets.append(bullet)
        return bullet