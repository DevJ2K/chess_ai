from numba import njit
from app.movements.get_moves import get_valid_moves
import numpy as np


@njit
def has_available_moves(board: np.ndarray, move_history: np.ndarray) -> bool:
    """Checks if the move is available."""

    moves = get_valid_moves(board, move_history)
    return len(moves) > 0
