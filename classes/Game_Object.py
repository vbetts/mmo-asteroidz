import random, math

MAX_HEIGHT = 600
MAX_WIDTH = 700
MAX_VELOCITY = 5
MIN_VELOCITY = 0

class Game_Object:
    def __init__(self):
        self.direction = ""
        self.velocity = 0
        self.rotation = random.randint(0, 359)
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 400)

    def set_direction(self, direction):
        if direction == "left":
            self.rotation -= 20
        elif direction == "right":
            self.rotation += 20

        if self.rotation >= 360:
            #Wrap around if total rotation exceeds 360
            self.rotation = self.rotation%360
        elif self.rotation < 0:
            #Wrap for negative values
            self.rotation += 360
        
        #Increase/decrease velocity within set boundaries
        if direction == "up" and self.velocity < MAX_VELOCITY:
            self.velocity += 1
        elif direction == "down" and self.velocity > MIN_VELOCITY:
            self.velocity -= 1

        self.direction = direction
    
    #Moves the ship continuously once the user chooses a direction
    def move(self):
        rad = math.radians(self.rotation)

        self.x+= self.velocity*math.cos(rad)
        self.y+= self.velocity*math.sin(rad)

        if self.x > MAX_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = MAX_WIDTH
        
        if self.y > MAX_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = MAX_HEIGHT


