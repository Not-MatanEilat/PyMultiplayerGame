import pygame
import Colors
from Timer import CountdownTimer
from Player import Player
from UI import EditText, Button, Text
from Screen import Screen
from Sprite import Sprite
from Block import Block
from Communicator import ResponseCodes
from typing import Dict, Callable
from Game import Game


class GameScreen(Screen):
    def __init__(self, engine, blocks):
        super().__init__(engine)

        self.game = Game(engine, blocks)

        self.init_UI()

        self.text_view = Text(pygame.Rect(0, 50, 100, 50), "Time: ", 36, Colors.BLACK, self.engine.mouse)
        self.add_view(self.text_view)

        self.timer = CountdownTimer(10)
        self.timer.start()
        self.timer.on_finish = lambda: self.back_to_last_screen()

        self.response_functions: Dict[ResponseCodes, Callable[[Game], None]] = {
            ResponseCodes.MOVE: self.game.on_movement_response
        }

    def init_UI(self):
        button = Button(pygame.Rect(0, 0, 100, 50), Colors.RED, "Back", Colors.BLACK, self.engine.mouse)
        button.on_click_call_backs.append(lambda: self.back_to_last_screen())
        self.add_view(button)

    def on_packet_received(self, response_code, data):
        super()
        self.response_functions[response_code](data)


    def updates(self, events):
        super().updates(events)
        self.game.update()
        self.text_view.text = "Time: " + str(int(self.timer.get_time_is_left()))

    def draw(self):
        super().draw()
        self.game.draw()

    def dispose(self):
        self.game.update_player_position_timer.delete()