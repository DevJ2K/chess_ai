from enum import Enum


class MoveResult(Enum):
    SUCCESS = 1
    INVALID_SHAPE = 2
    INVALID_PROMOTION = 3
    CASTLING_ERROR = 4