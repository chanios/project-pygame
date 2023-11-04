from game.scenes.scene import Scene

class IntroScene(Scene):
    def __init__(self, engine):
        super().__init__(engine)
        self.tick = 0
    def init(self):
        self.engine.music.play('intro')
        return;
    def draw(self, screen):
        screen.blit("intro", (0,0))
        if self.tick // 24 % 2 == 0:
            screen.draw.text("Press Enter to continue", owidth=2, ocolor=(39,18,77), center=(self.engine.WIDTH * 0.55, self.engine.HEIGHT * 0.8), fontsize=32, color="white")
        return;
    def update(self,pygame):
        self.tick += 1
    def on_key_down(self, key, mod, unicode, pygame):
        if key == pygame.K_RETURN:
            self.engine.sounds.pause.play()
            self.engine.change_scene("CHAPTHER_SELECTER")