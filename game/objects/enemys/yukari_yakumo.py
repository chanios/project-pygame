from game.objects.item import PCoinItem
from game.objects.bullet import Bullet
from game.spitemaps import spite_maps
from game.utils import get_direction_to
from .enemy import Enemy
import math
import random

class YukariYakumo(Enemy):
    def __init__(self, scene):
        super().__init__(scene)
        self.current_sprite_state = None
        self.all_actions = [
            # "ATTACK_1",
            "ATTACK_2",
            "ATTACK_3",
            "ATTACK_4",
            "ATTACK_5",
            "ATTACK_6"
        ]
        self.current_action = None;
        self.max_hp = 500;
        self.hp = self.max_hp;
        self.set_sprite_queue([
            spite_maps["yukari_yakumo_intro"]["start"],
            spite_maps["yukari_yakumo_idle"]["loop"]
        ])
        self.pattern_data = None
        self.is_cloned = False
        self.pattern_start_tick = 0
    def draw(self,screen):
        super().draw(screen)
        if self.current_action == "ATTACK_4":
            if self.pattern_data:
                sprite = self.scene.engine.sprites["rift_1"]
                for x,y in self.pattern_data:
                    screen.blit(sprite["image"], (x - self.scene.camera.x - sprite["center"][0], y - self.scene.camera.y - sprite["center"][1]))
    def death(self):
        super().death();
        self.drop(PCoinItem,50)
    def update(self):
        if self.current_sprite == spite_maps["yukari_yakumo_intro"]["start"]:
            return;
        sprite = spite_maps["yukari_yakumo_idle"]
        if self._tick % 300 == 0:
            if self.current_action == None:
                self.pattern_data = None
                self.pattern_start_tick = self._tick
                self.current_action = self.all_actions[random.randint(0,len(self.all_actions)-1)]
            else:
                dx, dy = get_direction_to([self.x,self.y],[self.scene.player.x+random.randint(-100,100),self.scene.player.y+random.randint(-100,100)])
                self.velocity_x = dx*random.randint(20,100)
                self.velocity_y = dy*random.randint(20,100)
                self.current_action = None
        if self._tick % 4 == 0:
            is_shoot = False
            if self.current_action == "ATTACK_1":
                is_shoot = True
                num_bullets = 5
                for i in range(num_bullets):
                    b = self.new_bullet()
                    b.set_position(self.x, self.y)
                    dx, dy = get_direction_to([b.x, b.y], [self.scene.player.x, self.scene.player.y])
                    b.set_sprite('bullet_red')
                    b.set_velocity(dx * 30, dy * 30)
                    b.set_homing(self.scene.player, 100)
                    b.set_f(1.1)
            elif self.current_action == "ATTACK_2":
                is_shoot = True
                for y_offset in range(-100, 101, 20):
                    b = self.new_bullet()
                    b.set_position(self.x, self.y + y_offset)
                    dx, dy = get_direction_to([b.x, b.y], [self.scene.player.x, self.scene.player.y])
                    b.set_sprite('bullet_green')
                    b.set_velocity(dx * 40, dy * 40)
            elif self.current_action == "ATTACK_3":
                is_shoot = True
                self.x = self.scene.player.x + random.randint(-750, 750)
                self.y = self.scene.player.y + random.randint(-550, 550)
                b = self.new_bullet()
                b.set_position(self.x, self.y)
                dx, dy = get_direction_to([b.x, b.y], [self.scene.player.x, self.scene.player.y])
                b.set_sprite('bullet_purple')
                b.set_velocity(dx * 25, dy * 25)
            elif self.current_action == "ATTACK_4":
                is_shoot = True
                if self.pattern_data == None:
                    self.pattern_data = [(self.scene.player.x + random.randint(-750, 750), self.scene.player.y + random.randint(-550, 550)) for _ in range(20)]
                for pos in self.pattern_data:
                    b = self.new_bullet()
                    b.set_position(pos[0], pos[1])
                    dx, dy = get_direction_to([b.x, b.y], [self.scene.player.x, self.scene.player.y])
                    b.set_sprite('bullet_purple')
                    b.set_velocity(dx * 25, dy * 25)
            elif self.current_action == "ATTACK_5":
                for _ in range(20):
                    b = self.new_bullet()
                    b.set_position(self.x+random.randint(-50, 50), self.y+random.randint(-50, 50))
                    dx, dy = get_direction_to([b.x, b.y], [self.scene.player.x, self.scene.player.y])
                    b.set_sprite('bullet_purple')
                    b.set_velocity(dx * 25, dy * 25)
            elif self.current_action == "ATTACK_6":
                for _ in range(2):
                        chain_x = self.scene.camera.x - 100
                        chain_y = self.scene.camera.world_pos["y"] + random.randint(-750, 750)
                        for i in range(5):
                            b = self.new_bullet()
                            b.set_position(chain_x, chain_y)
                            b.set_sprite('bullet_purple')
                            b.set_velocity(20, 0)
                            chain_x += 30
            if is_shoot:
                self.scene.engine.sounds.ok00.play()
        if sprite:
            if self.current_sprite_state != sprite:
                self.current_sprite_state = sprite
                self.set_sprite_q(sprite)
        super().update()