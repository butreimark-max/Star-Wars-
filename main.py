import random
import time
from itertools import cycle

from All_cards_boosts import All_cards_boosts
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from Enemy_Starship import Enemy_Starship
from Setting_button_orginal import Setting_button_orginal
from Shooting import Shooting
from  Skin_shop_button_orginal import Skin_shop_button_orginal

import arcade

from Starship import Starship
from Ultimate import Ultimate

















class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        """ background """
        self.background_picture = arcade.load_texture("Pictures/pixilart-drawing (5).png")
        self.setting_picture=arcade.load_texture("Pictures/black-screen-background-4k.png")
        self.setting_button=Setting_button_orginal()
        self.skin_shop=arcade.load_texture("Pictures/Skin Shop.png")

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
        self.all_card_boost =arcade.SpriteList()

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
        """All cards"""

        self.boost_fr=All_cards_boosts("Pictures/Fire rate card.png",100,"fire_rate")
        self.all_card_boost.append(self.boost_fr)
        self.boost_d = All_cards_boosts("Pictures/Damage.png", 300, "damage")
        self.all_card_boost.append(self.boost_d)
        self.boost_Ult = All_cards_boosts("Pictures/Ult.png", 500, "ult_charge")
        self.all_card_boost.append(self.boost_Ult)
        """ cooldowns"""
        self.fire_rate_cooldown=0.6



    def check_cards_buttons(self, x, y):
        if self.boost_fr.collides_with_point((x, y)):
            self.fire_rate_cooldown=self.fire_rate_cooldown * (1-5/100)
            print(self.fire_rate_cooldown)
        if self.boost_d.collides_with_point((x, y)):
            pass
        if self.boost_Ult.collides_with_point((x, y)):
            pass

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
            if time.time()-self.cooldown>=self.fire_rate_cooldown:
                self.cooldown=time.time()
                lazer_shoot = Shooting()
                lazer_shoot .center_x =self.star_ship_star.center_x-29
                lazer_shoot .center_y =self.star_ship_star.center_y+10

                self.lazers.append(lazer_shoot )
                lazer_shoot = Shooting()
                lazer_shoot .center_x =self.star_ship_star.center_x+29
                lazer_shoot .center_y =self.star_ship_star.center_y+10

                self.lazers.append(lazer_shoot )
            if self.game_status==4:
                self.check_cards_buttons(x, y)
                return
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

        arcade.draw_text(f'Damage 100', 0, self.height - 100, font_size=20)
        arcade.draw_text(f'Fire rate: {self.fire_rate_cooldown}', 0, self.height - 150, font_size=20)
        arcade.draw_text(f'Damage 100', 0, self.height - 200, font_size=20)

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
        if self.game_status == 4:
            self.all_card_boost.draw()


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
            self.game_status=4
            self.set_mouse_visible(True)
            self.prepare_start_time = time.time()

        if self.wave_prepare:
            elapsed = time.time() - self.prepare_start_time
            remaining = int(self.prepare_duration - elapsed)
            self.prepare_time_left = remaining

            if elapsed >= self.prepare_duration:

                self.wave_prepare = False
                self.waves += 1
                self.game_status=1
                self.set_mouse_visible(False)
                self.enemy_create(self.get_enemy_amount())



window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()


"""
1. выставить карточки в норм порядке + размер подобрать
2. Сделать так, что когда нажали на краточку - нужно переключить состояние на игру
3. Нарисовать босса и остальные спрайтики (возможно, прикольные иконки для дэмеджа + файр рейт + ульт, которые будут в углу окна)
4. Сделать так, чтобы при нажатии на ТАБ отображалась статистика игрока (состояние, тру/фолс) 
"""