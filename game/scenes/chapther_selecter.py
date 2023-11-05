from game.scenes.scene import Scene

from game.objects.enemys.koishi_komeiji import KoishiKomeiji
from game.objects.enemys.yukari_yakumo import YukariYakumo

import pygame
chapthers = [
    {
        "name" : "The Lost sin in the dark wood",
        "enemys": [KoishiKomeiji],
        "background": "dark-wood",
        "music": "game-1",
        "hp": 5,
        "time": 60,
        "max_hp": 5
    },{
        "name" : "The Battle At Temple",
        "enemys": [YukariYakumo],
        "background": "temple",
        "music": "yukari",
        "hp": 5,
        "time": 90,
        "max_hp": 5
    },{
        "name" : "The Battle At Temple(Day)",
        "enemys": [YukariYakumo,KoishiKomeiji],
        "background": "temple_day",
        "music": "yukari",
        "hp": 5,
        "time": 120,
        "max_hp": 5
    },{
        "name" : "The Full Moon Night",
        "enemys": [KoishiKomeiji,YukariYakumo],
        "background": "red-moon",
        "music": "yukari",
        "hp": 5,
        "time": 120,
        "max_hp": 5
    }
]

class ChaptherSelectorScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.tick = 0
        self.current_chapther = 0
        self.current_music = None
    def init(self):
        self.engine.music.play('intro')

        for i,chapther in enumerate(chapthers):
            scale_factor = 30
            sprite = self.engine.sprites[chapther["background"]]
            small_image = pygame.transform.smoothscale(sprite["image"], (sprite["rect"].width // scale_factor, sprite["rect"].height // scale_factor))
            chapther["background-blurred"] = pygame.transform.smoothscale(small_image, (self.engine.WIDTH, self.engine.HEIGHT))
            chapther["background-resized"] = pygame.transform.scale(sprite["image"], (self.engine.WIDTH * 0.4, self.engine.HEIGHT * 0.6))
            
            chapther["offset_x_target"] = 0
            if i < self.current_chapther:
                chapther["offset_x_target"] = -self.engine.WIDTH
            elif i > self.current_chapther:
                chapther["offset_x_target"] = self.engine.WIDTH + self.engine.HALF_WIDTH
            chapther["offset_x"] = chapther["offset_x_target"]
            
        return;
    def draw_chapther(self, screen, chapther):
        offset_x = chapther["offset_x"]
        detail = f"""Level Detail
enemys: {len(chapther["enemys"])}
hp: {chapther["hp"]}
max_hp: {chapther["max_hp"]}
"""
        screen.blit(chapther["background-resized"], ((self.engine.WIDTH*0.1)+ offset_x,self.engine.HEIGHT*0.2))
        screen.draw.text(chapther["name"], topleft=((self.engine.WIDTH*0.53)+ offset_x, self.engine.HEIGHT*0.2), fontsize=48, color="white", owidth=2, ocolor=(39,18,77))
        screen.draw.text("Max Time:", bottomleft=((self.engine.WIDTH*0.52)+ offset_x, self.engine.HEIGHT*0.56), fontsize=72, color="white", owidth=2, ocolor=(39,18,77))
        screen.draw.text(str(chapther["time"]) + " Seconds", bottomleft=((self.engine.WIDTH*0.52)+ offset_x, self.engine.HEIGHT*0.65), fontsize=82, color="white", owidth=2, ocolor=(39,18,77))
        screen.draw.text("Higest Score:", bottomleft=((self.engine.WIDTH*0.52)+ offset_x, self.engine.HEIGHT*0.73), fontsize=72, color="white", owidth=2, ocolor=(39,18,77))
        screen.draw.text((str(chapther["higest_score"] if "higest_score" in chapther else 0)).zfill(12), bottomleft=((self.engine.WIDTH*0.52)+ offset_x, self.engine.HEIGHT*0.82), fontsize=82, color="white", owidth=2, ocolor=(39,18,77))
        screen.draw.text(detail, topleft=((self.engine.WIDTH*0.53)+ offset_x, self.engine.HEIGHT*0.25), fontsize=32, color="white", owidth=2, ocolor=(39,18,77))
    def draw(self, screen):
        screen.blit(chapthers[self.current_chapther]["background-blurred"], (0,0))
        self.draw_chapther(screen,chapthers[self.current_chapther])
        if self.current_chapther > 0: self.draw_chapther(screen,chapthers[self.current_chapther-1])
        if self.current_chapther < len(chapthers) - 1: self.draw_chapther(screen,chapthers[self.current_chapther+1])
        screen.draw.text("LEVEL SELECTOR", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.1), fontsize=62, color="white", owidth=2, ocolor=(39,18,77))
        screen.blit('arrow_left', (0,self.engine.HALF_HEIGHT - 36))
        screen.blit('arrow_right', (self.engine.WIDTH * 0.95,self.engine.HALF_HEIGHT - 36))
        if self.tick // 24 % 2 == 0:
            screen.draw.text("Press Enter to start the game!", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT*0.9), fontsize=32, color="white", owidth=2, ocolor=(39,18,77))
        return;
    def update(self,pygame):
        self.tick += 1
        if self.engine.controller.keyboard_pressed[pygame.K_RETURN]:
            self.engine.sounds.pause.play()
            # self.engine.change_scene("CHAPTHER_SELECTER", background="dark-wood", enemys=[])
        if not self.current_music == chapthers[self.current_chapther]["music"]:
            self.current_music = chapthers[self.current_chapther]["music"]
            self.engine.music.play(self.current_music)
        for chapther in chapthers:
            chapther["offset_x"] += (chapther["offset_x_target"] - chapther["offset_x"]) / 16
        return;
    def on_key_down(self, key, mod, unicode, pygame):
        if key == pygame.K_a or key == pygame.K_LEFT:
            self.current_chapther -= 1
        if key == pygame.K_d or key == pygame.K_RIGHT:
            self.current_chapther += 1
        if key == pygame.K_RETURN or key == pygame.K_e:
            chapther = chapthers[self.current_chapther]
            self.engine.change_scene("GAME", background=chapther["background"], enemys=chapther["enemys"], music=chapther["music"])
            self.engine.sounds.pause.play()
        if key == pygame.K_ESCAPE:
            self.engine.change_scene("INTRO")
        self.current_chapther = min(max(self.current_chapther,0),len(chapthers)-1)
        chapthers[self.current_chapther]["offset_x_target"] = 0
        for i,chapther in enumerate(chapthers):
            if i < self.current_chapther:
                chapther["offset_x_target"] = -self.engine.WIDTH
            elif i > self.current_chapther:
                chapther["offset_x_target"] = self.engine.WIDTH + self.engine.HALF_WIDTH
