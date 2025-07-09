import numpy as np
from numba import njit
from app.movements.piece_utils import is_in_board
from app.movements.king_movement_utils import can_castle_kingside, can_castle_queenside, is_king_in_check


@njit
def get_pawn_moves(board: np.ndarray, x: int, y: int, is_white_turn: bool):

    NUMBER_OF_POSSIBLE_MOVES = 4
    all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
    iteration = 0

    def add_move(new_x: int, new_y: int):
        nonlocal iteration
        all_moves[iteration] = (new_x, new_y)
        iteration += 1

    if is_white_turn:
        if is_in_board(board, x, y + 1) and board[y + 1, x] == 0:
            add_move(x, y + 1)

        if y == 1 \
            and is_in_board(board, x, y + 1) and board[y + 1, x] == 0 \
                and is_in_board(board, x, y + 2) and board[y + 2, x] == 0:
            add_move(x, y + 2)

        if is_in_board(board, x + 1, y + 1) and board[y + 1, x + 1] < 0:
            add_move(x + 1, y + 1)

        if is_in_board(board, x - 1, y + 1) and board[y + 1, x - 1] < 0:
            add_move(x - 1, y + 1)

    else:
        if is_in_board(board, x, y - 1) and board[y - 1, x] == 0:
            add_move(x, y - 1)

        if y == 6 \
            and is_in_board(board, x, y - 1) and board[y - 1, x] == 0 \
                and is_in_board(board, x, y - 2) and board[y - 2, x] == 0:
            add_move(x, y - 2)

        if is_in_board(board, x + 1, y - 1) and board[y - 1, x + 1] > 0:
            add_move(x + 1, y - 1)

        if is_in_board(board, x - 1, y - 1) and board[y - 1, x - 1] > 0:
            add_move(x - 1, y - 1)

    return all_moves[:iteration]


@njit
def get_bishop_moves(board: np.ndarray, x: int, y: int):
    NUMBER_OF_POSSIBLE_MOVES = 13
    all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
    iteration = 0

    directions = np.array([
        (1, 1), (1, -1), (-1, -1), (-1, 1)
    ], dtype=np.int8)

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        while is_in_board(board, new_x, new_y):
            if board[new_y, new_x] == 0:
                all_moves[iteration] = (new_x, new_y)
                iteration += 1
            elif board[new_y, new_x] * board[y, x] < 0:
                all_moves[iteration] = (new_x, new_y)
                iteration += 1
                break
            else:
                break
            new_x += dx
            new_y += dy

    return all_moves[:iteration]


@njit
def get_knight_moves(board: np.ndarray, x: int, y: int):
    NUMBER_OF_POSSIBLE_MOVES = 8
    all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
    iteration = 0

    knight_moves = np.array([
        (1, 2), (2, 1), (2, -1), (1, -2),
        (-1, -2), (-2, -1), (-2, 1), (-1, 2)
    ], dtype=np.int8)

    for dx, dy in knight_moves:
        new_x, new_y = x + dx, y + dy
        if is_in_board(board, new_x, new_y) and board[new_y, new_x] * board[y, x] <= 0:
            all_moves[iteration] = (new_x, new_y)
            iteration += 1

    return all_moves[:iteration]


@njit
def get_rook_moves(board: np.ndarray, x: int, y: int):
    NUMBER_OF_POSSIBLE_MOVES = 14
    all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
    iteration = 0

    directions = np.array([
        (1, 0), (0, 1), (-1, 0), (0, -1)
    ], dtype=np.int8)

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        while is_in_board(board, new_x, new_y):
            if board[new_y, new_x] == 0:
                all_moves[iteration] = (new_x, new_y)
                iteration += 1
            elif board[new_y, new_x] * board[y, x] < 0:
                all_moves[iteration] = (new_x, new_y)
                iteration += 1
                break
            else:
                break
            new_x += dx
            new_y += dy

    return all_moves[:iteration]


