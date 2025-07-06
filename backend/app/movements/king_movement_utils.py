import numpy as np
from numba import njit
from app.movements.piece_utils import is_in_board

@njit
def is_king_in_check(board: np.ndarray, king_x: int, king_y: int):
    is_white_king = board[king_y, king_x] > 0
    return is_square_under_attack(board, king_x, king_y, is_white_king)

@njit
def is_square_under_attack(board: np.ndarray, x: int, y: int, is_white_piece: bool):
    enemy_multiplier = -1 if is_white_piece else 1

    # Check for pawn attacks
    pawn_direction = -1 if is_white_piece else 1
    for dx in [-1, 1]:
        new_x, new_y = x + dx, y + pawn_direction
        if (is_in_board(board, new_x, new_y) and
            board[new_y, new_x] == enemy_multiplier * 1):  # Enemy pawn
            return True

    # Check for knight attacks
    knight_moves = np.array([
        (1, 2), (2, 1), (2, -1), (1, -2),
        (-1, -2), (-2, -1), (-2, 1), (-1, 2)
    ], dtype=np.int8)

    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if (is_in_board(board, new_x, new_y) and
            board[new_y, new_x] == enemy_multiplier * 2):  # Enemy knight
            return True

    # Check for diagonal attacks (bishop, queen, king)
    diagonal_dirs = np.array([(1, 1), (1, -1), (-1, -1), (-1, 1)], dtype=np.int8)
    for dx, dy in diagonal_dirs:
        new_x, new_y = x + dx, y + dy
        distance = 1
        while is_in_board(board, new_x, new_y):
            piece = board[new_y, new_x]
            if piece != 0:
                if piece == enemy_multiplier * 3:  # Enemy bishop
                    return True
                elif piece == enemy_multiplier * 4:  # Enemy queen
                    return True
                elif piece == enemy_multiplier * 6 and distance == 1:  # Adjacent enemy king
                    return True
                break
            new_x += dx
            new_y += dy
            distance += 1

    # Check for horizontal/vertical attacks (rook, queen, king)
    straight_dirs = np.array([(1, 0), (0, 1), (-1, 0), (0, -1)], dtype=np.int8)
    for dx, dy in straight_dirs:
        new_x, new_y = x + dx, y + dy
        distance = 1
        while is_in_board(board, new_x, new_y):
            piece = board[new_y, new_x]
            if piece != 0:
                if piece == enemy_multiplier * 5:  # Enemy rook
                    return True
                elif piece == enemy_multiplier * 4:  # Enemy queen
                    return True
                elif piece == enemy_multiplier * 6 and distance == 1:  # Adjacent enemy king
                    return True
                break
            new_x += dx
            new_y += dy
            distance += 1

    return False

@njit
def can_castle_kingside(board: np.ndarray, king_x: int, king_y: int, rook_has_moved: bool):
    """Checks if kingside castling is possible."""
    if rook_has_moved:
        return False

    # Check that the rook is in its initial position
    expected_rook_value = 4 if board[king_y, king_x] > 0 else -4
    if board[king_y, 7] != expected_rook_value:
        return False

    # Check that the squares between the king and rook are empty
    for x in range(king_x + 1, 7):
        if board[king_y, x] != 0:
            return False

    # Check that the king does not pass through an attacked square
    for x in range(king_x + 1, king_x + 3):
        if is_square_under_attack(board, x, king_y, board[king_y, king_x] > 0):
            return False

    return True

@njit
def can_castle_queenside(board: np.ndarray, king_x: int, king_y: int, rook_has_moved: bool):
    """Checks if queenside castling is possible."""
    if rook_has_moved:
        return False

    # Check that the rook is in its initial position
    expected_rook_value = 4 if board[king_y, king_x] > 0 else -4
    if board[king_y, 0] != expected_rook_value:
        return False

    # Check that the squares between the king and rook are empty
    for x in range(1, king_x):
        if board[king_y, x] != 0:
            return False

    # Check that the king does not pass through an attacked square
    for x in range(king_x - 2, king_x + 1):
        if is_square_under_attack(board, x, king_y, board[king_y, king_x] > 0):
            return False

    return True
