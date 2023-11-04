from game.objects.generic_object import GenericObject
from game.utils import is_point_inside_rectangle, get_direction_to

class Item(GenericObject):
    def __init__(self, scene, sprite="p_coin"):
        super().__init__(scene)
        self.set_sprite(sprite)
        self.magnet = False
    def update(self):
        super().update();
        if self.magnet:
            dist = self.distance_to(self.scene.player)
            if dist < 200:
                dx, dy = get_direction_to([self.x,self.y],[self.scene.player.x,self.scene.player.y])
                self.set_velocity(dx*20,dy*20)
        if is_point_inside_rectangle((self.x,self.y), (self.scene.player.x-10, self.scene.player.y-10, 20, 20)):
            self.player_collected()
            self.scene.engine.sounds.item.play()
            self.scene.items.remove(self)
            return
    def player_collected(self):
        return;


class PCoinItem(Item):
    def __init__(self, scene, sprite="p_coin"):
        super().__init__(scene, sprite)
        self.velocity_y = 2
        self.magnet = True
    def player_collected(self):
        self.scene.player.point+=100;