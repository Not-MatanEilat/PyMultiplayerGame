from Player import PlayablePlayer, Player
from Block import Block
from Timer import CountdownTimer
from Responses import MoveResponse, UpdatePlayersResponse, get_response
from UI import Text


class Game:
    def __init__(self, engine, blocks, players, local_player_name):
        self.blocks = blocks
        self.local_player = self.player = PlayablePlayer(engine.camera, 50, 50, local_player_name)
        self.players: dict = players

        # remove the local player from the players list
        del self.players[local_player_name]

        self.engine = engine

        self.update_player_position_timer = CountdownTimer(0.1, True)
        self.update_player_position_timer.start()

        self.update_player_position_timer.on_finish = self.update_player_position

        self.requests = {}
        self.next_request_id = 1

    def update(self):
        self.local_player.update(self.engine.keyboard, self.blocks)

        for player in self.players.values():
            player.update(self.engine.keyboard, self.blocks)

    def draw(self):
        self.local_player.draw(self.engine.screen)
        for block in self.blocks:
            block.draw(self.engine.screen)

        for player in self.players.values():
            player.draw(self.engine.screen)


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
        print(response.players)

        for player in response.players:
            if player.name in self.players:
                self.players[player.name].rect.x = player.position.x
                self.players[player.name].rect.y = player.position.y
            elif player.name != self.local_player.name:
                self.players[player.name] = Player(self.engine.camera, player.position.x, player.position.y, player.name)

    def update_player_position(self):
        self.engine.communicator.update_player_position(self.next_request_id, self.local_player.rect.x, self.local_player.rect.y)
        # save the requests to validate with the server later
        self.requests[self.next_request_id] = self.local_player.rect.x, self.local_player.rect.y
        self.next_request_id += 1
