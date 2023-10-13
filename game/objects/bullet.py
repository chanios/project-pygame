from game.objects.generic_object import GenericObject
from game.utils import is_point_inside_rectangle, get_direction_to

class Bullet(GenericObject):
    def __init__(self, game, team="player"):
        super().__init__(game)
        self.f = 1
        self.mass = 1
        self.damage = 1
        self.team = team

        self.homing_target = None
        self.homing_tick_left = None
        self._removed = False
    def destroy(self):
        if self._removed: return;
        self._removed = True
        self.game.bullets.remove(self)
    def set_homing(self, obj, tick=None):
        self.homing_target = obj
        self.homing_tick_left = tick
    def check_collide(self):
        if self.x + self.velocity_x < 0 or self.y + self.velocity_y < 0:
            self.destroy()
    def destruct(self):
        self.destroy()
    def update(self):
        super().update();
        if self.homing_target:
            if self.homing_tick_left != None and self.homing_tick_left <= 0:
                self.destruct()
            dx, dy = get_direction_to([self.x,self.y], [self.homing_target.x, self.homing_target.y])
            self.velocity_x += dx*3
            self.velocity_y += dy*3
            if self.homing_tick_left:
                self.homing_tick_left -=  1
        if self.team == "player":
            for enemy in self.game.enemys:
                if is_point_inside_rectangle((self.x,self.y), (enemy.x-50, enemy.y-100, 100, 200)):
                    enemy.damage(self.damage)
                    self.destroy()
                    self.game.sounds.damage.play()
                    return
        else:
            if self.game.player.shield <= 0 and is_point_inside_rectangle((self.x,self.y), (self.game.player.x-10, self.game.player.y-10, 20, 20)):
                self.game.player.damage(self.damage)
                self.game.sounds.damage.play()
                self.destroy()
                return