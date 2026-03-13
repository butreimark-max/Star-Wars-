from Animation import Animation
from Constants import HP_ENEMY, SPEED_ENEMIES


class Enemy_Starship(Animation):
    def __init__(self, angle, is_flip):
        super().__init__(filename="Pictures/Enemy ship.png", scale=2, flipped_horizontally=is_flip)
        self.angle = angle
        self.lifes = HP_ENEMY

    def movement(self,width,height):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.change_y = -SPEED_ENEMIES

        if self.top <0:
            self.bottom=height

        if self.lifes <=0:
            self.kill()