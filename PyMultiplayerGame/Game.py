from Player import Player
from Block import Block
from Timer import CountdownTimer
from Responses import MoveResponse, get_response

class Game:
    def __init__(self, engine, blocks):
        self.blocks = blocks
        self.player = self.player = Player(engine.camera, 50, 50, 50, 50)

        self.engine = engine

        self.update_player_position_timer = CountdownTimer(0.1, True)
        self.update_player_position_timer.start()

        self.update_player_position_timer.on_finish = self.update_player_position

        self.requests = {}
        self.next_request_id = 1

    def update(self):
        self.player.update(self.engine.keyboard, self.blocks)

    def draw(self):
        self.player.draw(self.engine.screen)
        for block in self.blocks:
            block.draw(self.engine.screen)

    def on_movement_response(self, data):
        response: MoveResponse = get_response(data, MoveResponse)

        if not response.ok or (response.position.x, response.position.y) != self.requests[response.request_id]:
            self.player.rect.x = response.position.x
            self.player.rect.y = response.position.y

        print(self.requests)
        self.requests.pop(response.request_id)

    def update_player_position(self):
        self.engine.communicator.update_player_position(self.next_request_id, self.player.rect.x, self.player.rect.y)
        # save the requests to validate with the server later
        self.requests[self.next_request_id] = self.player.rect.x, self.player.rect.y
        self.next_request_id += 1
