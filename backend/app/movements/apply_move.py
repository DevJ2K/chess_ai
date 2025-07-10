import numpy as np
from numba import njit


@njit
def apply_move(board: np.ndarray, move: np.ndarray, promotion: np.int8) -> bool:
    if move.shape != (2, 3):
        print("Invalid move shape:", move.shape)
        return False

    start_x, start_y, piece = move[0]
    dest_x, dest_y, _ = move[1]

    #################################
    # Handle castling
    #################################
    if piece == 6 and (start_x, start_y) == (4, 0) and (dest_x, dest_y) == (6, 0):  # Kingside castling for white
        board[0, 7] = 0
        board[0, 5] = 4
    elif piece == 6 and (start_x, start_y) == (4, 0) and (dest_x, dest_y) == (2, 0):  # Queenside castling for white
        board[0, 0] = 0
        board[0, 3] = 4
    elif piece == -6 and (start_x, start_y) == (4, 7) and (dest_x, dest_y) == (6, 7):  # Kingside castling for black
        board[7, 7] = 0
        board[7, 5] = -4
    elif piece == -6 and (start_x, start_y) == (4, 7) and (dest_x, dest_y) == (2, 7):  # Queenside castling for black
        board[7, 0] = 0
        board[7, 3] = -4

    #################################
    # Handle promotions
    #################################
    if abs(piece) == 1:  # Pawn
        if (piece > 0 and dest_y == 7) or (piece < 0 and dest_y == 0):
            if promotion not in [2, 3, 4, 5]:
                print("Invalid promotion piece:", promotion)
                return False
            piece *= promotion

    board[start_y, start_x] = 0
    board[dest_y, dest_x] = piece
    return True
