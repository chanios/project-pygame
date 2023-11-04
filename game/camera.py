class Camera():
    def __init__(self, HALF_WIDTH=0, HALF_HEIGHT=0,min_x=0,min_y=50):
        self.x = 0;
        self.y = 0;
        self.world_pos = {
            "x": 0,
            "y": 0
        }
        self.min_x = min_x
        self.min_y = min_y
        self.HALF_WIDTH = HALF_WIDTH
        self.HALF_HEIGHT = HALF_HEIGHT
    def update_world_pos(self):
        self.world_pos["x"] = self.x + self.HALF_WIDTH
        self.world_pos["y"] = self.y + self.HALF_HEIGHT
        return self.world_pos

    def update(self,x,y):
        self.x = max(x - self.HALF_WIDTH,self.min_x)
        self.y = max(y - self.HALF_HEIGHT,self.min_y)