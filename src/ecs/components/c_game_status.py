from enum import Enum

class CGameStatus:
    def __init__(self) -> None:
        self.status = GameStatus.IDLE
        self.timer = 3

class GameStatus(Enum):
    IDLE = 0
    SHOW_ALIENS = 1
    START_ALIENS = 2
    START = 3
    PAUSE = -1
    GAME_OVER = -2
