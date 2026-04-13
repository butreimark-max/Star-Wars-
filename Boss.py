from Animation import Animation
from Constants import HP_BOSS, SPEED_BOSS, SPEED_BULLET_BOSS
from Shooting import Shooting
import time
import random


class Boss(Animation):
    def __init__(self, angle, is_flip, main_class):
        super().__init__(filename="Pictures/boss.png.", scale=5, flipped_horizontally=is_flip)

        self.move_diraction=random.randint(1,4)
        self.angle = angle
        self.lifes = HP_BOSS
        self.main_class = main_class
        self.boss_shoting_cooldown  = time.time()
        self.boss_stop_time = time.time()
        self.fly_down = True

        self.state = "go_down"
        self.target_x = 960
        self.target_y = 540

        self.mode = "normal"
        self.change_time = time.time()

        self.base_speed = SPEED_BOSS
        self.current_speed = SPEED_BOSS
        self.max_speed = SPEED_BOSS * 2  # предел ускорения
        self.acceleration = 0.1  # насколько быстро разгоняется

    def shooting(self):
        # right up
        lazer = Shooting(speed=3,texture="Pictures/boss-lazer-pixilart.png",type=2, dir_x=SPEED_BULLET_BOSS, dir_y=SPEED_BULLET_BOSS,)
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

    def movement(self, width, height):
        if time.time() - self.boss_shoting_cooldown >= 2:
            self.shooting()
            self.boss_shoting_cooldown = time.time()

        # если HP стало меньше 50 — переключаем режим
        if self.lifes < 50 and self.mode != "free_4dir":
            self.mode = "free_4dir"
            self.change_time = time.time()
            self.move_diraction = random.randint(1, 4)

        # применяем движение
        self.center_x += self.change_x
        self.center_y += self.change_y

        # ===== ОБЫЧНЫЙ РЕЖИМ =====
        if self.mode == "normal":

            if self.state == "go_down":
                self.change_x = 0
                self.change_y = -SPEED_BOSS

                if self.center_y <= 300:
                    self.state = "return_center"

            elif self.state == "return_center":
                dx = self.target_x - self.center_x
                dy = self.target_y - self.center_y

                if abs(dx) > 5:
                    self.change_x = SPEED_BOSS if dx > 0 else -SPEED_BOSS
                else:
                    self.change_x = 0

                if abs(dy) > 5:
                    self.change_y = SPEED_BOSS if dy > 0 else -SPEED_BOSS
                else:
                    self.change_y = 0

                if abs(dx) < 10 and abs(dy) < 10:
                    self.move_diraction = random.randint(1, 4)
                    self.state = "random_move"

            elif self.state == "random_move":
                if self.move_diraction == 1:  # вниз
                    self.change_x = 0
                    self.change_y = -SPEED_BOSS
                elif self.move_diraction == 2:  # вправо
                    self.change_x = SPEED_BOSS
                    self.change_y = 0
                elif self.move_diraction == 3:  # влево
                    self.change_x = -SPEED_BOSS
                    self.change_y = 0
                elif self.move_diraction == 4:  # вверх
                    self.change_x = 0
                    self.change_y = SPEED_BOSS

                if self.center_x < 250 or self.center_x > width - 250 or \
                        self.center_y < 250 or self.center_y > height - 250:
                    self.state = "return_center"

        # ===== РЕЖИМ ПРИ HP < 50 =====
        elif self.mode == "free_4dir":
            if self.current_speed < self.max_speed:
                self.current_speed += self.acceleration

            # раз в 1.5 секунды меняем направление
            if time.time() - self.change_time >= 1.5:
                self.move_diraction = random.randint(1, 4)
                self.change_time = time.time()

            if self.move_diraction == 1:
                self.change_x = 0
                self.change_y = -self.current_speed
            elif self.move_diraction == 2:
                self.change_x = self.current_speed
                self.change_y = 0
            elif self.move_diraction == 3:
                self.change_x = -self.current_speed
                self.change_y = 0
            elif self.move_diraction == 4:
                self.change_x = 0
                self.change_y = self.current_speed

            MARGIN = 250

            if self.center_x < MARGIN:
                self.center_x = MARGIN
                self.move_diraction = 2  # вправо

            if self.center_x > width - MARGIN:
                self.center_x = width - MARGIN
                self.move_diraction = 3  # влево

            if self.center_y < MARGIN:
                self.center_y = MARGIN
                self.move_diraction = 4  # вверх

            if self.center_y > height - MARGIN:
                self.center_y = height - MARGIN
                self.move_diraction = 1  # вниз

        if self.top < 0:
            self.bottom = height

        if self.lifes <= 0:
            self.kill()


# если высота выше чем 100:
#     летим вниз
# иначе:
#     если высота больше 500
#         просто меняем направление на рандомное