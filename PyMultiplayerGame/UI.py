import pygame
from pygame import draw
from pygame import font
import Colors
import abc
from Drawable import Drawable


class View(Drawable):
    def __init__(self, rect, static):
        super().__init__()
        self.static = static
        self.rect = rect
        self.visible = True
        self.on_click_call_backs = []

    def draw(self, screen, camera):
        if self.static:
            self.static_draw(screen)
        else:
            self.camera_draw(screen, camera)

    @abc.abstractmethod
    def static_draw(self, screen):
        pass

    @abc.abstractmethod
    def camera_draw(self, screen, camera):
        pass

    def handle_call_backs(self, mouse):
        if self.visible:
            if self.rect.collidepoint(mouse.x, mouse.y):
                if mouse.left_click.just_pressed:
                    self.on_click()

    def update(self, mouse, keyboard):
        self.handle_call_backs(mouse)

    def on_click(self):
        for call_back in self.on_click_call_backs:
            call_back()


class Image(View):
    def __init__(self, rect, image, static=True):
        super().__init__(rect, static)
        self.image = image

    def static_draw(self, screen):
        screen.blit(self.image, self.rect)

    def camera_draw(self, screen, camera):
        screen.blit(self.image, (self.rect.x - camera.game_scroll.x, self.rect.y - camera.game_scroll.y))

class Text(View):
    def __init__(self, rect, text, font_size, color, static=True):
        super().__init__(rect, static)
        self.text = text
        self.font_size = font_size
        self.color = color

    def static_draw(self, screen):
        current_font = font.Font(None, self.font_size)
        text = current_font.render(self.text, True, self.color)

        screen.blit(text, (self.rect.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y + self.rect.height / 2 - text.get_height() / 2))

    def camera_draw(self, screen, camera):
        current_font = font.Font(None, self.font_size)
        text = current_font.render(self.text, True, self.color)

        screen.blit(text, (self.rect.x - camera.game_scroll.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y - camera.game_scroll.y + self.rect.height / 2 - text.get_height() / 2))

class EditText(View):
    def __init__(self, rect, text, font_size, color, static=True):
        super().__init__(rect, static)
        self.text = text
        self.font_size = font_size
        self.color = color

        self.current_text = self.text
        self.current_color = self.color

        self.is_editing = False

        self.on_start_editing_call_back = None
        self.on_end_editing_call_back = None

    def static_draw(self, screen):
        draw.rect(screen, Colors.WHITE, self.rect)
        draw.rect(screen, Colors.BLACK, self.rect, 3)

        current_font = font.Font(None, self.font_size)
        text = current_font.render(self.current_text, True, self.current_color)
        screen.blit(text, (self.rect.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y + self.rect.height / 2 - text.get_height() / 2))

    def camera_draw(self, screen, camera):
        draw.rect(screen, Colors.WHITE, pygame.Rect(self.rect.x - camera.game_scroll.x, self.rect.y - camera.game_scroll.y, self.rect.width, self.rect.height))
        draw.rect(screen, Colors.BLACK, pygame.Rect(self.rect.x - camera.game_scroll.x, self.rect.y - camera.game_scroll.y, self.rect.width, self.rect.height), 3)

        current_font = font.Font(None, self.font_size)
        text = current_font.render(self.current_text, True, self.current_color)
        screen.blit(text, (self.rect.x - camera.game_scroll.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y - camera.game_scroll.y + self.rect.height / 2 - text.get_height() / 2))

    def update(self, mouse, keyboard):
        super(EditText, self).update(mouse, keyboard)
        self.handle_editing(mouse, keyboard)

    def handle_editing(self, mouse, keyboard):
        if self.rect.collidepoint(mouse.x, mouse.y):
            if mouse.left_click.just_pressed:
                self.is_editing = True
                if self.on_start_editing_call_back is not None:
                    self.on_start_editing_call_back()
                self.current_color = Colors.COLDGREY
        else:
            if mouse.left_click.just_pressed:
                self.is_editing = False
                if self.on_end_editing_call_back is not None:
                    self.on_end_editing_call_back()
                self.current_color = self.color

        if self.is_editing:
            if keyboard.is_key_just_pressed(pygame.K_BACKSPACE):
                self.current_text = self.current_text[:-1]
            elif keyboard.get_letter_just_pressed() is not None:
                self.on_key_down(keyboard.get_letter_just_pressed(), keyboard)

    def on_key_down(self, key, keyboard):
        if self.is_editing:
            if keyboard.get_letter_name(key) is not None:
                self.current_text += keyboard.get_letter_name(key)



class Button(View):
    def __init__(self, rect, button_color, text, text_color, static=True):
        super().__init__(rect, static)
        self.text = Text(rect, text, 36, text_color)
        self.current_button_color = button_color
        self.button_color = button_color
        self.text_color = text_color

        self.dont_change_color_on_button_hover = False

    def static_draw(self, screen):
        draw.rect(screen, self.current_button_color, self.rect)
        draw.rect(screen, Colors.BLACK, self.rect, 3)

        self.text.static_draw(screen)

    def camera_draw(self, screen, camera):
        draw.rect(screen, self.current_button_color, pygame.Rect(self.rect.x - camera.game_scroll.x, self.rect.y - camera.game_scroll.y, self.rect.width, self.rect.height))
        draw.rect(screen, Colors.BLACK, pygame.Rect(self.rect.x - camera.game_scroll.x, self.rect.y - camera.game_scroll.y, self.rect.width, self.rect.height), 3)

        self.text.camera_draw(screen, camera)

    def update(self, mouse, keyboard):
        super(Button, self).update(mouse, keyboard)
        self.handle_button_hover(mouse)

    def handle_button_hover(self, mouse):
        if not self.dont_change_color_on_button_hover:
            if self.rect.collidepoint(mouse.x, mouse.y):
                self.current_button_color = Colors.LIGHTGREY
            else:
                self.current_button_color = self.button_color
