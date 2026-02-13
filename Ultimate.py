from Animation import Animation


class Ultimate (Animation):
    def __init__(self,):
        super().__init__(filename="Pictures/lazer.png", scale=100)

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y = 5
        if self.bottom>height:
            self.kill()