from game.scenes.scene import Scene

from game.objects.enemys.koishi_komeiji import KoishiKomeiji
from game.objects.enemys.yukari_yakumo import YukariYakumo

chapthers = [
    {
        "name" : "The Lost sin in the dark wood",
        "enemys": [KoishiKomeiji],
        "background": "dark-wood",
        "hp": 5,
        "max_hp": 5
    },{
        "name" : "The Battle At Temple",
        "enemys": [YukariYakumo],
        "background": "temple",
        "hp": 5,
        "max_hp": 5
    },{
        "name" : "The Battle At Temple(Day)",
        "enemys": [YukariYakumo,KoishiKomeiji],
        "background": "temple_day",
        "hp": 5,
        "max_hp": 5
    },{
        "name" : "The Full Moon Night",
        "enemys": [KoishiKomeiji,YukariYakumo],
        "background": "red-moon",
        "hp": 5,
        "max_hp": 5
    }
]

class ChaptherSelectorScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.tick = 0
        self.current_chapther = 0
    def init(self):
        self.engine.music.play('intro')
        return;
    def draw(self, screen):
        chapther = chapthers[self.current_chapther]
        screen.blit(chapther["background"], (0,0))
        detail = f"""Level Detail
enemys: {len(chapther["enemys"])}
hp: {chapther["hp"]}
max_hp: {chapther["max_hp"]}
"""
        screen.draw.text("LEVEL SELECTOR", center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.15), fontsize=62, color="white", owidth=2, ocolor=(39,18,77))
        screen.blit('arrow_left', (0,self.engine.HALF_HEIGHT - 36))
        screen.blit('arrow_right', (self.engine.WIDTH * 0.95,self.engine.HALF_HEIGHT - 36))
        screen.draw.text(chapther["name"], center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.8), fontsize=32, color="white", owidth=2, ocolor=(39,18,77))
        screen.draw.text(detail, center=(self.engine.HALF_WIDTH, self.engine.HEIGHT * 0.45), fontsize=32, color="white", owidth=2, ocolor=(39,18,77))
        return;
    def update(self,pygame):
        self.tick += 1
        if self.engine.controller.keyboard_pressed[pygame.K_RETURN]:
            self.engine.sounds.pause.play()
            # self.engine.change_scene("CHAPTHER_SELECTER", background="dark-wood", enemys=[])
        return;
    def on_key_down(self, key, mod, unicode, pygame):
        if key == pygame.K_a or key == pygame.K_LEFT:
            self.current_chapther -= 1
        if key == pygame.K_d or key == pygame.K_RIGHT:
            self.current_chapther += 1
        if key == pygame.K_RETURN:
            chapther = chapthers[self.current_chapther]
            self.engine.change_scene("GAME", background=chapther["background"], enemys=chapther["enemys"])
            self.engine.sounds.pause.play()
        if key == pygame.K_ESCAPE:
            self.engine.change_scene("INTRO")
        self.current_chapther = min(max(self.current_chapther,0),len(chapthers)-1)