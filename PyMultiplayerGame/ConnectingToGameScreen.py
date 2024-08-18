import pygame

from Block import Block
from GameScreen import GameScreen
from Screen import Screen
import Colors
from Timer import Timer, CountdownTimer
from UI import Text, EditText, Button
from typing import Dict, Callable
from Communicator import PacketCodes
from Responses import ConnectToGameResponse, ErrorResponse, get_response
from Player import Player

class ConnectingToGameScreen(Screen):

    CONNECTING_ATTEMPTS = 5

    def __init__(self, engine):
        super().__init__(engine)

        self.top_text = None
        self.name_title_text = None
        self.name_edit_text = None
        self.connect_button = None
        self.error_text = None

        self.connecting_attempts = 0

        self.response_functions: Dict[PacketCodes, Callable[[dict], None]] = {
            PacketCodes.CONNECTED_TO_SERVER: self.on_connected_to_server,
            PacketCodes.CONNECT_TO_GAME: self.on_connected_to_game,
            PacketCodes.Error: self.on_response_error
        }

    def on_create(self):

        self.init_UI()

    def connect_to_server(self):
        self.top_text.text = "Connecting to server..."
        self.engine.communicator.connect_to_server()

    def init_UI(self):
        self.top_text = Text(pygame.Rect(255, 0, 100, 50), "", 36, Colors.BLACK)
        self.name_title_text = Text(pygame.Rect(100, 50, 100, 50), "Name ", 40, Colors.BLACK)
        self.name_edit_text = EditText(pygame.Rect(200, 50, 250, 50), "", 36, Colors.BLACK)
        self.error_text = Text(pygame.Rect(250, 150, 100, 50), "", 36, Colors.RED)
        self.connect_button = Button(pygame.Rect(200, 100, 100, 50), Colors.RED, "Connect", Colors.BLACK)
        self.connect_button.on_click_call_backs.append(self.connect_to_server)

        self.add_view(self.name_edit_text)
        self.add_view(self.top_text)
        self.add_view(self.name_title_text)
        self.add_view(self.connect_button)
        self.add_view(self.error_text)

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
        self.engine.communicator.connect_to_game(self.name_edit_text.current_text)

    def on_connected_to_game(self, data):
        response: ConnectToGameResponse = get_response(data, ConnectToGameResponse)

        blocks = []
        for block in response.blocks:
            blocks.append(Block(block.x, block.y, block.width, block.height))

        players = {}
        for player in response.players:
            players[player.name] = Player(player.position.x, player.position.y, Colors.RED, player.name)

        game_screen = GameScreen(self.engine, blocks, players, self.name_edit_text.current_text)
        self.start_screen(game_screen)

    def on_response_error(self, data):

        error_response: ErrorResponse = get_response(data, ErrorResponse)

        self.error_text.text = error_response.message
        self.engine.communicator.close()
