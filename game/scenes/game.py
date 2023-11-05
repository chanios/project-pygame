from game.objects.player import Player
from game.objects.enemys.koishi_komeiji import KoishiKomeiji
from game.objects.enemys.yukari_yakumo import YukariYakumo

from game.spitemaps import spite_maps
from game.camera import Camera
from game.scenes.scene import Scene
import random
class GameScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)

        # game objects
        self.player = None
        self.enemys = []
        self.bullets = []
        self.items = []
        self.background = None
        self._tick = 0
        self.game_over = None
        self.camera = Camera(self.engine.HALF_WIDTH, self.engine.HALF_HEIGHT, 0, 50)
        self.pause = False
    def init(self,background,enemys,music="game-1"):
        self.enemys_list = enemys
        self.background = background
        self.player = Player(self)
        self.setup_scene()
        self.pause = False
        
        self.engine.music.play(music)
    def setup_scene(self):
        self.enemys = []
        self.bullets = []
        self.items = []
        self.player.set_position(2000,2000)
        self.player.hp = 3
        self.player.max_hp = 3
        self.player.point = 0
        self.game_over = None

        for ENEMY in self.enemys_list:
            e = ENEMY(self)
            e.set_position(self.player.x + 500 + random.randint(-500,500), self.player.y + random.randint(-500,500))
            self.enemys.append(e)
    def draw(self, screen):
        screen.blit(self.background, (-self.camera.x / 7, -self.camera.y / 7))
        self.player.draw(screen)
        cam_x_start = self.camera.x - 100
        cam_y_start = self.camera.y - 100
        cam_y_end = self.camera.y + self.engine.HEIGHT + 100
        cam_x_end = self.camera.x + self.engine.WIDTH + 100
        for obj in self.enemys:
            obj.draw(screen)
        for obj in self.items+self.bullets:
            if obj.x > cam_x_start and obj.x < cam_x_end and obj.y > cam_y_start and obj.y < cam_y_end:
                obj.draw(screen)
        
        if self.game_over:
            screen.draw.text(self.game_over, center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.4),owidth=2, ocolor=(0,0,0), fontsize=64,fontname="joystixmonospace", color="white")
            screen.draw.text(f"Score : {self.player.point}", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.5),owidth=2, ocolor=(0,0,0), fontsize=32,fontname="joystixmonospace", color="white")
                
            if self._tick // 24 % 2 == 0:
                screen.draw.text("Press R to restart", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.6),owidth=2, ocolor=(0,0,0),fontname="joystixmonospace", fontsize=24, color="white")
                screen.draw.text("Press M to back to main menu", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.7),owidth=2, ocolor=(0,0,0),fontname="joystixmonospace", fontsize=24, color="white")
        elif self.pause:
            screen.draw.text("Pause", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.4), fontsize=64,owidth=2, ocolor=(0,0,0),fontname="joystixmonospace", color="white")
            if self._tick // 24 % 2 == 0:
                screen.draw.text("Press C to unpause", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.6),owidth=2, ocolor=(0,0,0),fontname="joystixmonospace", fontsize=24, color="white")
                screen.draw.text("Press M to back to main menu", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.7),owidth=2, ocolor=(0,0,0),fontname="joystixmonospace", fontsize=24, color="white")
        else:self.player.draw_ui(screen)
    def update(self,pygame):
        self._tick+=1
        if self.game_over or self.pause: return

        self.player.update()
        
        # if len(self.enemys) <= 0:
        #     for i in range(1):
        #         ENEMY = random.choice([KoishiKomeiji,YukariYakumo])
        #         e = ENEMY(self)
        #         e.set_position(self.player.x + 500 + random.randint(-500,500), self.player.y + random.randint(-500,500))
        #         self.enemys.append(e)
        
        for obj in self.enemys + self.bullets + self.items:
            obj.update()
        
        if self._tick%20==0:
            cam_x_start = self.camera.x - 200
            cam_y_start = self.camera.y - 200
            cam_y_end = self.camera.y + self.engine.HEIGHT + 200
            cam_x_end = self.camera.x + self.engine.WIDTH + 200
            for obj in self.bullets:
                if obj.x < cam_x_start and obj.x > cam_x_end and obj.y < cam_y_start and obj.y > cam_y_end:
                    obj.destroy()
        if len(self.enemys) <= 0:
            self.game_over = "You Win!"
        self.camera.update(self.player.x,self.player.y)
        self.camera.update_world_pos()
    def player_death(self):
        self.game_over = "You Dead!"
        self.player.set_sprite_q(spite_maps["player_timeout"])
    
    def on_key_down(self, key, mod, unicode, pygame):
        if self.pause:
            if key == pygame.K_c or key == pygame.K_ESCAPE:
                self.pause = False
            if key == pygame.K_m:
                self.engine.change_scene('CHAPTHER_SELECTER')
        elif self.game_over:
            if key == pygame.K_m:
                self.engine.change_scene('CHAPTHER_SELECTER')
            if key == pygame.K_r:
                self.setup_scene()
        else:
            if key == pygame.K_ESCAPE:
                self.engine.sounds.pause.play()
                self.pause = True