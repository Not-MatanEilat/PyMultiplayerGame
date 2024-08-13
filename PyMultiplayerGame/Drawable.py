import abc


class DrawManager:
    instance = None

    def __init__(self, current_screen):
        DrawManager.instance = self
        self.current_screen = current_screen

    @staticmethod
    def get_instance():
        if DrawManager.instance is None:
            raise Exception("DrawManager not initialized")
        return DrawManager.instance

    def add_drawable(self, drawable):
        self.current_screen.drawables.append(drawable)
        self.current_screen.drawables = sorted(self.current_screen.drawables, key=lambda draw: draw.priority)

    def draw(self, screen):
        for drawable in self.current_screen.drawables:
            drawable.draw(screen)

    def clear(self):
        self.current_screen.drawables.clear()

    def remove_drawable(self, drawable):
        self.current_screen.drawables.remove(drawable)


class Drawable:
    def __init__(self, priority=0):
        self.priority = priority
        DrawManager.get_instance().add_drawable(self)


    @abc.abstractmethod
    def draw(self, screen):
        pass
