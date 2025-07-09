import numpy as np
from numba import njit
from app.state.king import is_king_in_check

@njit
def evaluate_board(board: np.ndarray, game_history: np.ndarray) -> int:

    is_white_turn = len(game_history) % 2 == 0

    if is_white_turn:
        pass
    else:
        # opponent_king_value = 6 if is_white_turn else -6
        king_value = -6
        positions = np.where(board == king_value)
        if len(positions[0]) > 0:
            y, x = positions[0][0], positions[1][0]
            if is_king_in_check(board, x, y):
                return 1000
        pass

    return 0
