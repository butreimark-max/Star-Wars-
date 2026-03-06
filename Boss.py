from Animation import Animation


class Boss(Animation):
    def __init__(self, angle, is_flip):
        super().__init__(filename="Pictures/boss.png.", scale=5, flipped_horizontally=is_flip)
        self.angle = angle
        self.boss_lifes = 20

    def movement(self,width,height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y = -5
        if self.top <0:
            self.bottom=height
        if self.boss_lifes <=0:
            self.kill()
        print(self.boss_lifes)

