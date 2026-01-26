import random

import arcade
from pyglet.image import Animation

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 750
SCREEN_TITLE = ""
GRAVITY = 0.5
JUMP = 10


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


class Pipe(Animation):
    def __init__(self, texture, angle, is_flip):
        super().__init__(filename=texture, scale=2, flipped_horizontally=is_flip)
        self.angle = angle
        self.pipe_type = [
            arcade.load_texture("загрузка (1).png"),
            arcade.load_texture("загрузка.jpg"),
            arcade.load_texture("Без названия.png"),

        ]

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_x = -3
        if self.right <= 0:
            self.left = width
            self.texture = random.choice(self.pipe_type)
            self.hit_box = self.texture.hit_box_points


class Bird(Animation):
    def __init__(self, ):
        super().__init__(filename="загрузка (1).png", scale=0.5)
        self.angle = 0

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle
        self.change_y -= GRAVITY
        self.change_angle -= 0.4
        if self.angle < -90:
            self.angle = -90
        if self.angle > 25:
            self.angle = 25
        if self.top > SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        if self.bottom < 0:
            self.bottom = 0


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        """ Bird """
        self.bird = Bird()
        self.bird.center_x = self.width / 2
        self.bird.center_y = self.width / 2
        """ background """
        self.background_picture = arcade.load_texture("загрузка.jpg")
        """ Pipe sprite list  """
        self.pipes = arcade.SpriteList()

        """ Game reset """
        self.game_reset()

    def game_reset(self):
        self.game_status = True
        # self.player_point = 0
        self.bird.center_x = self.width / 2
        self.bird.center_y = self.height / 2
        self.bird.change_y = 0

        self.pipes = arcade.SpriteList()
        for p in range(4):
            bottom_pipe = Pipe("pixil-frame-0 (17).png", 0, is_flip=False)
            bottom_pipe.texture = random.choice(bottom_pipe.pipe_type)
            bottom_pipe.hit_box = bottom_pipe.texture.hit_box_points
            bottom_pipe.center_x = 425 * p + SCREEN_WIDTH
            bottom_pipe.center_y = 300

            top_pipe = Pipe("pixil-frame-0 (17).png", 180, is_flip=True)
            top_pipe.texture = random.choice(top_pipe.pipe_type)
            top_pipe.hit_box = top_pipe.texture.hit_box_points
            top_pipe.center_x = 425 * p + SCREEN_WIDTH
            top_pipe.center_y = SCREEN_HEIGHT - 300

            self.pipes.append(bottom_pipe)
            self.pipes.append(top_pipe)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.bird.change_y = JUMP
            self.bird.change_angle = 10

        if symbol == arcade.key.R:
            self.game_reset()

    def on_key_release(self, symbol: int, modifiers: int):
        pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height, self.background_picture)
        self.bird.draw()
        self.pipes.draw()
        self.bird.draw_hit_box((255, 0, 0), 3)
        self.pipes.draw_hit_boxes((255, 0, 0), 3)

    def on_update(self, delta_time):
        if not self.game_status:
            return

        if arcade.check_for_collision_with_list(self.bird, self.pipes):
            self.game_status = False

            return

        self.bird.movement(self.width, self.height)

        for pipe in self.pipes:
            pipe.movement(self.width, self.height)


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()