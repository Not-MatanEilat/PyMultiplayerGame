import Colors
from Player import PlayablePlayer, Player
from Block import Block
from Timer import CountdownTimer
from Responses import MoveResponse, UpdatePlayersResponse, get_response
from UI import Text


class Game:
    def __init__(self, engine, blocks, players, local_player_name):
        self.blocks = blocks
        self.local_player = self.player = PlayablePlayer(50, 50, Colors.BLUE, local_player_name)
        self.players: dict = players

        # remove the local player from the players list
        del self.players[local_player_name]

        engine.camera.follow(self.local_player)
        self.engine = engine

        self.update_player_position_timer = CountdownTimer(0.1, True)
        self.update_player_position_timer.start()

        self.update_player_position_timer.on_finish = self.update_player_position

        self.requests = {}
        self.next_request_id = 1

    def update(self, keyboard):
        self.local_player.update(keyboard, self.blocks)

        for player in self.players.values():
            player.update(keyboard, self.blocks)

    def draw(self, screen, camera):
        self.local_player.draw(screen, camera)
        for block in self.blocks:
            block.draw(screen, camera)

        for player in self.players.values():
            player.draw(screen, camera)


    def on_movement_response(self, data):
        response: MoveResponse = get_response(data, MoveResponse)

        if response.request_id not in self.requests:
            return

        if not response.ok or (response.position.x, response.position.y) != self.requests[response.request_id]:
            self.local_player.rect.x = response.position.x
            self.local_player.rect.y = response.position.y

        self.requests.pop(response.request_id)

    def on_update_players_response(self, data):
        response: UpdatePlayersResponse = get_response(data, UpdatePlayersResponse)

        for player in response.players:
            if player.name in self.players:
                self.players[player.name].rect.x = player.position.x
                self.players[player.name].rect.y = player.position.y
            elif player.name != self.local_player.name:
                self.players[player.name] = Player(player.position.x, player.position.y, Colors.RED, player.name)

        for player_name in list(self.players.keys()):
            if player_name not in [player.name for player in response.players]:
                del self.players[player_name]

    def update_player_position(self):
        self.engine.communicator.update_player_position(self.next_request_id, self.local_player.rect.x, self.local_player.rect.y)
        # save the requests to validate with the server later
        self.requests[self.next_request_id] = self.local_player.rect.x, self.local_player.rect.y
        self.next_request_id += 1
