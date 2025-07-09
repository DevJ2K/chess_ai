import numpy as np
from numba import njit
from app.state.king import is_king_in_check
from app.movements.piece_moves import get_pawn_moves, get_knight_moves, get_bishop_moves, get_rook_moves, get_queen_moves, get_king_moves


@njit
def get_valid_moves(board: np.ndarray, move_history: np.ndarray) -> np.ndarray:
    # Moves: [[[x1, y1], [x2, y2], [v1, v2]]]
    # Moves: [[[x1, y1, value1], [x2, y2, value2]], ...]

    MAX_MOVES = 323
    possible_moves = np.zeros((MAX_MOVES, 2, 3), dtype=np.int8)
    iteration = 0

    is_white_turn = len(move_history) % 2 == 0
    if is_white_turn:
        y_indexes, x_indexes = np.where(board > 0)
    else:
        y_indexes, x_indexes = np.where(board < 0)

    for x, y in zip(x_indexes, y_indexes):
        piece = board[y, x]
        abs_piece = abs(piece)

        if abs_piece == 1:
            moves = get_pawn_moves(board, x, y, is_white_turn)
        elif abs_piece == 2:
            moves = get_bishop_moves(board, x, y)
        elif abs_piece == 3:
            moves = get_knight_moves(board, x, y)
        elif abs_piece == 4:
            moves = get_rook_moves(board, x, y)
        elif abs_piece == 5:
            moves = get_queen_moves(board, x, y)
        elif abs_piece == 6:

            if piece > 0:  # White
                default_queenside_rook = np.array([0, 0, 4], dtype=np.int8)
                default_kingside_rook = np.array([7, 0, 4], dtype=np.int8)
                default_king_position = np.array([4, 0, 6], dtype=np.int8)
            else:  # Black
                default_queenside_rook = np.array([0, 7, -4], dtype=np.int8)
                default_kingside_rook = np.array([7, 7, -4], dtype=np.int8)
                default_king_position = np.array([4, 7, -6], dtype=np.int8)

            moves = get_king_moves(
                board, x, y,
                king_has_moved=is_move_startswith(move_history, default_king_position),
                rook_kingside_moved=is_move_startswith(move_history, default_kingside_rook),
                rook_queenside_moved=is_move_startswith(move_history, default_queenside_rook)
            )
        else:
            continue

        for move in moves:

            dest_x, dest_y = move

            if is_not_dangerous_for_king(board, np.array([x, y]), np.array([dest_x, dest_y]), is_white_turn):
                possible_moves[iteration, 0] = [x, y, piece]
                possible_moves[iteration, 1] = [dest_x, dest_y, board[dest_y, dest_x]]
                iteration += 1

                if iteration >= MAX_MOVES:
                    break

    return possible_moves[:iteration]


@njit
def is_move_startswith(data: np.ndarray, initial_move: np.ndarray) -> bool:
    for i in range(data.shape[0]):
        row_match = True
        for j in range(initial_move.shape[0]):
            if data[i, 0, j] != initial_move[j]:
                row_match = False
                break
        if row_match:
            return True
    return False


@njit
def is_not_dangerous_for_king(board: np.ndarray, initial_pos: np.ndarray, new_pos: np.ndarray, is_white_turn: bool) -> bool:
    initial_x, initial_y = initial_pos
    new_x, new_y = new_pos

    initial_value = board[initial_y, initial_x]
    new_pos_value = board[new_y, new_x]
    board[initial_y, initial_x] = 0
    board[new_y, new_x] = initial_value

    king_value = 6 if is_white_turn else -6

    positions = np.where(board == king_value)
    if len(positions[0]) > 0:
        y, x = positions[0][0], positions[1][0]

        result = not is_king_in_check(board, x, y)

        board[initial_y, initial_x] = initial_value
        board[new_y, new_x] = new_pos_value

        return result
    else:
        board[initial_y, initial_x] = initial_value
        board[new_y, new_x] = new_pos_value
    return False


if __name__ == "__main__":
    from benchmark.MeasureTime import MeasureTime
    from app.chess.Chess import Chess

    DISABLE_JIT_WARMUP = True
    if not DISABLE_JIT_WARMUP:
        from app.optimization.jit_configuration import warm_up_jit
        warm_up_jit()
        get_valid_moves(
            np.zeros((8, 8), dtype=np.int8),
            0
        )
        is_not_dangerous_for_king(
            np.zeros((8, 8), dtype=np.int8),
            np.array([0, 0], dtype=np.int8),
            np.array([0, 0], dtype=np.int8),
            is_white_turn=True
        )

    chess = Chess.initialize_board()
    measureTime = MeasureTime(start=True)
    valid_moves = get_valid_moves(chess, 0)
    measureTime.stop()
