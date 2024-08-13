import pygame
import Colors
from Drawable import Drawable


class Sprite(Drawable):
    def __init__(self, camera, x, y, width, height):
        super().__init__()
        self.camera = camera

        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, Colors.RED, pygame.Rect(self.rect.x - self.camera.game_scroll.x, self.rect.y - self.camera.game_scroll.y, self.rect.width, self.rect.height))
