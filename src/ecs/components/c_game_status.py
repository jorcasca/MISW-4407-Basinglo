from enum import Enum

class CGameStatus:
    def __init__(self) -> None:
        self.status = GameStatus.IDLE
        self.timer = 3

class GameStatus(Enum):
    IDLE = 0
    SHOW_ALIENS = 1
    START_ALIENS = 2
    PLAYER_RESTART = 3
    START = 4
    SHOW_GAME_OVER = 5
    PAUSE = -1
    GAME_OVER = -2
