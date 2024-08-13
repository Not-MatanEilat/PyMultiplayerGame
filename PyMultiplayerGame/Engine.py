import pygame
import Colors
from Timer import TimerManager
from Mouse import Mouse
from Keyboard import Keyboard
from MenuScreen import MenuScreen
from Drawable import DrawManager


pygame.init()


class Engine:
    HEIGHT = 600
    WIDTH = 800
    FPS = 60
    BACKGROUND_COLOR = Colors.LIGHTBLUE

    def __init__(self):
        self.screen = pygame.display.set_mode((Engine.WIDTH, Engine.HEIGHT))
        self.current_screen = None
        self.screens = []
        self.running = True
        self.draw_manager = DrawManager(self.current_screen)
        self.timer_manager = TimerManager()
        self.clock = pygame.time.Clock()

        self.camera = Camera()

        self.mouse = Mouse()
        self.keyboard = Keyboard()

        self.UI = Ui_Manager(self)

    def run(self, starter_screen):
        """
        Starts the engine
        :param starter_screen: The class of the screen to start with
        """
        self.current_screen = starter_screen(self)
        self.current_screen.start_screen(starter_screen)
        pygame.quit()

    def set_current_screen(self, screen):
        """
        Sets the engine to display the given screen
        :param screen: The class of the screen to display
        """
        self.current_screen = screen
        self.draw_manager.current_screen = screen
        self.UI.current_screen = screen

class Ui_Manager:
    def __init__(self, current_screen):
        self.current_screen = current_screen


    def add_view(self, view):
        self.current_screen.views.append(view)

    def update(self):
        for view in self.current_screen.views:
            view.update()

    def draw(self, screen):
        for view in self.current_screen.views:
            view.draw(screen)

    def remove_view(self, view):
        self.current_screen.views.remove(view)

    def clear(self):
        self.current_screen.views.clear()


class Camera:
    def __init__(self):
        self.game_scroll = CameraScroll()

        self.sprite_following = None
        self.is_following = False

    def update(self):
        if self.is_following:
            self.game_scroll.x = self.sprite_following.rect.x - Engine.WIDTH / 2
            self.game_scroll.y = self.sprite_following.rect.y - Engine.HEIGHT / 2

    def follow(self, sprite):
        self.is_following = True

        self.game_scroll.x = sprite.rect.x - Engine.WIDTH / 2
        self.game_scroll.y = sprite.rect.y - Engine.HEIGHT / 2
        self.sprite_following = sprite

    def stop_following(self):
        self.is_following = False

    def move_x(self, x):
        self.game_scroll.x += x

    def move_y(self, y):
        self.game_scroll.y += y


class CameraScroll:
    def __init__(self):
        self.x = 0
        self.y = 0



if __name__ == "__main__":
    game = Engine()
    game.run(MenuScreen)