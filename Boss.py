from Animation import Animation
from Constants import HP_BOSS, SPEED_BOSS


class Boss(Animation):
    def __init__(self, angle, is_flip):
        super().__init__(filename="Pictures/boss.png.", scale=5, flipped_horizontally=is_flip)
        self.angle = angle
        self.lifes = HP_BOSS

    def movement(self,width,height):

        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y = -SPEED_BOSS

        if self.top <0:
            self.bottom=height
        if self.lifes <=0:
            self.kill()


