import numpy as np

###########################################
# Chess default board preset
###########################################
def chess_preset_default():
    board = np.zeros((8, 8), dtype=np.int8)

    # White pieces
    board[1, :] = 1   # pawns
    board[0, 2] = board[0, 5] = 2   # bishops
    board[0, 1] = board[0, 6] = 3   # knights
    board[0, 0] = board[0, 7] = 4   # rooks
    board[0, 3] = 5   # queen
    board[0, 4] = 6   # king

    # Black pieces
    board[6, :] = -1  # pawns
    board[7, 2] = board[7, 5] = -2  # bishops
    board[7, 1] = board[7, 6] = -3  # knights
    board[7, 0] = board[7, 7] = -4  # rooks
    board[7, 3] = -5  # queen
    board[7, 4] = -6  # king

    return board

###########################################
# Chess little rook preset
###########################################
def chess_preset_white_rook():
    """
    Creates a chess board with only two rooks, one for each color.
    """
    # Initialize an empty chess board
    board = np.zeros((8, 8), dtype=np.int8)

    board[0, 0] = board[0, 7] = 4   # White rook
    # board[0, 3] = 2  # White bishop
    board[0, 4] = 6   # king
    board[1, 3:6] = 1   # White pawns

    return board

def chess_preset_promotion():
    """
    Creates a chess board with a white pawn ready to be promoted.
    """
    # Initialize an empty chess board
    board = np.zeros((8, 8), dtype=np.int8)

    board[6, 4] = 1   # White pawn
    board[0, 0] = -4   # White rooks
    board[0, 4] = 6   # White king
    board[0, 3] = 5   # White queen
    board[7, 2] = -6

    return board

def chess_preset_promotion_mat():
    """
    Creates a chess board with a white pawn ready to be promoted.
    """
    # Initialize an empty chess board
    board = np.zeros((8, 8), dtype=np.int8)

    board[6, 1] = 1   # White pawn
    board[6, 2] = 4   # White rooks
    board[0, 4] = 6   # White king

    board[7, 5] = -6  # Black king

    return board

def chess_preset_draw():
    board = np.zeros((8, 8), dtype=np.int8)

    board[6, 2] = board[6, 4] = board[4, 7] = 4   # White rooks
    board[0, 4] = 6   # White king

    board[5, 3] = -6  # Black king

    return board