@njit
def get_queen_moves(board: np.ndarray, x: int, y: int):
    NUMBER_OF_POSSIBLE_MOVES = 27
    all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
    iteration = 0

    rook_moves = get_rook_moves(board, x, y)
    bishop_moves = get_bishop_moves(board, x, y)

    for move in rook_moves:
        all_moves[iteration] = move
        iteration += 1

    for move in bishop_moves:
        all_moves[iteration] = move
        iteration += 1

    return all_moves[:iteration]


@njit
def get_king_moves(board: np.ndarray, x: int, y: int, king_has_moved: bool = False,
                      rook_kingside_moved: bool = False, rook_queenside_moved: bool = False):

    NUMBER_OF_POSSIBLE_MOVES = 10
    all_moves = np.zeros((NUMBER_OF_POSSIBLE_MOVES, 2), dtype=np.int8)
    iteration = 0

    king_moves = np.array([
        (1, 0), (0, 1), (-1, 0), (0, -1),
        (1, 1), (1, -1), (-1, -1), (-1, 1)
    ], dtype=np.int8)

    for dx, dy in king_moves:
        new_x, new_y = x + dx, y + dy
        if is_in_board(board, new_x, new_y) and board[new_y, new_x] * board[y, x] <= 0:
            all_moves[iteration] = (new_x, new_y)
            iteration += 1

    if not king_has_moved and not is_king_in_check(board, x, y):

        if can_castle_kingside(board, x, y, rook_kingside_moved):
            all_moves[iteration] = (x + 2, y)
            iteration += 1

        if can_castle_queenside(board, x, y, rook_queenside_moved):
            all_moves[iteration] = (x - 2, y)
            iteration += 1

    return all_moves[:iteration]


if __name__ == "__main__":
    import time
    from app.chess.Chess import Chess
    from app.optimization.jit_configuration import warm_up_jit
    board = np.zeros((8, 8), dtype=np.int8)

    # # White pieces
    # board[1, :] = 1   # pawns
    # board[0, 2] = board[0, 5] = 2   # bishops
    # board[0, 1] = board[0, 6] = 3   # knights
    board[0, 0] = board[0, 7] = 4   # rooks
    # board[0, 3] = 5   # queen
    # board[0, 4] = 6   # king

    # # Black pieces
    # board[6, :] = -1  # pawns
    # board[2, 1] = -1  # pawns
    # board[7, 2] = board[7, 5] = -2  # bishops
    # board[7, 1] = board[7, 6] = -3  # knights
    # board[7, 0] = board[7, 7] = -4  # rooks
    # board[7, 3] = -5  # queen
    # board[7, 4] = -6  # king

    chess = Chess(board)

    warm_up_jit(warmup_movement=True)

    piece_x, piece_y = 4, 0
    board[piece_y, piece_x] = 6

    print(chess)

    start_time = time.time()
    # for i in range(1):
    # moves = get_pawn_moves(board, x=0, y=1, is_white_turn=True)
    # get_pawn_moves(board, x=piece_x, y=piece_y, is_white_turn=True)
    # get_knight_moves(board, x=piece_x, y=piece_y)
    # get_bishop_moves(board, x=piece_x, y=piece_y)
    # get_rook_moves(board, x=piece_x, y=piece_y)
    # get_queen_moves(board, x=piece_x, y=piece_y)
    moves = get_king_moves(board, x=piece_x, y=piece_y)
    # moves = get_king_moves(board, x=piece_x, y=piece_y)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.6f} seconds")

    # for move in moves:
    #     board_copy = board.copy()
    #     x, y = move
    #     board_copy[y, x] = board_copy[piece_y, piece_x]
    #     board_copy[piece_y, piece_x] = 0
    #     print(f"Move from ({piece_x}, {piece_y}) to {move}:")
    #     print(Chess(board_copy))

    for move in moves:
        x, y = move
        board[y, x] = 14
    print(chess)
