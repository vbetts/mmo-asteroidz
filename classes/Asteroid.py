import random
from . import Game_Object
from enum import IntEnum

class Asteroid_Size(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Asteroid(Game_Object.Game_Object):
    SCALE = 15

    def __init__(self, size, x=None, y=None):
        super().__init__()
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.size = size
        self.radius = self.SCALE*size
        self.velocity = random.randint(1, 5)
        self.points = self.generate_points()
        self.spin = random.randint(0, 359)

    def generate_points(self):
        degrees_remaining = 360
        points = []
        #Generate random points around a circle for an organically shaped asteroid
        while degrees_remaining > 0:
            deg = random.randint(min(degrees_remaining, 30), min(70, degrees_remaining))
            degrees_remaining -= deg
            points.append(deg)
        return points

    def move(self):
        super().move()
        self.spin+=5

        if self.spin >= 360:
            self.spin = self.spin%360
