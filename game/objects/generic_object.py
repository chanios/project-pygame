from game.utils import get_distance

class GenericObject:
    def __init__(self, game):
        self.game = game

        self.x = 0
        self.y = 0

        self.velocity_x = 0
        self.velocity_y = 0

        self.f = 1.1
        
        # for renderer
        self.rotate_angle = 0
        self.d_i = 0
        self.current_sprite = None
        self.last_sprite = {}
        self.offset_render_x = 0
        self.playing_sprite = 0
        self.sprites_len = 0
        self.sprite_queue = []
    def set_f(self,f):
        self.f = f
    def set_position(self,x,y):
        if x: self.x = x
        if y: self.y = y
        return self
    def set_velocity(self,x,y):
        if x: self.velocity_x = x
        if y: self.velocity_y = y
        return self
    def set_sprite_q(self, sprite_q):
        queue = []
        if self.last_sprite.get('end') != None:
            queue.append(self.last_sprite["end"])
        if sprite_q.get('start') != None:
            queue.append(sprite_q["start"])
        if sprite_q.get('loop') != None:
            queue.append(sprite_q["loop"])
        self.last_sprite = sprite_q
        self.set_sprite_queue(queue)
    def set_sprite_queue(self, sprite_queue):
        self.sprite_queue = sprite_queue
        self.set_sprite(self.sprite_queue.pop(0))
    def set_sprite(self, sprite):
        if sprite == self.current_sprite:
            return;
        self.current_sprite = sprite
        self.sprites = self.load_sprite(sprite)
        self.sprites_len = len(self.sprites)
        self.d_i = 0
        self.playing_sprite = 0
        return;
    def distance_to(self,obj):
        return get_distance([self.x, self.y], [obj.x, obj.y])
    def end_playing_sprite(self):
        if self.sprite_queue:
            self.set_sprite(self.sprite_queue.pop(0))
        return;
    def update(self):
        self.velocity_x /= self.f;
        self.velocity_y /= self.f;

        self.check_collide()

        self.x += self.velocity_x;
        self.y += self.velocity_y;
        return;
    def check_collide(self):
        return;
    def draw(self, screen):
        if self.sprites:
            sprite = self.game.sprites[self.sprites[self.playing_sprite]]
            if self.rotate_angle:
                rotated_image = pygame.transform.rotate(sprite["image"], self.rotate_angle)
                rotated_rect = rotated_image.get_rect(center=sprite["center"])
                rotated_center = (rotated_rect.width // 2, rotated_rect.height // 2)
                screen.blit(rotated_image, ((self.x + self.offset_render_x) - self.game.camera.x - rotated_center[0], self.y - self.game.camera.y - rotated_center[1]))
            else:
                screen.blit(sprite["image"], ((self.x + self.offset_render_x) - self.game.camera.x - sprite["center"][0], self.y - self.game.camera.y - sprite["center"][1]))
            self.d_i += 1
            if self.d_i % 7 == 0:
                self.playing_sprite = (self.playing_sprite + 1) % self.sprites_len
                if self.playing_sprite == 0 and self.d_i != 0:
                    self.end_playing_sprite()
    def load_sprite(self,sprite):
        if sprite.startswith('sprite_group_'):
            return list(sorted(filter(lambda f: f.startswith(sprite+"_"), self.game.sprites), key=lambda f: int(f.split("_")[-1])))
        else:
            return [sprite]