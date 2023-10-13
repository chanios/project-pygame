import pygame
import pgzrun
import os
import random
import math

WIDTH, HEIGHT = 1920, 1080
camera = {'x': 0, 'y': 0}
all_imgs = os.listdir("images")
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
all_imgs_sprites = {}
for img in all_imgs:
    image = pygame.image.load("images/"+img)
    image_rect = image.get_rect()
    image_center = (image_rect.width // 2, image_rect.height // 2)
    all_imgs_sprites[img] = {
        "image": image,
        "image_rect": image_rect,
        "center": image_center
    }
spite_map = {
    "player_idle": {
        "loop": "sprite_group_11"
    },
    "player_forward": {
        "start": "sprite_group_13",
        "loop": "sprite_group_14",
        "end": "sprite_group_12"
    },
    "player_backward": {
        "start": "sprite_group_16",
        "loop": "sprite_group_17",
        "end": "sprite_group_15"
    },
    
    "enemy_idle": {
        "start": "sprite_group_6",
        "loop": "sprite_group_5",
    }
}

def get_direction_to(p1,p2):
    # Calculate direction from bullet to player
    direction_x = p2[0] - p1[0]
    direction_y = p2[1] - p1[1]
    
    # Calculate the magnitude of the direction vector
    magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
    
    # Normalize the direction vector (make it a unit vector)
    if magnitude != 0:
        direction_x /= magnitude
        direction_y /= magnitude
    
    # Calculate velocity components using normalized direction vector and bullet speed
    return direction_x, direction_y
def load_sprite(sprite):
    if sprite.startswith('sprite_group_'):
        return list(filter(lambda f: f.startswith(sprite+"_"), all_imgs))
    else:
        return [sprite]
def is_point_inside_rectangle(point, rect):
    x, y = point
    rect_x, rect_y, width, height = rect

    if rect_x <= x <= rect_x + width and rect_y <= y <= rect_y + height:
        return True
    return False
class GameObject:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y

        self.velocity_x = 0
        self.velocity_y = 0

        self.mass = 1.1
        self.f = 1.1
        
        self.current_sprite = None
        self.d_i = 0
        if sprite:
            self.set_sprite(sprite)
        self.sprite_queue = []
        self.last_sprite_q = {}
        self.offset_render_x = 0
    def set_velocity(self,x,y):
        if x: self.velocity_x = x
        if y: self.velocity_y = y
        return self
    def set_sprite_q(self, sprite_q):
        queue = []
        if self.last_sprite_q.get('end') != None:
            queue.append(self.last_sprite_q["end"])
        if sprite_q.get('start') != None:
            queue.append(sprite_q["start"])
        if sprite_q.get('loop') != None:
            queue.append(sprite_q["loop"])
        self.last_sprite_q = sprite_q
        self.set_sprite_queue(queue)
    def set_sprite_queue(self, sprite_queue):
        self.sprite_queue = sprite_queue
        self.set_sprite(self.sprite_queue.pop(0))
    def set_sprite(self, sprite):
        if sprite == self.current_sprite:
            return;
        self.current_sprite = sprite
        self.sprites = load_sprite(sprite)
        self.sprites_len = len(self.sprites)
        self.d_i = 0
        self.playing_sprite = 0
        return;
    def distance_to(self,obj):
        return math.dist([self.x, self.y], [obj.x, obj.y])
    def end_playing_sprite(self):
        if self.sprite_queue:
            self.set_sprite(self.sprite_queue.pop(0))
        return;
    def update(self):
        self.velocity_x /= self.f;
        self.velocity_y /= self.f;

        if self.x + self.velocity_x < 0:
            self.velocity_x = -self.velocity_x / self.mass
            self.wall_collide()

        self.x += self.velocity_x;
        self.y += self.velocity_y;
        return;
    def wall_collide(self):
        return;
    def draw(self):
        # screen.draw.filled_circle((self.x - camera['x'], self.y - camera['y']),25,'red')
        sprite = all_imgs_sprites[self.sprites[self.playing_sprite]]
        # print(sprite)
        screen.blit(sprite["image"], ((self.x + self.offset_render_x) - camera['x'] - sprite["center"][0], self.y - camera['y'] - sprite["center"][1]))
        self.d_i += 1
        if self.d_i % 7 == 0:
            self.playing_sprite = (self.playing_sprite + 1) % self.sprites_len
            if self.playing_sprite == 0 and self.d_i != 0:
                self.end_playing_sprite()
class Enemy(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
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
        self._tick = 0
        self.max_hp = 1000;
        self.hp = self.max_hp;
    def spawn_bullets_around(self, num_bullets, offset_angle = 0):
        angle_step = 2 * math.pi / num_bullets
        for i in range(num_bullets):
            angle = i * angle_step
            velocity_x = math.cos(angle+offset_angle) * 10  # Set initial velocity in x direction
            velocity_y = math.sin(angle+offset_angle) * 10  # Set initial velocity in y direction
            bullet = Bullet(self.x, self.y, 'bullet_red.png', 'enemy')
            bullet.set_velocity(velocity_x,velocity_y)
            bullets.append(bullet)
    def draw(self):
        super().draw();
        # screen.draw.filled_rect(Rect(self.x-camera['x']-90,self.y-camera['y']+100,180,5), 'rosybrown')
        # screen.draw.filled_rect(Rect(self.x-camera['x']-90,self.y-camera['y']+100,180,5), 'firebrick')
        screen.draw.text(str(self.hp)+"/"+str(self.max_hp), (self.x-camera['x'],self.y-camera['y']+105), fontname="joystixmonospace", fontsize=16, color="white")
    def damage(self, damage):
        self.hp -= damage
        if self.hp % 10 == 0:
            self.drop(PCoinItem,5)
        if self.hp <= 0:
            self.death();
    def drop(self, ITEM, amount = 1):
        for i in range(amount):
            item = ITEM(self.x,self.y)
            item.set_velocity(random.randint(-20,20),random.randint(-20,20))
            items.append(item)
    def death(self):
        self.drop(PCoinItem,50)
        r = random.randint(0,2)
        if r == 0:
            sounds.tan0.play()
        elif r == 1:
            sounds.tan1.play()
        else:
            sounds.tan2.play()
        enemys.remove(self)
    def update(self):
        sprite = spite_map["enemy_idle"]
        if self._tick % 300 == 0:
            if self.current_action == None:
                self.current_action = self.all_actions[random.randint(0,len(self.all_actions)-1)]
            else:
                dx, dy = get_direction_to([self.x,self.y],[player.x+random.randint(-100,100),player.y+random.randint(-100,100)])
                self.velocity_x = dx*random.randint(20,100)
                self.velocity_y = dy*random.randint(20,100)
                self.current_action = None
        if self._tick % 4 == 0:
            if self.current_action:
                sounds.ok00.play()
            if self.current_action == "ATTACK_1":
                obj = Bullet(self.x, self.y, 'bullet_red.png', 'enemy')
                dx, dy = get_direction_to([self.x,self.y],[player.x,player.y])
                obj.set_velocity(dx*20,dy*20)
                bullets.append(obj)
            elif self.current_action == "ATTACK_2":
                obj = Bullet(self.x, self.y + 100, 'bullet_red.png', 'enemy')
                dx, dy = get_direction_to([obj.x,obj.y],[player.x,player.y])
                obj.set_velocity(dx*20,dy*20)
                bullets.append(obj)
                
                obj = Bullet(self.x, self.y - 100, 'bullet_red.png', 'enemy')
                dx, dy = get_direction_to([obj.x,obj.y],[player.x,player.y])
                obj.set_velocity(dx*20,dy*20)
                bullets.append(obj)
            elif self.current_action == "ATTACK_3":
                self.spawn_bullets_around(18, self._tick)
            elif self.current_action == "ATTACK_4":
                self.spawn_bullets_around(18,0 if (self._tick // 16) % 2 == 0 else 1.57)
            elif self.current_action == "ATTACK_5":
                self.spawn_bullets_around(18,( 0 if (self._tick // 16) % 2 == 0 else 1.57)+(self._tick/100))
            elif self.current_action == "ATTACK_6":
                self.spawn_bullets_around(18,( 0 if (self._tick // 16) % 2 == 0 else 1.57)+(self._tick/1000))
            elif self.current_action == "ATTACK_7":
                bullet = Bullet(self.x, self.y - 50, 'bullet_red.png', 'enemy')
                bullet.set_velocity(math.cos(self._tick/20) * 20,math.sin(self._tick/20)*20)
                bullets.append(bullet)
                
                bullet = Bullet(self.x, self.y + 50, 'bullet_red.png', 'enemy')
                bullet.set_velocity(math.cos(-self._tick/20) * 20,math.sin(-self._tick/20)*20)
                bullets.append(bullet)
        if sprite:
            if self.current_sprite_state != sprite:
                self.current_sprite_state = sprite
                self.set_sprite_q(sprite)
        self._tick += 1;
        super().update()
class Bullet(GameObject):
    def __init__(self, x, y, sprite, team="player"):
        super().__init__(x, y, sprite)
        self.f = 1
        self.mass = 1
        self.damage = 1
        self.team = team
    def update(self):
        super().update();
        if self.team == "player":
            for enemy in enemys:
                if is_point_inside_rectangle((self.x,self.y), (enemy.x-50, enemy.y-100, 100, 200)):
                    enemy.damage(self.damage)
                    bullets.remove(self)
                    sounds.damage.play()
                    return
        else:
            if player.shield <= 0 and is_point_inside_rectangle((self.x,self.y), (player.x-10, player.y-10, 20, 20)):
                player.damage(self.damage)
                sounds.damage.play()
                bullets.remove(self)
                return
    def wall_collide(self):
        bullets.remove(self)
        super().wall_collide()
class Item(GameObject):
    def __init__(self, x, y, sprite="p_coin.png"):
        super().__init__(x, y, sprite)
        self.magnet = False
    def update(self):
        super().update();
        if self.magnet:
            dist = self.distance_to(player)
            if dist < 200:
                dx, dy = get_direction_to([self.x,self.y],[player.x,player.y])
                self.set_velocity(dx*20,dy*20)
        if is_point_inside_rectangle((self.x,self.y), (player.x-10, player.y-10, 20, 20)):
            self.player_collected()
            sounds.item.play()
            items.remove(self)
            return
    def player_collected(self):
        return;
class PCoinItem(Item):
    def __init__(self, x, y, sprite="p_coin.png"):
        super().__init__(x, y, sprite)
        self.velocity_y = 2
        self.magnet = True
    def player_collected(self):
        player.point+=100;
class Player(GameObject):
    def __init__(self, x, y, sprite):
        super().__init__(x, y, sprite)
        self.velocity_x = 0
        self.velocity_y = 0
        self.f = 1.07
        self.max_hp = 1
        self.hp = self.max_hp
        self.current_sprite_state = None
        self.offset_render_x = -40
        self.point = 0
        self.shield = 0
    def draw(self):
        super().draw();
        sprite = all_imgs_sprites["bullet_blue_small.png"]
        if self.shield > 0 and self.shield % 2 == 0:
            return;
        screen.blit(sprite["image"], (self.x - camera['x'] - sprite["center"][0], self.y - camera['y'] - sprite["center"][1]))
    def damage(self,dmg):
        self.hp -= dmg
        if self.hp <= 0:
            sounds.pldead.play()
            self.shield = 100
            self.hp = self.max_hp
    def update(self):
        sprite = None
        self.shield -= 1
        keys = pygame.key.get_pressed()
        m = pygame.mouse.get_pressed(num_buttons=3)
        speed = 1
        if keys[pygame.K_LSHIFT]:
            speed = 0.3
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y -= speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y += speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            sprite = spite_map['player_backward']
            self.velocity_x -= speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            sprite = spite_map['player_forward']
            self.velocity_x += speed
        if m[0] and self.d_i % 4 == 0:
            x = self.x
            dx, dy = get_direction_to([x,self.y], [mouse['x'] + camera['x'], mouse['y'] + camera['y']])
            obj = Bullet(x + (dx*30), self.y + (dy*30), 'bullet_blue.png')
            obj.set_velocity(dx*30, dy*30)
            bullets.append(obj)
            # if self.velocity_x > 0:
            #     obj = Bullet(self.x, self.y, 'bullet_red.png')
            #     obj.set_velocity(player.velocity_x+50,0)
            #     bullets.append(obj)
            # else:
            #     obj = Bullet(self.x, self.y, 'bullet_red.png')
            #     obj.set_velocity(player.velocity_x-50,0)
            #     bullets.append(obj)
        # print(self.velocity_x, self.velocity_y)
        if sprite == None and abs(self.velocity_x) <= 0.4 and abs(self.velocity_y) <= 0.4:
            sprite = spite_map['player_idle']
        if sprite:
            if self.current_sprite_state != sprite:
                self.current_sprite_state = sprite
                self.set_sprite_q(sprite)
        super().update()

player = Player(20, HALF_HEIGHT, 'sprite_group_5')
enemys = []
bullets = []
items = []
i = 0
def init():
    global bullets, enemys
    music.play('bg-1')
    for i in range(5):
        enemy = Enemy(2000 + random.randint(0,200), HALF_HEIGHT + random.randint(0,500), None)
        enemys.append(enemy)
def draw_ui():
    screen.draw.filled_rect(Rect(30,HEIGHT-30,400,10), 'rosybrown')
    screen.draw.filled_rect(Rect(30,HEIGHT-30,(player.hp/player.max_hp)*400,10), 'firebrick')

    # screen.draw.filled_rect(Rect(HALF_WIDTH - 600,25,1200,10), 'rosybrown')
    # screen.draw.filled_rect(Rect(HALF_WIDTH - 600,25,1200,10), 'firebrick')

    screen.draw.text(str(player.point), (WIDTH-200, HEIGHT-35), fontname="joystixmonospace", fontsize=24, color="white")
    screen.draw.text(str(player.hp)+"/"+str(player.max_hp), (450, HEIGHT-35), fontname="joystixmonospace", fontsize=16, color="white")
def draw():
    screen.blit("background", (-camera['x'] / 7, -camera['y'] / 7))
    player.draw()
    for obj in bullets:
        dist = math.dist([camera["x"] + HALF_WIDTH, camera["y"] + HALF_HEIGHT],[obj.x, obj.y])
        if dist < dist_draw:
            obj.draw()
    for obj in enemys:
        dist = math.dist([camera["x"] + HALF_WIDTH, camera["y"] + HALF_HEIGHT],[obj.x, obj.y])
        if dist < dist_draw:
            obj.draw()
    for obj in items:
        dist = math.dist([camera["x"] + HALF_WIDTH, camera["y"] + HALF_HEIGHT],[obj.x, obj.y])
        if dist < dist_draw:
            obj.draw()
    draw_ui()

mouse = {
    "x": 0,
    "y": 0
}
dist_draw = math.dist([HALF_WIDTH,HALF_HEIGHT], [WIDTH,0]) * 1.02
dist_clear = dist_draw * 1.3
def on_mouse_move(pos,rel, buttons):
    global mouse
    mouse['x'] = pos[0]
    mouse['y'] = pos[1]
def update_camera():
    global camera
    camera['x'] = max(player.x - HALF_WIDTH,0)
    camera['y'] = max(player.y - HALF_HEIGHT,50)
def update(dt):
    global i
    player.update()
    for obj in enemys:
        obj.update()
    for obj in bullets:
        obj.update()
    for obj in items:
        obj.update()
    if i%20==0:
        for obj in bullets:
            dist = math.dist([camera["x"] + HALF_WIDTH, camera["y"] + HALF_HEIGHT],[obj.x, obj.y])
            if dist > dist_clear:
                bullets.remove(obj)
    i+=1
    update_camera()
init()
pgzrun.go()
