from numba import njit
from app.movements.get_movements import get_valid_moves
from app.movements.king_movement_utils import is_king_in_check
import numpy as np


@njit
def get_king_status(board: np.ndarray, move_history: np.ndarray, move: np.ndarray, x: int, y: int) -> int:
    """
    Returns the status of the king at position (x, y).
    1 if the king is in check, 0 if not.
    """
    result_king_in_check = 1 if is_king_in_check(board, x, y) else 0
    result_number_of_moves = 1 if len(get_valid_moves(board, np.append(move_history, np.expand_dims(move, axis=0), axis=0))) > 0 else 0

    return np.array([result_king_in_check, result_number_of_moves], dtype=np.int8)
