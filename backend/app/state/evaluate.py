import numpy as np
from numba import njit
from app.state.king import is_king_in_check
from app.state.moves import has_available_moves

@njit
def evaluate_board(board: np.ndarray, game_history: np.ndarray) -> int:
    score = 0
    score += evaluate_material(board) * 1.0
    score += evaluate_mobility(board) * 0.1
    score += evaluate_king_safety(board) * 0.5
    score += evaluate_pawn_structure(board) * 0.3
    score += evaluate_center_control(board) * 0.2
    return score

@njit
def evaluate_material(board: np.ndarray) -> int:
    score = 0
    piece_values = {
        1: 1,   # Pawn
        2: 3,   # Knight
        3: 3,   # Bishop
        4: 5,   # Rook
        5: 9,   # Queen
    }

    for turn in [-1, 1]:
        for piece_value, value in piece_values.items():
            score += (np.count_nonzero(board == (piece_value * turn)) * value) * turn
    return score

# @njit
def evaluate_mobility(board: np.ndarray) -> int:...

# @njit
def evaluate_king_safety(board: np.ndarray) -> int:...

# @njit
def evaluate_pawn_structure(board: np.ndarray) -> int:...

# @njit
def evaluate_center_control(board: np.ndarray) -> int:...


# @njit
# def _evaluate_board(board: np.ndarray, game_history: np.ndarray) -> int:

#     is_white_turn = len(game_history) % 2 == 0

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
