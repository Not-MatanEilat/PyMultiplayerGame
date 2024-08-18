import pygame
import Colors
from Timer import TimerManager
from Mouse import Mouse
from Keyboard import Keyboard
from MenuScreen import MenuScreen
from Communicator import Communicator


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
        self.timer_manager = TimerManager()
        self.clock = pygame.time.Clock()
        self.communicator = Communicator(self)

        self.camera = Camera()

        self.mouse = Mouse()
        self.keyboard = Keyboard()

    def run(self, starter_screen):
        """
        Starts the engine
        :param starter_screen: The instance of the screen to start with
        """

        self.communicator.current_screen = starter_screen
        self.current_screen = starter_screen
        self.screens.append(self.current_screen)
        self.current_screen.run()
        pygame.quit()

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