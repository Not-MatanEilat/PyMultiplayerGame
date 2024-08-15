from Player import Player
from Block import Block
from Timer import CountdownTimer


class Game:
    def __init__(self, engine, blocks):
        self.blocks = blocks
        self.player = self.player = Player(engine.camera, 50, 50, 50, 50)

        self.engine = engine

        self.update_player_position_timer = CountdownTimer(0.1, True)
        self.update_player_position_timer.start()

        self.update_player_position_timer.on_finish = self.update_player_position

    def update(self):
        self.player.update(self.engine.keyboard, self.blocks)

    def draw(self):
        self.player.draw(self.engine.screen)
        for block in self.blocks:
            block.draw(self.engine.screen)

    def on_movement_response(self, data):
       print(data)

    def update_player_position(self):
        self.engine.communicator.update_player_position(self.player.rect.x, self.player.rect.y)
