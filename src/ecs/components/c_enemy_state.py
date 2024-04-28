from enum import Enum

class CEnemyState:
    def __init__(self) -> None:
        self.state = EnemyState.IDLE_FOWARD


class EnemyState(Enum):
    IDLE_FOWARD = 0
    IDLE_BACKWARD = 1
    MOVE = 2
