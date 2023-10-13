class Controller():
    def __init__(self, game):
        self.game = game

        self.keyboard_pressed = None
        self.mouse = {
            "x": 0,
            "y": 0,
            "pressed": []
        }
    
    def update(self, pygame):
        self.keyboard_pressed = pygame.key.get_pressed()
        self.mouse["pressed"] = pygame.mouse.get_pressed(num_buttons=3)
    
    def update_mouse_pos(self, pos):
        self.mouse['x'] = pos[0];
        self.mouse['y'] = pos[1];
    