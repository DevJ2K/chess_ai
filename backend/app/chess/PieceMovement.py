import numpy as np
from numba import njit

class PieceMovement:
    def __init__(self):
        # WARMUP Numba JIT compilation
        PieceMovement.get_pawn_movement(np.zeros((8, 8), dtype=np.int8), 0, 0, True)
        pass

    @staticmethod
    @njit
    def get_pawn_movement(board: np.ndarray, x: int, y: int, is_white_turn: bool):

        NUMBER_OF_POSSIBLE_MOVES = 4
        all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
        iteration = 0

        def add_move(new_x: int, new_y: int):
            nonlocal iteration
            if is_in_board(board, new_x, new_y):
                all_moves[iteration] = (new_x, new_y)
                iteration += 1

        if is_white_turn:
            if board[y + 1, x] == 0:
                add_move(x, y + 1)

            if y == 1\
            and board[y + 1, x] == 0\
            and board[y + 2, x] == 0:
                add_move(x, y + 2)

            if board[y + 1, x + 1] < 0:
                add_move(x + 1, y + 1)

            if board[y + 1, x - 1] < 0:
                add_move(x - 1, y + 1)

        else:
            if board[y - 1, x] == 0:
                add_move(x, y - 1)

            if y == 6\
            and board[y - 1, x] == 0\
            and board[y - 2, x] == 0:
                add_move(x, y - 2)

            if board[y - 1, x + 1] > 0:
                add_move(x + 1, y - 1)

            if board[y - 1, x - 1] > 0:
                add_move(x - 1, y - 1)

        return all_moves[:iteration]

@njit
def is_in_board(board: np.ndarray, x: int, y: int):
    return 0 <= x < board.shape[1] and 0 <= y < board.shape[0]

if __name__ == "__main__":
    import time
    from app.chess.Chess import Chess
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
    board[2, 1] = -1  # pawns
    board[7, 2] = board[7, 5] = -2  # bishops
    board[7, 1] = board[7, 6] = -3  # knights
    board[7, 0] = board[7, 7] = -4  # rooks
    board[7, 3] = -5  # queen
    board[7, 4] = -6  # king

    # print(board)

    chess = Chess(board)
    print(chess)

    piece_movement = PieceMovement()

    start_time = time.time()
    for i in range(1000):
        moves = piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")

    # for move in moves:
    #     board_copy = board.copy()
    #     x, y = move
    #     board_copy[y, x] = 1
    #     board_copy[1, 0] = 0
    #     print(f"Move from (0, 1) to {move}:")
    #     print(Chess(board_copy))

