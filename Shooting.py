from Animation import Animation
from Constants import SPEED_LASER


class Shooting(Animation):
    def __init__(self,):
        super().__init__(filename="Pictures/lazer.png", scale=0.5)

    def movement(self, width, height):

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.change_y = SPEED_LASER

        if self.bottom>height:
            self.kill()