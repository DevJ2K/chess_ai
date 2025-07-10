import numpy as np
from numba import njit
from app.state.king import is_king_in_check
from app.state.moves import has_available_moves

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
                # Avantageux pour l'adversaire si le roi est en échec
                if not has_available_moves(board, game_history):
                    # Si l'adversaire n'a pas de coups disponibles, c'est un échec et mat
                    return 1000 - len(game_history)
                return 700 - len(game_history)

    return 0


# @njit
# def evaluate_player_board(board: np.ndarray, game_history: np.ndarray, ) -> int:
#     pass
