from game.objects.item import PCoinItem
from game.objects.bullet import Bullet
from game.spitemaps import spite_maps
from game.utils import get_direction_to
from .enemy import Enemy
import math
import random
import pygame

class KoishiKomeiji(Enemy):
    def __init__(self, game):
        super().__init__(game)
        self.current_sprite_state = None
        self.all_actions = [
            "ATTACK_1",
            "ATTACK_2",
            "ATTACK_3",
            "ATTACK_4",
            "ATTACK_5",
            "ATTACK_6",
            "ATTACK_7",
        ]
        self.current_action = None;
        self.max_hp = 500;
        self.hp = self.max_hp;
    def death(self):
        super().death();
        self.drop(PCoinItem,50)
    def draw(self,screen):
        super().draw(screen)
        if self.current_action == "ATTACK_7":
            for y in [self.y-50,self.y+50]:
                sprite = self.game.sprites["star_small"]
                rotated_image = pygame.transform.rotate(sprite["image"], (self._tick/5)%360)
                rotated_rect = rotated_image.get_rect(center=sprite["center"])
                rotated_center = (rotated_rect.width // 2, rotated_rect.height // 2)
                screen.blit(rotated_image, (self.x - self.game.camera.x - rotated_center[0], y - self.game.camera.y - rotated_center[1]))
    def update(self):
        sprite = spite_maps["koishi_komeiji_idle"]
        if self._tick % 300 == 0:
            if self.current_action == None:
                self.current_action = self.all_actions[random.randint(0,len(self.all_actions)-1)]
            else:
                dx, dy = get_direction_to([self.x,self.y],[self.game.player.x+random.randint(-100,100),self.game.player.y+random.randint(-100,100)])
                self.velocity_x = dx*random.randint(20,100)
                self.velocity_y = dy*random.randint(20,100)
                self.current_action = None
        if self._tick % 4 == 0:
            if self.current_action:
                self.game.sounds.ok00.play()
            if self.current_action == "ATTACK_1":

                b = self.new_bullet()
                b.set_position(self.x,self.y)
                dx, dy = get_direction_to([b.x,b.y],[self.game.player.x,self.game.player.y])
                b.set_sprite('bullet_red')
                b.set_velocity(dx*30, dy*30)
            elif self.current_action == "ATTACK_2":
                for y in [self.y+100,self.y-100]:
                    b = self.new_bullet()
                    b.set_position(self.x, y)
                    dx, dy = get_direction_to([b.x,b.y],[self.game.player.x,self.game.player.y])
                    b.set_sprite('bullet_red')
                    b.set_velocity(dx*30, dy*30)

            elif self.current_action == "ATTACK_3":
                self.spawn_bullets_around(18, self._tick)
            elif self.current_action == "ATTACK_4":
                self.spawn_bullets_around(18,0 if (self._tick // 16) % 2 == 0 else 1.57)
            elif self.current_action == "ATTACK_5":
                self.spawn_bullets_around(18,( 0 if (self._tick // 16) % 2 == 0 else 1.57)+(self._tick/100))
            elif self.current_action == "ATTACK_6":
                self.spawn_bullets_around(18,( 0 if (self._tick // 16) % 2 == 0 else 1.57)+(self._tick/1000))
            elif self.current_action == "ATTACK_7":
                
                b = self.new_bullet()
                b.set_position(self.x, self.y-50)
                b.set_sprite('bullet_red')
                b.set_velocity(math.cos(self._tick/20) * 20,math.sin(self._tick/20)*20)
                
                b = self.new_bullet()
                b.set_position(self.x, self.y+50)
                b.set_sprite('bullet_red')
                b.set_velocity(math.cos(-self._tick/20) * 20,math.sin(-self._tick/20)*20)
        if sprite:
            if self.current_sprite_state != sprite:
                self.current_sprite_state = sprite
                self.set_sprite_q(sprite)
        super().update()