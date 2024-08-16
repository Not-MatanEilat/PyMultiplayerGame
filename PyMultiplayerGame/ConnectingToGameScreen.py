import pygame

from Block import Block
from GameScreen import GameScreen
from Screen import Screen
import Colors
from Timer import Timer, CountdownTimer
from UI import Text
from typing import Dict, Callable
from Communicator import RequestCodes
from Responses import ConnectToGameResponse, get_response

class ConnectingToGameScreen(Screen):

    CONNECTING_ATTEMPTS = 5

    def __init__(self, engine):
        super().__init__(engine)

        self.top_text = None

        self.connecting_attempts = 0

        self.response_functions: Dict[RequestCodes, Callable[[dict], None]] = {
            RequestCodes.CONNECTED_TO_SERVER: self.on_connected_to_server,
            RequestCodes.CONNECT_TO_GAME: self.on_connected_to_game
        }

    def on_create(self):
        self.connect_to_server()

        self.init_UI()

    def connect_to_server(self):
        self.engine.communicator.connect_to_server()

    def init_UI(self):
        self.top_text = Text(pygame.Rect(255, 0, 100, 50), "Connecting to the game...", 36, Colors.BLACK, self.engine.mouse)
        self.add_view(self.top_text)

    def on_packet_received(self, response_code, data):
        super().on_packet_received(response_code, data)
        self.response_functions[response_code](data)

    def on_communicator_error(self, error):
        super().on_communicator_error(error)
        if isinstance(error, ConnectionRefusedError):
            if self.connecting_attempts < ConnectingToGameScreen.CONNECTING_ATTEMPTS:
                self.top_text.text = "Could not connect to server, trying again... try: " + str(self.connecting_attempts + 1)
                self.connecting_attempts += 1
                self.connect_to_server()
            else:
                self.top_text.text = "Could not connect to server, returning...."
                back_to_menu_timer = CountdownTimer(3)
                back_to_menu_timer.on_finish = lambda: self.back_to_last_screen()
                back_to_menu_timer.start()

    def on_connected_to_server(self, data):
        print("Connecting to game")
        self.engine.communicator.connect_to_game()

    def on_connected_to_game(self, data):

        response: ConnectToGameResponse = get_response(data, ConnectToGameResponse)

        blocks = []
        for block in response.blocks:
            blocks.append(Block(self.engine.camera, block.x, block.y, block.width, block.height))

        game_screen = GameScreen(self.engine, blocks)
        self.start_screen(game_screen)
