import pygame
import Colors
from Drawable import Drawable


class Sprite(Drawable):
    def __init__(self, x, y, width, height, color=Colors.RED):
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen, camera):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.rect.x - camera.game_scroll.x, self.rect.y - camera.game_scroll.y, self.rect.width, self.rect.height))
