from game.objects.generic_object import GenericObject
from game.spitemaps import spite_maps
from game.utils import get_direction_to
from game.objects.bullet import Bullet
import pygame

class Player(GenericObject):
    def __init__(self, game):
        super().__init__(game)
        self.velocity_x = 0
        self.velocity_y = 0
        self.f = 1.07
        self.max_hp = 1
        self.hp = self.max_hp
        self.current_sprite_state = None
        self.offset_render_x = -40
        self.point = 0
        self.shield = 0
    
    def draw_ui(self, screen):
        screen.draw.filled_rect(pygame.Rect(30,self.game.HEIGHT-30,400,10), 'rosybrown')
        screen.draw.filled_rect(pygame.Rect(30,self.game.HEIGHT-30,(self.hp/self.max_hp)*400,10), 'firebrick')
        screen.draw.text(str(self.point), (self.game.WIDTH-200, self.game.HEIGHT-35), fontname="joystixmonospace", fontsize=24, color="white")
        screen.draw.text(str(self.hp)+"/"+str(self.max_hp), (450, self.game.HEIGHT-35), fontname="joystixmonospace", fontsize=16, color="white")
    def get_bullets(self):
        return list(filter(self.game.bullets, lambda b: b.team=="player"))
    def check_collide(self):
        if self.x + self.velocity_x < 0:
            self.velocity_x = -self.velocity_x / self.f
        if self.y + self.velocity_y < 0:
            self.velocity_y = -self.velocity_y / self.f
    def draw(self, screen):
        super().draw(screen);
        sprite = self.game.sprites["bullet_blue_small"]
        if self.shield > 0 and self.shield % 2 == 0:
            return;
        screen.blit(sprite["image"], (self.x - self.game.camera.x - sprite["center"][0], self.y - self.game.camera.y - sprite["center"][1]))
    
    def damage(self,dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.game.sounds.pldead.play()
            self.shield = 100
            self.hp = self.max_hp

    def update(self):
        sprite = None
        self.shield -= 1
        keys = self.game.controller.keyboard_pressed

        speed = 1
        
        if keys[pygame.K_LSHIFT]:
            speed = 0.3

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y -= speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y += speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            sprite = spite_maps['player_backward']
            self.velocity_x -= speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            sprite = spite_maps['player_forward']
            self.velocity_x += speed

        if self.game.controller.mouse["pressed"][0] and self.d_i % 4 == 0:
            dx, dy = get_direction_to([self.x,self.y], [self.game.controller.mouse['x'] + self.game.camera.x, self.game.controller.mouse['y'] + self.game.camera.y])
            bullet = Bullet(self.game,'player')
            bullet.set_position(self.x + (dx*30),self.y + (dy*30))
            bullet.set_sprite('bullet_blue')
            bullet.set_velocity(dx*30, dy*30)
            self.game.bullets.append(bullet)

        if sprite == None and abs(self.velocity_x) <= 0.4 and abs(self.velocity_y) <= 0.4:
            sprite = spite_maps['player_idle']
        if sprite:
            if self.current_sprite_state != sprite:
                self.current_sprite_state = sprite
                self.set_sprite_q(sprite)
        super().update()
