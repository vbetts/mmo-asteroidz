import random

OPPOSITE_DIRECTION = {"left":"right", "right":"left", "up":"down", "down":"up"}
MAX_HEIGHT = 600
MAX_WIDTH = 700
class Game_Object:
    def __init__(self):
        self.direction = ""
        self.velocity = 0
        self.rotation = 0
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 400)

    def set_direction(self, direction):
        if self.direction != "" and direction == OPPOSITE_DIRECTION[self.direction]:
            self.velocity = 0
        else:
            self.velocity = 1
            #the rotation here can be 90 or 270

        self.direction = direction
    
    #Moves the ship continuously once the user chooses a direction
    def move(self):
        if self.direction == "left":
            self.x = self.x-self.velocity
        elif self.direction == "right":
            self.x = self.x+self.velocity
        elif self.direction == "up":
            self.y = self.y-self.velocity
        elif self.direction == "down":
            self.y = self.y+self.velocity

        if self.x > MAX_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = MAX_WIDTH
        
        if self.y > MAX_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = MAX_HEIGHT


