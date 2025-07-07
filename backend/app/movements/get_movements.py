DISABLE_NUMBA_JIT = False  # Set to True to disable Numba JIT compilation for testing purposes

if DISABLE_NUMBA_JIT:
    import tests.configuration  # un-comment to ignore Numba JIT annotations

import numpy as np
from numba import njit
from app.movements.king_movement_utils import is_king_in_check
from app.movements.piece_movements import get_pawn_movement, get_knight_movement, get_bishop_movement, get_rook_movement, get_queen_movement, get_king_movement

@njit
def get_valid_moves(board: np.ndarray, nb_moves: int) -> np.ndarray:
    # Tableau pré-alloué : (x0, y0, x1, y1, piece_type)
    MAX_MOVES = 323

    all_moves = np.zeros((MAX_MOVES, 5), dtype=np.int8)
    move_count = 0

    is_white_turn = nb_moves % 2 == 0

    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            piece = board[y, x]
            if (is_white_turn and piece > 0) or (not is_white_turn and piece < 0):
                abs_piece = abs(piece)

                if abs_piece == 1:  # Pawn
                    moves = get_pawn_movement(board, x, y, is_white_turn)
                elif abs_piece == 2:  # Bishop
                    moves = get_bishop_movement(board, x, y)
                elif abs_piece == 3:  # Knight
                    moves = get_knight_movement(board, x, y)
                elif abs_piece == 4:  # Rook
                    moves = get_rook_movement(board, x, y)
                elif abs_piece == 5:  # Queen
                    moves = get_queen_movement(board, x, y)
                elif abs_piece == 6:  # King
                    moves = get_king_movement(board, x, y, False, False, False)
                else:
                    continue

                # Stocker tous les mouvements valides de cette pièce
                for i in range(moves.shape[0]):
                    dest_x, dest_y = moves[i]
                    if is_not_dangerous_for_king(board, np.array([x, y]), np.array([dest_x, dest_y]), is_white_turn):
                        all_moves[move_count, :5] = [x, y, dest_x, dest_y, abs_piece]
                        move_count += 1

                        if move_count >= MAX_MOVES:
                            break  # éviter overflow

    # Retourner uniquement la partie remplie
    return all_moves[:move_count]

@njit
def is_not_dangerous_for_king(board: np.ndarray, initial_pos: np.ndarray, new_pos: np.ndarray, is_white_turn: bool) -> bool:
    # On doit appliquer le vecteur sur le board
    initial_x, initial_y = initial_pos
    new_x, new_y = new_pos

    initial_value = board[initial_y, initial_x]
    new_pos_value = board[new_y, new_x]
    board[initial_y, initial_x] = new_pos_value
    board[new_y, new_x] = initial_value

    king_value = 6 if is_white_turn else -6

    positions = np.where(board == king_value)
    if len(positions[0]) > 0:
        y, x = positions[0][0], positions[1][0]

        result = not is_king_in_check(board, x, y)

        board[initial_y, initial_x] = initial_value
        board[new_y, new_x] = new_pos_value

        return result
    return False


if __name__ == "__main__":
    from benchmark.MeasureTime import MeasureTime
    from app.chess.Chess import Chess

    if not DISABLE_NUMBA_JIT:
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