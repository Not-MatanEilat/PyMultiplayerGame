from Sprite import Sprite

class Block(Sprite):
    def __init__(self, camera, x, y, width, height):
        super().__init__(camera, x, y, width, height)

    def update(self, keyboard):
        pass