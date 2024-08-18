import pygame
import Colors
from Timer import CountdownTimer
from Player import Player
from UI import EditText, Button, Text
from Screen import Screen
from Sprite import Sprite
from Block import Block
from Communicator import PacketCodes
from typing import Dict, Callable
from Game import Game


class GameScreen(Screen):
    def __init__(self, engine, blocks, players, local_player_name):
        super().__init__(engine)

        self.game = Game(engine, blocks, players, local_player_name)

        self.response_and_events_functions: Dict[PacketCodes, Callable[[Game], None]] = {
            PacketCodes.MOVE: self.game.on_movement_response,
            PacketCodes.UPDATE_PLAYERS: self.game.on_update_players_response
        }

    def on_packet_received(self, response_code, data):
        super()
        self.response_and_events_functions[response_code](data)


    def updates(self, events):
        super().updates(events)
        self.game.update(self.engine.keyboard)

    def draw(self):
        super().draw()
        self.game.draw(self.engine.screen, self.engine.camera)

    def dispose(self):
        self.game.update_player_position_timer.delete()
