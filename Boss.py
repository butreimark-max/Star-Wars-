from Animation import Animation
from Constants import HP_BOSS, SPEED_BOSS, SPEED_BULLET_BOSS
from Shooting import Shooting
import time
import random


class Boss(Animation):
    def __init__(self, angle, is_flip, main_class):
        super().__init__(filename="Pictures/boss.png.", scale=5, flipped_horizontally=is_flip)

        self.move_diraction=random.randint(1,4)
        self.move_diraction=0
        self.angle = angle
        self.lifes = HP_BOSS
        self.main_class = main_class
        self.boss_shoting_cooldown  = time.time()
        self.boss_stop_time = time.time()
        self.fly_down = True

    def shooting(self):
        # right up
        lazer = Shooting(speed=3,texture="Pictures/boss-lazer-pixilart.png",type=2, dir_x=SPEED_BULLET_BOSS, dir_y=SPEED_BULLET_BOSS)
        lazer.center_x=self.center_x
        lazer.center_y= self.center_y+20
        self.main_class.boss_shooting.append(lazer)
        # right down
        lazer = Shooting(speed=3, texture="Pictures/boss-lazer-pixilart.png", type=2, dir_x=SPEED_BULLET_BOSS, dir_y=-SPEED_BULLET_BOSS)
        lazer.center_x = self.center_x
        lazer.center_y = self.center_y + 20
        self.main_class.boss_shooting.append(lazer)

        lazer = Shooting(speed=3, texture="Pictures/boss-lazer-pixilart.png", type=2, dir_x=-SPEED_BULLET_BOSS, dir_y=-SPEED_BULLET_BOSS)
        lazer.center_x = self.center_x
        lazer.center_y = self.center_y + 20
        self.main_class.boss_shooting.append(lazer)

        lazer = Shooting(speed=3, texture="Pictures/boss-lazer-pixilart.png", type=2, dir_x=-SPEED_BULLET_BOSS, dir_y=SPEED_BULLET_BOSS)
        lazer.center_x = self.center_x
        lazer.center_y = self.center_y + 20
        self.main_class.boss_shooting.append(lazer)

    def movement(self,width,height):
        if time.time() - self.boss_shoting_cooldown >= 2:
            self.shooting()
            self.boss_shoting_cooldown = time.time()

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.fly_down:   # если разрешено лететь вниз
            if self.center_y> height/2:
                self.change_y = -SPEED_BOSS
            else:
                self.change_y=0
                self.fly_down = False   # дошёл до конца и запрещаем лететь вниз

        if not self.fly_down:
            if self.move_diraction==1:  # down
                self.change_y=-SPEED_BOSS
                self.change_x=0
            if self.move_diraction==2:  # right
                self.change_y=0
                self.change_x=SPEED_BOSS
            if self.move_diraction==3:  # left
                self.change_x=-SPEED_BOSS
                self.change_y=0
            if self.move_diraction == 4:    # up
                self.change_y = SPEED_BOSS
                self.change_x = 0


        if self.top <0:
            self.bottom=height
        if self.lifes <=0:
            self.kill()


