import random

from Animation import Animation
from Constants import SPEED_LASER


class Shooting(Animation):
    def __init__(self,speed,texture,type, dir_x, dir_y):
        super().__init__(filename=texture, scale=1)
        if type == 1:
            self.scale = 1
        else:
            self.scale = 5

        self.speed=speed
        self.type=type

        self.dir_x = dir_x
        self.dir_y = dir_y

    def movement(self, width, height):

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.type==1:
            self.change_y = self.speed

        elif self.type ==2:
            self.change_x = self.dir_x
            self.change_y = self.dir_y

        if self.bottom>height:
            self.kill()