import arcade


class Animation(arcade.Sprite):
    time = 0
    i = 0

    def update_animation(self, delta_time: float = 1 / 60):
        self.time += delta_time
        print(delta_time)
        if self.time >= 0.2:
            self.time = 0
            if len(self.textures) - 1 == self.i:
                self.i = 0
            else:
                self.i += 1
            self.set_texture(self.i)