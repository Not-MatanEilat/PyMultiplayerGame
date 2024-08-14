import pygame
import Colors
from Timer import CountdownTimer
from Player import Player
from UI import EditText, Button, Text
from Screen import Screen
from Sprite import Sprite
from Block import Block


class GameScreen(Screen):
    def __init__(self, engine):
        super().__init__(engine)

        self.player = Player(self.engine.camera, self.engine.communicator, 50, 50, 50, 50)
        self.blocks = []

        self.init_UI()
        self.init_blocks()

        self.text_view = Text(pygame.Rect(0, 50, 100, 50), "Time: ", 36, Colors.BLACK, self.engine.mouse)
        self.engine.UI.add_view(self.text_view)

        self.timer = CountdownTimer(10)
        self.timer.start()
        self.timer.on_finish = lambda: self.back_to_last_screen()

        self.connect_to_game()

    def connect_to_game(self):
        self.engine.communicator.connect_to_server()
        self.engine.communicator.connect_to_game()

    def init_UI(self):
        button = Button(pygame.Rect(0, 0, 100, 50), Colors.RED, "Back", Colors.BLACK, self.engine.mouse)
        button.on_click_call_backs.append(lambda: self.back_to_last_screen())
        self.engine.UI.add_view(button)

    def init_blocks(self):
        pass

    def updates(self, events):
        super().updates(events)
        self.player.update(self.engine.keyboard, self.blocks)
        self.text_view.text = "Time: " + str(int(self.timer.get_time_is_left()))

    def draw(self):
        super().draw()