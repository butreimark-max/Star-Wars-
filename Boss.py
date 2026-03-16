from Animation import Animation
from Constants import HP_BOSS, SPEED_BOSS
from Shooting import Shooting
import time


class Boss(Animation):
    def __init__(self, angle, is_flip, main_class):
        super().__init__(filename="Pictures/boss.png.", scale=5, flipped_horizontally=is_flip)
        self.angle = angle
        self.lifes = HP_BOSS
        self.main_class = main_class
        self.boss_shoting_cooldown  = time.time()

    def shooting(self):
        lazer = Shooting(speed=3,texture="Pictures/boss-lazer-pixilart.png")
        self.main_class.boss_shooting.append(lazer)

    def movement(self,width,height):
        if time.time() - self.boss_shoting_cooldown >= 2:
            self.shooting()
            self.boss_shoting_cooldown = time.time()

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_y> height/2:
            self.change_y = -SPEED_BOSS
        else:
            self.change_y=0

        if self.top <0:
            self.bottom=height
        if self.lifes <=0:
            self.kill()


