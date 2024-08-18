import pygame

from Sprite import Sprite
import Colors
from UI import Text


class Player(Sprite):
    WIDTH = 50
    HEIGHT = 50

    def __init__(self, camera, x, y, name):
        super().__init__(camera, x, y, self.WIDTH, self.HEIGHT)

        self.name = name
        self.name_text = Text(pygame.Rect(0, 0, 100, 50), self.name, 36, Colors.BLACK)

    def update(self, keyboard, blocks):
        self.update_name_text_position()

    def draw(self, screen):
        super().draw(screen)
        self.name_text.draw(screen)

    def update_name_text_position(self):
        self.name_text.rect.x = self.rect.x + self.rect.width / 2 - self.name_text.rect.width / 2
        self.name_text.rect.y = self.rect.y - self.name_text.rect.height


class CollisionsDirections:
    def __init__(self):
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False

        self.right_block = None
        self.left_block = None
        self.top_block = None
        self.bottom_block = None

    def reset(self):
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False

        self.right_block = None
        self.left_block = None
        self.top_block = None
        self.bottom_block = None


class PlayablePlayer(Player):
    def __init__(self, camera, x, y, name):
        super().__init__(camera, x, y, name)

        self.speed = 5

        self.x_velocity = 0
        self.y_velocity = 0

        self.gravity = 0.5

        self.jump_power = 15

        self.collision_directions = CollisionsDirections()

        self.lock_all_controls = False

    def update(self, keyboard, blocks):
        super().update(keyboard, blocks)

        self.reset_collisions()

        self.move_x()
        self.get_horizontal_collisions(blocks)
        self.handle_horizontal_collisions()
        self.move_y()
        self.get_vertical_collisions(blocks)
        self.handle_vertical_collisions()

        self.handle_keyboard_presses(keyboard)
        self.handle_gravity()

    def reset_collisions(self):
        self.collision_directions.reset()



    def handle_horizontal_collisions(self):
        if self.collision_directions.left:
            self.x_velocity = 0
            self.rect.left = self.collision_directions.left_block.rect.right

        if self.collision_directions.right:
            self.x_velocity = 0
            self.rect.right = self.collision_directions.right_block.rect.left

    def handle_vertical_collisions(self):
        if self.collision_directions.top:
            self.y_velocity = 0
            self.rect.top = self.collision_directions.top_block.rect.bottom

        if self.collision_directions.bottom:
            self.y_velocity = 0
            self.rect.bottom = self.collision_directions.bottom_block.rect.top

    def handle_keyboard_presses(self, keyboard):
        if not self.lock_all_controls:
            if keyboard.is_key_down(pygame.K_a):
                self.x_velocity = -self.speed
            elif keyboard.is_key_down(pygame.K_d):
                self.x_velocity = self.speed
            else:
                self.x_velocity = 0

            if keyboard.is_key_down(pygame.K_w):
                if self.is_ground():
                    self.y_velocity = -self.jump_power

    def handle_gravity(self):
        self.y_velocity += self.gravity

    def move_x(self):
        self.rect.x += self.x_velocity

    def move_y(self):
        self.rect.y += self.y_velocity

    def get_horizontal_collisions(self, blocks):
        blocks_collided = self.current_collisions(blocks)
        for block in blocks_collided:
            if self.x_velocity > 0:
                self.rect.right = block.rect.left
                self.collision_directions.right_block = block
                self.collision_directions.right = True
            elif self.x_velocity < 0:
                self.rect.left = block.rect.right
                self.collision_directions.left_block = block
                self.collision_directions.left = True

    def get_vertical_collisions(self, blocks):
        blocks_collided = self.current_collisions(blocks)
        for block in blocks_collided:
            if self.y_velocity > 0:
                self.rect.bottom = block.rect.top
                self.collision_directions.bottom_block = block
                self.collision_directions.bottom = True
            elif self.y_velocity < 0:
                self.rect.top = block.rect.bottom
                self.collision_directions.top_block = block
                self.collision_directions.top = True

    def is_ground(self):
        return self.collision_directions.bottom


    def current_collisions(self, blocks):
        collides = []
        for block in blocks:
            if self.rect.colliderect(block.rect):
                collides.append(block)
        return collides
