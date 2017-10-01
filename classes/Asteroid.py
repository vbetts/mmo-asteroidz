import random
from . import Game_Object

class Asteroid(Game_Object.Game_Object):
    def __init__(self):
        super().__init__()
        self.radius = random.randint(20, 75)
        self.velocity = random.randint(1, 5)
        self.points = self.generate_points()
        self.spin = random.randint(0, 359)

    def generate_points(self):
        degrees_remaining = 360
        points = []
        #Generate random points around a circle for an organically shaped asteroid
        while degrees_remaining > 20:
            deg = random.randint(20, 80)
            degrees_remaining -= deg
            points.append(deg)
        return points

    def move(self):
        super().move()
        self.spin+=5

        if self.spin >= 360:
            self.spin = self.spin%360
