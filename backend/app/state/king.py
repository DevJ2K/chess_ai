from numba import njit
from app.movements.king_movement_utils import is_square_under_attack
import numpy as np

@njit
def is_king_in_check(board: np.ndarray, king_x: int, king_y: int) -> bool:
    """ Checks if the king is in check. """

    is_white_king = board[king_y, king_x] > 0
    return is_square_under_attack(board, king_x, king_y, is_white_king)
