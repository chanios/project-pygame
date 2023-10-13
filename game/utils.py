import math

def get_distance(p1,p2):
    return math.dist(p1,p2)

def get_direction_to(p1,p2):
    direction_x = p2[0] - p1[0]
    direction_y = p2[1] - p1[1]
    
    magnitude = math.sqrt(direction_x ** 2 + direction_y ** 2)
    
    if magnitude != 0:
        direction_x /= magnitude
        direction_y /= magnitude
    
    return direction_x, direction_y
    
def is_point_inside_rectangle(point, rect):
    x, y = point
    rect_x, rect_y, width, height = rect

    if rect_x <= x <= rect_x + width and rect_y <= y <= rect_y + height:
        return True
    return False