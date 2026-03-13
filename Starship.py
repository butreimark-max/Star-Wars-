from Animation import Animation
from Constants import DAMAGE_PLAYER, ULT_DAMAGE_PLAYER


class Starship (Animation):
    def __init__(self, ):
        super().__init__(filename="Pictures/pixilart-drawing (6).png", scale=1)
        self.angle = 0
        self.damage= DAMAGE_PLAYER
        self.ult_damage=ULT_DAMAGE_PLAYER

    def movement(self, width, height):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.bottom < 0:
            self.bottom = 0

        if self.top > 100:
            self.top = 100
