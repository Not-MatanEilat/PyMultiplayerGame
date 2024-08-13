from pygame import mouse
from pygame import MOUSEBUTTONDOWN
from pygame import MOUSEBUTTONUP

class Mouse:
    LEFT = 1
    RIGHT = 3
    SCROLL_UP = 4
    SCROLL_DOWN = 5

    def __init__(self):
        self.left_click = Click(self.LEFT)
        self.right_click = Click(self.RIGHT)
        self.scroll = Scroll()
        self.x = 0
        self.y = 0

    def update(self, events):
        self.x, self.y = mouse.get_pos()
        self.left_click.update(events)
        self.right_click.update(events)


class Click:
    def __init__(self, mouse_button_type):
        self.mouse_button_type = mouse_button_type

        self.holding = False
        self.just_pressed = False
        self.just_released = False

    def update(self, events):
        if self.just_pressed:
            self.just_pressed = False
            self.holding = True

        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == self.mouse_button_type:
                self.holding = True
                self.just_pressed = True
            elif event.type == MOUSEBUTTONUP and event.button == self.mouse_button_type:
                self.holding = False
                self.just_released = True


class Scroll:
    def __init__(self):
        self.up = False
        self.down = False

    def update(self, events):
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == Mouse.SCROLL_UP:
                self.up = True
            elif event.type == MOUSEBUTTONDOWN and event.button == Mouse.SCROLL_DOWN:
                self.down = True
            else:
                self.up = False
                self.down = False