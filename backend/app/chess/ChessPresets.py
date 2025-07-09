import numpy as np


class ChessPresets:
    """
    A collection of chess board presets for testing and demonstration purposes.
    Each preset returns a numpy array representing the chess board state.
    """
    @staticmethod
    def default() -> np.ndarray:
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

    @staticmethod
    def white_rook() -> np.ndarray:
        board = np.zeros((8, 8), dtype=np.int8)

        board[0, 0] = board[0, 7] = 4   # White rook
        # board[0, 3] = 2  # White bishop
        board[0, 4] = 6   # king
        board[1, 3:6] = 1   # White pawns

        return board

    @staticmethod
    def promotion() -> np.ndarray:
        board = np.zeros((8, 8), dtype=np.int8)

        board[6, 4] = 1   # White pawn
        board[0, 0] = -4   # White rooks
        board[0, 4] = 6   # White king
        board[0, 3] = 5   # White queen
        board[7, 2] = -6

        return board

    @staticmethod
    def promotion_mat() -> np.ndarray:
        board = np.zeros((8, 8), dtype=np.int8)

        board[6, 1] = 1   # White pawn
        board[6, 2] = 4   # White rooks
        board[0, 4] = 6   # White king

        board[7, 5] = -6  # Black king

        return board

    @staticmethod
    def draw() -> np.ndarray:
        board = np.zeros((8, 8), dtype=np.int8)

        board[6, 2] = board[6, 4] = board[4, 7] = 4   # White rooks
        board[0, 4] = 6   # White king

        board[5, 3] = -6  # Black king

        return board
