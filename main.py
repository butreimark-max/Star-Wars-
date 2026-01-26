import arcade

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = ""
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




class Setting_button_orginal (Animation):
    def __init__(self, ):
        super().__init__(filename="Без названия.jpg", scale=0.5)
        self.center_x=750
        self.center_y=500




class Starship (Animation):
    def __init__(self, ):
        super().__init__(filename="images (1).png", scale=0.5)
        self.angle = 0

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y



class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        """ background """
        self.background_picture = arcade.load_texture("pixel-art-spaceship-flying-starry-cosmic-sky-scene-depicting-dazzling-filled-stars-colorful-nebulae-evoking-398455670.webp")
        self.setting_picture=arcade.load_texture("black-screen-background-4k.png")
        self.setting_button=Setting_button_orginal()
        """Starship """
        self. star_ship_star=Starship()
        self.star_ship_star.center_x = self.width / 2
        self.star_ship_star.center_y=self.height *0.25
        """game status """
        self.game_status=1
        self.set_mouse_visible(False)
        #self.set_mouse_position(0,0)




    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.game_status==1:
            self.star_ship_star.center_x=x



    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:

            if self.game_status==2:
                self.game_status=1
            elif self.game_status==1:
                self.game_status=2

    def on_key_release(self, symbol: int, modifiers: int):
            pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height, self.background_picture)
        self.star_ship_star.draw()
        if self.game_status==1:
            arcade.draw_text("game", 100,100)
            self.set_mouse_visible(False)
        if self.game_status == 2:
            arcade.draw_text("game_settings", 100, 100)
            arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height,
                                          self.setting_picture,alpha=150)
            self.setting_button.draw()
            self.set_mouse_visible(True)

    def on_update(self, delta_time):
        pass


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()


