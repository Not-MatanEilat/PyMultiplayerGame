from marshmallow_dataclass import dataclass


@dataclass
class Response:
    ok: bool

@dataclass
class Block:
    x: int
    y: int
    width: int
    height: int

@dataclass
class Position:
    x: int
    y: int

@dataclass
class MoveResponse(Response):
    request_id: int
    position: Position
@dataclass
class Player:
    name: str
    position: Position


@dataclass
class ConnectToGameResponse(Response):
    blocks: list[Block]
    players: list[Player]

@dataclass
class ErrorResponse(Response):
    message: str




@dataclass
class UpdatePlayersResponse(Response):
    players: list[Player]

def get_response(data: dict, response_type):
    return response_type.Schema().load(data)
