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
class ConnectToGameResponse(Response):
    blocks: list[Block]

@dataclass
class Position:
    x: int
    y: int

@dataclass
class MoveResponse(Response):
    request_id: int
    position: Position

def get_response(data: dict, response_type):
    return response_type.Schema().load(data)
