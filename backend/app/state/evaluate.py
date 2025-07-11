import numpy as np
# import tests.configuration
from numba import njit
from app.state.king import is_king_in_check
from app.state.moves import has_available_moves

@njit
def evaluate_board(board: np.ndarray, game_history: np.ndarray) -> int:
    is_white_turn = len(game_history) % 2 == 0

    score = 0
    score += int(evaluate_material(board) * 1.0)
    score += int(evaluate_mobility(board) * 0.1)
    score += int(evaluate_king_safety(board, game_history) * 0.5)
    score += int(evaluate_pawn_structure(board) * 0.3)
    score += int(evaluate_center_control(board) * 0.2)
    if is_white_turn:
        return score + (len(game_history) * 10)
    else:
        return score - (len(game_history) * 10)

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

@njit
def evaluate_mobility(board: np.ndarray) -> int:
    a = 3
    return a

@njit
def evaluate_king_safety(board: np.ndarray, game_history: np.ndarray) -> int:

    is_white_turn = len(game_history) % 2 == 0
    turn_multiplier = -1 if is_white_turn else 1

    if is_white_turn:
        positions = np.where(board == 6)
    else:
        positions = np.where(board == -6)
    if len(positions[0]) > 0:
        y, x = positions[0][0], positions[1][0]
        if is_king_in_check(board, x, y): # check
            if not has_available_moves(board, game_history):  # checkmate
                return 10000 * turn_multiplier
            return 20 * turn_multiplier # check only
        # else:
        #     # Si le roi n'est pas en échec, on ne pénalise pas
        #     # mais on peut ajouter une logique pour évaluer la sécurité du roi
        #     # par exemple, en regardant les cases autour du roi
        #     # et si elles sont contrôlées par l'adversaire.
        #     # Pour l'instant, on ne fait rien.
        #     return 0
    return 0

@njit
def evaluate_pawn_structure(board: np.ndarray) -> int:
    c = 2
    return c

@njit
def evaluate_center_control(board: np.ndarray) -> int:
    board_center = board[3:5, 3:5]

    white_pieces = np.count_nonzero(board_center > 0)
    black_pieces = np.count_nonzero(board_center < 0)
    return white_pieces - black_pieces


# @njit
# def _evaluate_board(board: np.ndarray, game_history: np.ndarray) -> int:

#     is_white_turn = len(game_history) % 2 == 0

#     if is_white_turn:
#         pass
#     else:
#         # opponent_king_value = 6 if is_white_turn else -6
#         king_value = -6
#         positions = np.where(board == king_value)
#         if len(positions[0]) > 0:
#             y, x = positions[0][0], positions[1][0]
#             if is_king_in_check(board, x, y):
#                 # Avantageux pour l'adversaire si le roi est en échec
#                 if not has_available_moves(board, game_history):
#                     # Si l'adversaire n'a pas de coups disponibles, c'est un échec et mat
#                     return 1000 - len(game_history)
#                 return 700 - len(game_history)

#     return 0


# @njit
# def evaluate_player_board(board: np.ndarray, game_history: np.ndarray, ) -> int:
#     pass

if __name__ == "__main__":
    # Example usage
    from app.chess.ChessPresets import ChessPresets
    from app.chess.Chess import Chess
    
    chess = Chess(ChessPresets.default())
    chess.apply_move_str("e4")
    print(chess)
    print(evaluate_material(chess.board))
    print(evaluate_center_control(chess.board))