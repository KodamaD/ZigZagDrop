from enum import Enum, IntEnum
from typing import Tuple

class Action:
    def __init__(self, id) -> None:
        self.id = id

    def ai_action_to_tuple(self) -> Tuple[int, int]:
        pass

class ActionType(Enum):
    HUMAN = 0
    AI = 1

class HumanAction(IntEnum):
    DROP = 0
    MOVE_L = 1
    MOVE_R = 2
    ROT_L = 3
    ROT_R = 4