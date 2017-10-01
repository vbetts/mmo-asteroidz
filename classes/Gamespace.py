from . import Player
from . import Spaceship
from . import Projectile
from . import Asteroid
import math

class Gamespace:
    def __init__(self):
        self.spaceships = {}
        self.projectiles = []
        self.asteroids = []
        self.players = {}

    def update(self):
        for ship in self.spaceships:
            self.spaceships[ship].move()
        for projectile in self.projectiles:
            for missile in self.projectiles:
                missile.move()
        for asteroid in self.asteroids:
            self.asteroids[asteroid].move()

    def new_player(self, sid):
        ship = Spaceship.Spaceship()
        self.spaceships[ship.shipid] = ship
        user = Player.Player(sid)
        user.shipid = ship.shipid
        self.players[user.playerid] = user

    def new_projectile(self, player_id):
        SPACESHIP_LENGTH = 15

        shipid = self.players[player_id].shipid
        
        ship_x = self.spaceships[shipid].x
        ship_y = self.spaceships[shipid].y
        ship_rot = self.spaceships[shipid].rotation
        ship_rot_rad = math.radians(ship_rot)
        
        #calculate the front of the ship
        start_x = ship_x + SPACESHIP_LENGTH * math.cos(ship_rot_rad)
        start_y = ship_y + SPACESHIP_LENGTH * math.sin(ship_rot_rad)

        self.projectiles.append(Projectile.Projectile(start_x, start_y, ship_rot, shipid))

    def new_asteroid(self):
        self.asteroids[0] = Asteroid.Asteroid()
