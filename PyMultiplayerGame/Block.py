from Sprite import Sprite

class Block(Sprite):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def update(self, keyboard):
        pass