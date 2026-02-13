from Animation import Animation
from Constants import SCREEN_WIDTH


class Skin_shop_button_orginal (Animation):
    def __init__(self, ):
        super().__init__(filename="Pictures/Skins button.png", scale=5)
        self.center_x=SCREEN_WIDTH/2
        self.center_y=500