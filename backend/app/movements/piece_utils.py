from numba import njit
import numpy as np


@njit
def is_in_board(board: np.ndarray, x: int, y: int):
    return 0 <= x < board.shape[1] and 0 <= y < board.shape[0]
