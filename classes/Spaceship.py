import random
from . import Game_Object

class Spaceship(Game_Object.Game_Object):
    def __init__(self):
        super().__init__()
        self.colour = "".join([random.choice("0123456789ABCDEF") for x in range(6)])
        self.shipid = random.randint(1000, 9999)

