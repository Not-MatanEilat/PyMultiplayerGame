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

        self.player = Player(self.engine.camera, 50, 50, 50, 50)
        self.blocks = []

        self.init_UI()
        self.init_blocks()

        self.text_view = Text(pygame.Rect(0, 50, 100, 50), "Time: ", 36, Colors.BLACK, self.engine.mouse)
        self.engine.UI.add_view(self.text_view)

        self.timer = CountdownTimer(10)
        self.timer.start()
        self.timer.on_finish = lambda: self.back_to_last_screen()

    def init_UI(self):
        button = Button(pygame.Rect(0, 0, 100, 50), Colors.RED, "Back", Colors.BLACK, self.engine.mouse)
        button.on_click_call_backs.append(lambda: self.back_to_last_screen())
        self.engine.UI.add_view(button)

    def init_blocks(self):
        block1 = Block(self.engine.camera, 0, 400, 50, 50)
        block2 = Block(self.engine.camera, 50, 400, 50, 50)
        block3 = Block(self.engine.camera, 100, 400, 50, 50)
        block4 = Block(self.engine.camera, 150, 400, 50, 50)
        block5 = Block(self.engine.camera, 200, 400, 50, 50)
        block6 = Block(self.engine.camera, 250, 400, 50, 50)
        block7 = Block(self.engine.camera, 300, 400, 50, 50)

        self.blocks.append(block1)
        self.blocks.append(block2)
        self.blocks.append(block3)
        self.blocks.append(block4)
        self.blocks.append(block5)
        self.blocks.append(block6)
        self.blocks.append(block7)

    def updates(self, events):
        super().updates(events)
        self.player.update(self.engine.keyboard, self.blocks)
        self.text_view.text = "Time: " + str(int(self.timer.get_time_is_left()))

    def draw(self):
        super().draw()