import random
import time
from itertools import cycle

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
class Skin_shop_button_orginal (Animation):
    def __init__(self, ):
        super().__init__(filename="Skins button.png", scale=5)
        self.center_x=SCREEN_WIDTH/2
        self.center_y=500
class Ultimate (Animation):
    def __init__(self,):
        super().__init__(filename="lazer.png", scale=100)

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y = 5
        if self.bottom>height:
            self.kill()
class Shooting(Animation):
    def __init__(self,):
        super().__init__(filename="lazer.png", scale=0.5)

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y = 5
        if self.bottom>height:
            self.kill()
class Enemy_Starship(Animation):
    def __init__(self, angle, is_flip):
        super().__init__(filename="Enemy ship.png", scale=2, flipped_horizontally=is_flip)
        self.angle = angle
    def movement(self,width,height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.change_y = -5
        if self.top <0:
            self.bottom=height




class Starship (Animation):
    def __init__(self, ):
        super().__init__(filename="pixilart-drawing (6).png", scale=1)
        self.angle = 0

    def movement(self, width, height):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom < 0:
            self.bottom = 0
        if self.top > 100:
            self.top = 100


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        """ background """
        self.background_picture = arcade.load_texture("pixilart-drawing (5).png")
        self.setting_picture=arcade.load_texture("black-screen-background-4k.png")
        self.setting_button=Setting_button_orginal()
        self.skin_shop=arcade.load_texture("Skin Shop.png")

        self.skin_shop_button =Skin_shop_button_orginal()
        """Starship """
        self. star_ship_star=Starship()
        self.star_ship_star.center_x = self.width / 2
        self.star_ship_star.center_y=self.height *0.25
        """Enemy ship """
        self.enemy_star_ship = Enemy_Starship(angle=180,is_flip=True)

        self.enemy_star_ship.center_x = self.width / 2
        self.enemy_star_ship.center_y = self.height * 0.75
        """ Sprite lists """
        self.enemy_star_ship =arcade.SpriteList()
        self.lazers =arcade.SpriteList()
        self.super_ult =arcade.SpriteList()
        self.game_reset()
        """game status """
        self.game_status=1
        self.set_mouse_visible(False)
        #self.set_mouse_position(0,0)
        """Waves"""
        self.waves=1
        """cooldown"""
        self.cooldown=time.time()
        """Ultimate bar """
        self.enemy_death=0
        """ WAVE PREPARE """
        self.wave_prepare = False
        self.prepare_start_time = 0
        self.prepare_duration =   5

    def check_menu_buttons(self, x, y):
        if self.skin_shop_button.collides_with_point((x, y)):

            self.game_status = 3

    def game_reset(self):
        self.game_status = 1
        self.enemy_star_ship = arcade.SpriteList()
        self.star_ship_star.center_x = self.width / 2
        self.star_ship_star.center_y = self.height * 0.25
        self.waves = 1
        self.enemy_create(5)


    def enemy_create(self,amount_enemy):
        for p in range(amount_enemy):
            enemyl1 = Enemy_Starship(180, is_flip=True)
            enemyl1.center_x=random.randint(100,self.width-100)
            enemyl1.bottom = self.height + 110 *p

            self.enemy_star_ship.append(enemyl1)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.game_status==1:
            self.star_ship_star.center_x=x
            self.star_ship_star.center_y=y
    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button==arcade.MOUSE_BUTTON_LEFT:
            if self.game_status == 2:
                self.check_menu_buttons(x, y)
                return
            if time.time()-self.cooldown>=0.5:
                self.cooldown=time.time()
                lazer_shoot = Shooting()
                lazer_shoot .center_x =self.star_ship_star.center_x-29
                lazer_shoot .center_y =self.star_ship_star.center_y+10

                self.lazers.append(lazer_shoot )
                lazer_shoot = Shooting()
                lazer_shoot .center_x =self.star_ship_star.center_x+29
                lazer_shoot .center_y =self.star_ship_star.center_y+10

                self.lazers.append(lazer_shoot )
        if button==arcade.MOUSE_BUTTON_RIGHT:
            if self.enemy_death>=10:
                self.enemy_death=0


                ult_super = Ultimate()
                ult_super .center_x =self.star_ship_star.center_x-29
                ult_super .center_y =self.star_ship_star.center_y+10



                self.super_ult.append(ult_super )





    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            if self.game_status == 3:
                self.game_status = 2
            elif self.game_status == 2:
                self.game_status = 1
            elif self.game_status == 1:
                self.game_status = 2


    def get_enemy_amount(self):
        return 5 + (self.waves - 1) * 5

    def on_key_release(self, symbol: int, modifiers: int):
            pass

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height, self.background_picture)
        self.lazers.draw()
        self.star_ship_star.draw()
        self.enemy_star_ship.draw()
        self.super_ult.draw()
        if self.game_status==1:
            arcade.draw_text("game", 100,100)
            self.set_mouse_visible(False)
            arcade.draw_text(self.enemy_death, 100, 200)
            arcade.draw_text(self.waves, 100, 300)
            if self.wave_prepare:
                arcade.draw_text(f"Prepare for the wave : {self.prepare_time_left} sec",
                                 self.width / 2 - 100, self.height - 100,
                                 arcade.color.WHITE, 30)

        if self.game_status == 2:
            arcade.draw_text("game_settings", 100, 100)
            arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height,
                                          self.setting_picture,alpha=150)
            self.setting_button.draw()
            self.skin_shop_button.draw()
            self.set_mouse_visible(True)
        if self.game_status ==3:
            arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height,
                                          self.skin_shop, )


    def on_update(self, delta_time):
        if self.game_status==1:
            for enemy in self.enemy_star_ship:
                enemy.movement(self.width, self.height)
            for lazer in self.lazers:
                lazer.movement(self.width, self.height)
                shooted=arcade.check_for_collision_with_list(lazer,self.enemy_star_ship)
                if len(shooted)>0:
                    lazer.kill()
                    for enemy in shooted:
                        enemy.kill()
                        self.enemy_death +=1

            for super_ult in self.super_ult:
                super_ult.movement(self.width, self.height)
                shooted = arcade.check_for_collision_with_list(super_ult, self.enemy_star_ship)
                if len(shooted) > 0:

                    for enemy in shooted:
                        enemy.kill()
                        self.enemy_death += 1



        if len(self.enemy_star_ship) == 0 and not self.wave_prepare:
            self.wave_prepare = True
            self.prepare_start_time = time.time()

        if self.wave_prepare:
            elapsed = time.time() - self.prepare_start_time
            remaining = int(self.prepare_duration - elapsed)
            self.prepare_time_left = remaining

            if elapsed >= self.prepare_duration:

                self.wave_prepare = False
                self.waves += 1
                self.enemy_create(self.get_enemy_amount())





window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()


