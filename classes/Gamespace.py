from . import Player
from . import Spaceship
from . import Projectile
from . import Asteroid
import math
import time

class Gamespace:
    def __init__(self):
        self.spaceships = {}
        self.projectiles = []
        self.asteroids = []
        self.players = {}
        for x in range(0, 5):
           self.new_asteroid(Asteroid.Asteroid_Size.LARGE)


    def update(self):
        now = time.time()
        self.projectiles = [p for p in self.projectiles if (now-p.spawn_time) <= 3]
        #Move all the things
        for ship in self.spaceships:
            self.spaceships[ship].move()
        for projectile in self.projectiles:
            projectile.move()
        for asteroid in self.asteroids:
            asteroid.move()
        #Collide all the things
        temp_asteroids = self.asteroids
        for a in temp_asteroids:
            for p in self.projectiles:
                if self.intersect(a, p):
                    p.alive = False
                    self.break_asteroid(a)
            for s in self.spaceships:
                if self.intersect(a, self.spaceships[s]):
                    self.kill(s)
        self.projectiles = [p for p in self.projectiles if p.alive]
        self.asteroids = [a for a in self.asteroids if a.alive]

    def break_asteroid(self, asteroid):
        asteroid.alive = False
        if asteroid.size != Asteroid.Asteroid_Size.SMALL:
            self.new_asteroid(asteroid.size-1, asteroid.x, asteroid.y)
            self.new_asteroid(asteroid.size-1, asteroid.x, asteroid.y)

    def kill(self, shipid):
        pass

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

    def new_asteroid(self, size, x=None, y=None):
        self.asteroids.append(Asteroid.Asteroid(size, x, y))

    def intersect(self, a, b):
        #first try an approximation of an intersection
        if self.maybe_intersect(a, b) == False:
            return False
        else:
            #if the approximation returns true, we need to check more precisely
            #finding the intersection of two polygons is complicated, so i will come back to this
            #and return True for now
            return True

    def maybe_intersect(self, a, b):
        dx = (a.x-b.x)**2
        dy = (a.y-b.y)**2

        return (dx+dy) < (a.radius + b.radius)**2


