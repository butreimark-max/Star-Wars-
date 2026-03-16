from Animation import Animation
from Constants import SPEED_LASER


class Shooting(Animation):
    def __init__(self,speed,texture):
        super().__init__(filename=texture, scale=0.5)
        self.speed=speed
    def movement(self, width, height):

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.change_y = self.speed

        if self.bottom>height:
            self.kill()