from . import Game_Object
import time

class Projectile(Game_Object.Game_Object):
    def __init__(self, start_x, start_y, direction, shipid):
        super().__init__()
        self.velocity = 8
        self.x = start_x
        self.y = start_y
        self.rotation = direction
        self.shipid = shipid
        self.spawn_time = time.time()


