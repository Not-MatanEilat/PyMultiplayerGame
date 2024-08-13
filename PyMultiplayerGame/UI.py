import pygame
from pygame import draw
from pygame import font
import Colors
import abc
from Drawable import Drawable


class View(Drawable):
    def __init__(self, rect, mouse):
        super().__init__()
        self.rect = rect
        self.mouse = mouse
        self.visible = True
        self.on_click_call_backs = []

    @abc.abstractmethod
    def draw(self, screen):
        pass

    def handle_call_backs(self):
        if self.visible:
            if self.rect.collidepoint(self.mouse.x, self.mouse.y):
                if self.mouse.left_click.just_pressed:
                    self.on_click()

    def update(self):
        self.handle_call_backs()

    def on_click(self):
        for call_back in self.on_click_call_backs:
            call_back()


class Image(View):
    def __init__(self, rect, image, mouse):
        super().__init__(rect, mouse)
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Text(View):
    def __init__(self, rect, text, font_size, color, mouse):
        super().__init__(rect, mouse)
        self.text = text
        self.font_size = font_size
        self.color = color

    def draw(self, screen):
        current_font = font.Font(None, self.font_size)
        text = current_font.render(self.text, True, self.color)
        screen.blit(text, (self.rect.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y + self.rect.height / 2 - text.get_height() / 2))


class EditText(View):
    def __init__(self, rect, text, font_size, color, mouse, keyboard):
        super().__init__(rect, mouse)
        self.keyboard = keyboard
        self.text = text
        self.font_size = font_size
        self.color = color

        self.current_text = self.text
        self.current_color = self.color

        self.is_editing = False

        self.on_start_editing_call_back = None
        self.on_end_editing_call_back = None

    def draw(self, screen):
        draw.rect(screen, Colors.WHITE, self.rect)
        draw.rect(screen, Colors.BLACK, self.rect, 3)

        current_font = font.Font(None, self.font_size)
        text = current_font.render(self.current_text, True, self.current_color)
        screen.blit(text, (self.rect.x + self.rect.width / 2 - text.get_width() / 2,
                           self.rect.y + self.rect.height / 2 - text.get_height() / 2))

    def update(self):
        super(EditText, self).update()
        self.handle_editing()

    def handle_editing(self):
        if self.rect.collidepoint(self.mouse.x, self.mouse.y):
            if self.mouse.left_click.just_pressed:
                self.is_editing = True
                if self.on_start_editing_call_back is not None:
                    self.on_start_editing_call_back()
                self.current_color = Colors.LIGHTGREY
        else:
            if self.mouse.left_click.just_pressed:
                self.is_editing = False
                if self.on_end_editing_call_back is not None:
                    self.on_end_editing_call_back()
                self.current_color = self.color

        if self.is_editing:
            if self.keyboard.is_key_just_pressed(pygame.K_BACKSPACE):
                self.current_text = self.current_text[:-1]
            elif self.keyboard.get_letter_just_pressed() is not None:
                self.on_key_down(self.keyboard.get_letter_just_pressed())

    def on_key_down(self, key):
        if self.is_editing:
            if self.keyboard.get_letter_name(key) is not None:
                self.current_text += self.keyboard.get_letter_name(key)



class Button(View):
    def __init__(self, rect, button_color, text, text_color, mouse):
        super().__init__(rect, mouse)
        self.text = Text(rect, text, 36, text_color, mouse)
        self.current_button_color = button_color
        self.button_color = button_color
        self.text_color = text_color

        self.dont_change_color_on_button_hover = False

    def draw(self, screen):
        draw.rect(screen, self.current_button_color, self.rect)
        draw.rect(screen, Colors.BLACK, self.rect, 3)

        self.text.draw(screen)

    def update(self):
        super(Button, self).update()
        self.handle_button_hover()

    def handle_button_hover(self):
        if not self.dont_change_color_on_button_hover:
            if self.rect.collidepoint(self.mouse.x, self.mouse.y):
                self.current_button_color = Colors.LIGHTGREY
            else:
                self.current_button_color = self.button_color
