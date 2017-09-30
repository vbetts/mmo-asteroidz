import random

class Spaceship:

    def __init__(self):
        self.x = random.randint(0, 600)
        self.y = random.randint(0, 400)
        self.velocity = 0
        self.colour = "".join([random.choice("0123456789ABCDEF") for x in range(6)])
        self.shipid = random.randint(1000, 9999)

