import random
import time
from itertools import cycle

from arcade import draw_text

from All_cards_boosts import All_cards_boosts
from Boss import Boss
from Constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, BACKGROUND_TEXTURE, SETTINGS_TEXTURE, \
    SKIN_SHOP_TEXTURE, STATS_TEXTURE, WAVE_PREPARE_TIME, DEFAULT_FIRE_RATE, SHAKE_DURATION, SHAKE_INTENSITY, \
    PARALLAX_STRENGTH, PARALLAX_SMOOTH, HP_PLAYER, ULTIMATE_CHARGE, BOSS_WAVE, FULLSCREEN
from Enemy_Starship import Enemy_Starship
from Setting_button_orginal import Setting_button_orginal
from Shooting import Shooting
from Skin_shop_button_orginal import Skin_shop_button_orginal

import arcade

from Starship import Starship
from Ultimate import Ultimate


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=FULLSCREEN)

        """ background """
        self.background_picture = arcade.load_texture(BACKGROUND_TEXTURE)
        self.setting_picture = arcade.load_texture(SETTINGS_TEXTURE)
        self.setting_button = Setting_button_orginal()
        self.skin_shop = arcade.load_texture(SKIN_SHOP_TEXTURE)
        self.stats_bg = arcade.load_texture(STATS_TEXTURE)
        self.skin_shop_button = Skin_shop_button_orginal()

        """ Starship """
        self.star_ship_star = Starship()
        self.star_ship_star.center_x = self.width / 2
        self.star_ship_star.center_y = self.height * 0.25

        """ Enemy ship """
        self.enemy_star_ship = Enemy_Starship(angle=180, is_flip=True)
        self.enemy_star_ship.center_x = self.width / 2
        self.enemy_star_ship.center_y = self.height * 0.75

        """ Sprite lists """
        self.enemy_star_ship = arcade.SpriteList()
        self.boss_one = arcade.SpriteList()
        self.lazers = arcade.SpriteList()
        self.super_ult = arcade.SpriteList()
        self.all_card_boost = arcade.SpriteList()

        self.game_reset()

        """ game status """
        self.game_status = 1
        self.set_mouse_visible(False)
        # self.set_mouse_position(0,0)

        """ Waves"""
        self.waves = 0

        """ cooldown"""
        self.cooldown = time.time()
        self.prepare_time_left = time.time()

        """ Ultimate bar """
        self.enemy_death = 0
        self.enemy_death_for_ult=ULTIMATE_CHARGE

        """ WAVE PREPARE """
        self.wave_prepare = False
        self.prepare_start_time = 0
        self.prepare_duration = WAVE_PREPARE_TIME

        """ All cards"""
        self.all_boost_types=[
            ("Pictures/New Fire rate boost.png","fire_rate"),
            ("Pictures/fire-rate-speed-new.png","damage"),
            ("Pictures/ult charge-pixilart.png","ult_charge"),
            ("Pictures/ult-damage-pixilart (2).png","ult_damage")
        ]

        """ cooldowns """
        self.fire_rate_cooldown = DEFAULT_FIRE_RATE

        """ Statistic """
        self.stats = False

        """ Bg movement """
        self.camera = arcade.Camera(self.width, self.height)
        self.shake_duration = 0
        self.shake_intensity = 0

        self.bg_offset_x = 0
        self.bg_offset_y = 0

        self.bg_target_x = 0
        self.bg_target_y = 0

        self.parallax_strength = PARALLAX_STRENGTH
        self.parallax_smooth = PARALLAX_SMOOTH

        """" All deadth """
        self.all_deaths = 0

        """ lifes """
        self.player_lifes = HP_PLAYER


    def  create_random_cards(self):
        self.all_card_boost =arcade.SpriteList()
        boosts =self.all_boost_types
        weights = [20,30,25,25]
        positions = [self.width/2 - 400, self.width/2, self.width/2 + 400]
        chosen = random.choices(boosts, weights=weights, k=3)
        for i, boost in enumerate(chosen):
            image, boost_type = boost
            card = All_cards_boosts(image, positions[i], boost_type)
            self.all_card_boost.append(card)

    def game_over(self):
        self.game_reset()
        self.player_lifes = HP_PLAYER

    def start_shake(self, duration=0.3, intensity=10):
        self.shake_duration = duration
        self.shake_intensity = intensity

    def check_cards_buttons(self, x, y):

        for card in self.all_card_boost:
            if card.collides_with_point((x,y)):

                if card.type =="fire_rate":
                   self.fire_rate_cooldown *= 0.95
                   
                elif card.type =="damage":
                   self.star_ship_star.damage *= 1.05
                elif card.type == "ult_charge":
                   self.enemy_death_for_ult *=0.93
                elif card.type == "ult_damage":
                    self.star_ship_star.ult_damage *=1.03

                self.wave_prepare = False
                self.waves += 1
                self.game_status = 1
                self.set_mouse_visible(False)
                self.enemy_create(self.get_enemy_amount())

                return

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

    def enemy_create(self, amount_enemy):
        for p in range(amount_enemy):
            enemyl1 = Enemy_Starship(180, is_flip=True)
            enemyl1.center_x = random.randint(100, self.width - 100)
            enemyl1.bottom = self.height + 110 * p
            self.enemy_star_ship.append(enemyl1)

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        if self.game_status == 1:
            self.star_ship_star.center_x = x
            self.star_ship_star.center_y = y

            center_x = self.width / 2
            center_y = self.height / 2

            dx = x - center_x
            dy = y - center_y

            self.bg_target_x = -dx * self.parallax_strength
            self.bg_target_y = -dy * self.parallax_strength

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:

            if self.game_status == 2:
                self.check_menu_buttons(x, y)
                return

            if time.time() - self.cooldown >= self.fire_rate_cooldown:
                self.cooldown = time.time()

                lazer_shoot = Shooting()
                lazer_shoot.center_x = self.star_ship_star.center_x - 29
                lazer_shoot.center_y = self.star_ship_star.center_y + 10
                self.lazers.append(lazer_shoot)

                lazer_shoot = Shooting()
                lazer_shoot.center_x = self.star_ship_star.center_x + 29
                lazer_shoot.center_y = self.star_ship_star.center_y + 10
                self.lazers.append(lazer_shoot)

            if self.game_status == 4:
                self.check_cards_buttons(x, y)
                return
        if button == arcade.MOUSE_BUTTON_RIGHT:
            if self.enemy_death >= ULTIMATE_CHARGE:
                self.enemy_death = 0
                ult_super = Ultimate()
                ult_super.center_x = self.star_ship_star.center_x - 29
                ult_super.center_y = self.star_ship_star.center_y + 10
                self.super_ult.append(ult_super)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.TAB:
            self.stats = True

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
        if symbol == arcade.key.TAB:
            self.stats = False
    """ON draw !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    def on_draw(self):
        self.clear()
        self.camera.use()
        arcade.draw_texture_rectangle(
            center_x=self.width / 2 + self.bg_offset_x,
            center_y=self.height / 2 + self.bg_offset_y,
            width=self.width * 1.2,
            height=self.height * 1.2,
            texture=self.background_picture
        )
        self.lazers.draw()
        self.star_ship_star.draw()
        self.enemy_star_ship.draw()
        self.boss_one.draw()
        self.super_ult.draw()

        arcade.draw_text(f'Damage 100', 0, self.height - 150, font_size=20)
        arcade.draw_text(f'Fire rate: {self.fire_rate_cooldown}', 0, self.height - 200, font_size=20)
        arcade.draw_text(f'Damage:{self.star_ship_star.damage}', 0, self.height - 250, font_size=20)
        arcade.draw_text(f'Ult_damage:{self.star_ship_star.ult_damage}',0,self.height-350, font_size=20)

        arcade.draw_text(
            text=f"wave: {self.waves}",
            start_x=200,
            start_y=200,
            color=arcade.color.RED,
            font_size=50
        )
        if self.game_status == 1:
            arcade.draw_text("game", 100, 100)
            self.set_mouse_visible(False)
            arcade.draw_text(self.enemy_death, 100, 200)
            arcade.draw_text(self.waves, 100, 300)
            if self.wave_prepare:
                arcade.draw_text(f"Prepare for the wave : {self.prepare_time_left} sec",

                                 self.width / 2 - 100, self.height - 100,
                                 arcade.color.WHITE, 30)

            if self.stats == True:
                arcade.draw_texture_rectangle(
                    center_x=320,
                    center_y=self.height / 2,
                    width=self.width / 3,
                    height=self.height / 4,
                    texture=self.stats_bg,
                    alpha=150)
                arcade.draw_text(
                    text=f"enemy death:{self.enemy_death}",
                    start_x=100,
                    start_y=650,
                    color=arcade.color.RED,
                    font_size=10
                )
                arcade.draw_text(
                    text=f"wave: {self.waves}",
                    start_x=100,
                    start_y=600,
                    color=arcade.color.RED,
                    font_size=10
                )
                arcade.draw_text(
                    text=f"all kills : {self.all_deaths}",
                    start_x=100,
                    start_y=550,
                    color=arcade.color.GREEN,
                    font_size=10
                )

        if self.game_status == 2:
            arcade.draw_text("game_settings", 100, 100)
            arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height,
                                          self.setting_picture, alpha=150)
            self.setting_button.draw()
            self.skin_shop_button.draw()
            self.set_mouse_visible(True)
        if self.game_status == 3:
            arcade.draw_texture_rectangle(self.width / 2, self.height / 2, self.width, self.height,
                                          self.skin_shop, )
        if self.game_status == 4:
            self.all_card_boost.draw()
    """Update Here !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"""
    def on_update(self, delta_time):
        self.camera_movement(delta_time)

        if self.game_status == 1:
            if self.player_lifes <= 0:
                self.game_over()

            self.enemy_and_player_collision()
            self.lasser_colision()
            self.ult_colision()

            for boss in self.boss_one:
                boss.movement(self.width, self.height)

        self.waves_mechanics()

    def waves_mechanics(self):
        if len(self.enemy_star_ship) == 0 and not self.wave_prepare and self.waves != 20:
            self.wave_prepare = True
            self.game_status = 4
            self.set_mouse_visible(True)
            self.prepare_start_time = time.time()
            self.create_random_cards()

        if self.waves == BOSS_WAVE and len(self.boss_one) == 0 and not self.wave_prepare:
            self.wave_prepare = True
            self.game_status = 4
            self.set_mouse_visible(True)
            self.prepare_start_time = time.time()

            self.create_random_cards()

        if self.wave_prepare:
            elapsed = time.time() - self.prepare_start_time
            remaining = int(self.prepare_duration - elapsed)
            self.prepare_time_left = remaining

            if elapsed >= self.prepare_duration:
                self.wave_prepare = False
                self.waves += 1
                self.game_status = 1
                self.set_mouse_visible(False)
                if self.waves != 20:
                    self.enemy_create(self.get_enemy_amount())
                elif self.waves == 20:
                    self.boss_create()

    def ult_colision(self):
        for super_ult in self.super_ult:

            super_ult.movement(self.width, self.height)

            shooted = arcade.check_for_collision_with_list(super_ult, self.enemy_star_ship)
            shooted_boss = arcade.check_for_collision_with_list(super_ult, self.boss_one)

            if len(shooted) > 0:
                for enemy in shooted:
                    enemy: Enemy_Starship
                    enemy.lifes -= self.star_ship_star.ult_damage
                    self.enemy_death += 1

            if len(shooted_boss) > 0:
                for boss in shooted_boss:
                    boss: Boss
                    boss.lifes -= self.star_ship_star.ult_damage
                    self.enemy_death += 1

    def lasser_colision(self):
        for lazer in self.lazers:

            lazer.movement(self.width, self.height)

            shooted = arcade.check_for_collision_with_list(lazer, self.enemy_star_ship)
            shooted_boss = arcade.check_for_collision_with_list(lazer, self.boss_one)

            if len(shooted) > 0:
                lazer.kill()
                for enemy in shooted:
                    enemy:Enemy_Starship
                    enemy.lifes-=self.star_ship_star.damage
                    self.enemy_death += 1
                    self.all_deaths += 1

            if len(shooted_boss) > 0:
                lazer.kill()
                for boss in shooted_boss:
                    boss:Boss
                    boss.lifes -= self.star_ship_star.damage

                    self.enemy_death += 1
                    self.all_deaths += 1  # todo: add boss deaths

    def enemy_and_player_collision(self):
        for enemy in self.enemy_star_ship:
            enemy: Enemy_Starship
            enemy.movement(self.width, self.height)

            if arcade.check_for_collision(enemy, self.star_ship_star):
                enemy.kill()
                self.player_lifes -= 1
                self.start_shake(SHAKE_DURATION , SHAKE_INTENSITY )

    def camera_movement(self, delta_time: float):
        self.bg_offset_x += (self.bg_target_x - self.bg_offset_x) * self.parallax_smooth
        self.bg_offset_y += (self.bg_target_y - self.bg_offset_y) * self.parallax_smooth

        if self.shake_duration > 0:
            self.shake_duration -= delta_time

            offset_x = random.uniform(-self.shake_intensity, self.shake_intensity)
            offset_y = random.uniform(-self.shake_intensity, self.shake_intensity)

            self.camera.move((offset_x, offset_y))
        else:
            self.camera.move_to((0, 0), speed=1)

    def boss_create(self):
        boss = Boss(180, is_flip=True)
        boss.center_x = self.width / 2
        boss.center_y = self.height - 100
        self.boss_one.append(boss)


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()

"""
1. выставить карточки в норм порядке + размер подобрать
2. Сделать так, что когда нажали на краточку - нужно переключить состояние на игру
3. Нарисовать босса и остальные спрайтики (возможно, прикольные иконки для дэмеджа + файр рейт + ульт, которые будут в углу окна)
4. Сделать так, чтобы при нажатии на ТАБ отображалась статистика игрока (состояние, тру/фолс) 
"""
