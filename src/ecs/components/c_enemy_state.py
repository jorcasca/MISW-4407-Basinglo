from enum import Enum

class CEnemyState:
    def __init__(self) -> None:
        self.state = EnemyState.IDLE


class EnemyState(Enum):
    IDLE = 0
    CHASE = 1
    RETURN = 2
    ROTATE = 3
