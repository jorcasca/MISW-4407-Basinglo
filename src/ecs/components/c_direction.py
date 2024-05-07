from enum import Enum

class CDirection:
    def __init__(self) -> None:
        self.direction_x = PlayerDirection.IDLE

class PlayerDirection(Enum):
    LEFT = -1
    IDLE = 0
    RIGHT = 1
