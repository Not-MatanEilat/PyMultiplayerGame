import pygame
from pygame import key as pygame_key
from copy import deepcopy


class Keyboard:
    def __init__(self):
        self.last_keys = {}
        self.keys = {}


    def update(self):
        self.last_keys = deepcopy(self.keys)
        self.keys = pygame_key.get_pressed()
    def is_key_down(self, key):
        return self.keys[key]

    def is_key_up(self, key):
        return not self.keys[key]

    def is_key_just_pressed(self, key):
        return self.keys[key] and not self.last_keys[key]

    def is_key_just_released(self, key):
        return not self.keys[key] and self.last_keys[key]

    def get_letter_name(self, key):
        if self.is_key_a_letter(key):
            if self.is_key_down(pygame.K_LSHIFT) or self.is_key_down(pygame.K_RSHIFT):
                return pygame.key.name(key).upper()
            else:
                return pygame.key.name(key)

        if self.is_key_a_number(key):
            if self.is_key_down(pygame.K_LSHIFT) or self.is_key_down(pygame.K_RSHIFT):
                return ")!@#$%^&*("[key - 48]
            else:
                return pygame.key.name(key)
        if key == pygame.K_MINUS:
            if self.is_key_down(pygame.K_LSHIFT) or self.is_key_down(pygame.K_RSHIFT):
                return "_"
            else:
                return "-"
        if key == pygame.K_EQUALS:
            if self.is_key_down(pygame.K_LSHIFT) or self.is_key_down(pygame.K_RSHIFT):
                return "+"
            else:
                return "="

        if key == pygame.K_SPACE:
            return " "


    def is_key_a_letter(self, key):
        return 97 <= key <= 122

    def is_key_a_number(self, key):
        return 48 <= key <= 57

    def get_letter_just_pressed(self):
        for key, state in enumerate(self.keys):
            if self.keys[key] and not self.last_keys[key]:
                return key

