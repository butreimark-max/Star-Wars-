from Animation import Animation
from Constants import SCREEN_HEIGHT


class All_cards_boosts  (Animation):
    def __init__(self,image,x,type ):
        super().__init__(filename=image, scale=1)
        self.type=type
        self.center_x=x
        self.center_y=SCREEN_HEIGHT/2