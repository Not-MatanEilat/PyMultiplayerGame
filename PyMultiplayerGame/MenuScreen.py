import pygame

import Colors
from UI import EditText, Button
from Screen import Screen
from Sprite import Sprite
from GameScreen import GameScreen

class MenuScreen(Screen):
    def __init__(self, engine):
        super().__init__(engine)

        self.init_UI()

    def init_UI(self):
        button = Button(pygame.Rect(150, 150, 100, 50), Colors.RED, "Play", Colors.BLACK, self.engine.mouse)
        button.on_click_call_backs.append(lambda: self.start_screen(GameScreen))
        self.engine.UI.add_view(button)


    def updates(self, events):
        super().updates(events)

    def draw(self):
        super().draw()
