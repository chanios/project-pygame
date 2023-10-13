class Camera():
    def __init__(self, game):
        self.game = game;
        self.x = 0;
        self.y = 0;
        self.world_pos = {
            "x": 0,
            "y": 0
        }

    def update_world_pos(self):
        self.world_pos["x"] = self.x + self.game.HALF_WIDTH
        self.world_pos["y"] = self.y + self.game.HALF_HEIGHT
        return self.world_pos

    def update(self):
        self.x = max(self.game.player.x - self.game.HALF_WIDTH,0)
        self.y = max(self.game.player.y - self.game.HALF_HEIGHT,50)