from enum import Enum

class CEnemyState:
    def __init__(self) -> None:
        self.state = EnemyState.MOVE

class EnemyState(Enum):
    IDLE = 0
    MOVE = 1
