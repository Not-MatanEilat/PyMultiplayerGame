import abc

class Drawable:
    def __init__(self):
        pass

    @abc.abstractmethod
    def draw(self, screen):
        pass
