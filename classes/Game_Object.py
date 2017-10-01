import random

OPPOSITE_DIRECTION = {"left":"right", "right":"left", "up":"down", "down":"up"}
MAX_HEIGHT = 600
MAX_WIDTH = 700
class Game_Object:
    def __init__(self):
        self.direction = ""
        self.velocity = 0
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 400)

    def move(self, obj, direction):
        if obj.direction != "" and direction == OPPOSITE_DIRECTION[obj.direction]:
            obj.velocity = 0
        else: 
            obj.velocity = 1

        obj.direction = direction

        if direction == "left":
            obj.x = obj.x-obj.velocity
        elif direction == "right":
            obj.x = obj.x+obj.velocity
        elif direction == "up":
            obj.y = obj.y-obj.velocity
        elif direction == "down":
            obj.y = obj.y+obj.velocity

        if obj.x > MAX_WIDTH:
            obj.x = 0
        elif obj.x < 0:
            obj.x = MAX_WIDTH
        
        if obj.y > MAX_HEIGHT:
            obj.y = 0
        elif obj.y < 0:
            obj.y = MAX_HEIGHT

        return obj

