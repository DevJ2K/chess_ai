from app.utils.Colors import BHMAG, BHGREEN, RESET
from time import time
import numpy as np


def warm_up_jit():
    # WARMUP Numba JIT compilation
    print(BHMAG + "Warming up Numba JIT compilation..." + RESET)
    start_time = time()

    # ====================================================
    from app.movements.piece_moves import (
        get_pawn_moves, get_knight_moves, get_bishop_moves,
        get_rook_moves, get_queen_moves, get_king_moves)

    get_pawn_moves(np.zeros((8, 8), dtype=np.int8), 0, 0, True)
    get_knight_moves(np.zeros((8, 8), dtype=np.int8), 0, 0)
    get_bishop_moves(np.zeros((8, 8), dtype=np.int8), 0, 0)
    get_rook_moves(np.zeros((8, 8), dtype=np.int8), 0, 0)
    get_queen_moves(np.zeros((8, 8), dtype=np.int8), 0, 0)
    get_king_moves(np.zeros((8, 8), dtype=np.int8), 0, 0, False, False, False)
    # ====================================================
    #
    # ====================================================
    from app.movements.get_moves import is_not_dangerous_for_king, get_valid_moves, is_move_startswith

    get_valid_moves(
        np.zeros((8, 8), dtype=np.int8),
        np.empty((0, 2, 3), dtype=np.int8),
    )
    is_not_dangerous_for_king(
        np.zeros((8, 8), dtype=np.int8),
        np.array([0, 0], dtype=np.int8),
        np.array([0, 0], dtype=np.int8),
        is_white_turn=True
    )
    is_move_startswith(
        np.empty((0, 2, 3), dtype=np.int8),
        np.array([[0, 0, 0], [0, 0, 0]], dtype=np.int8)
    )
    # ====================================================
    #
    # ====================================================
    from app.movements.king_movement_utils import is_square_under_attack, can_castle_kingside, can_castle_queenside

    is_square_under_attack(np.zeros((8, 8), dtype=np.int8), 0, 0, is_white_piece=True)
    can_castle_kingside(np.zeros((8, 8), dtype=np.int8), 0, 0, False)
    can_castle_queenside(np.zeros((8, 8), dtype=np.int8), 0, 0, False)
    # ====================================================
    #
    # ====================================================
    from app.movements.piece_utils import is_in_board

    is_in_board(np.zeros((8, 8), dtype=np.int8), 0, 0)
    # ====================================================
    #
    # ====================================================
    from app.state.king import is_king_in_check
    is_king_in_check(np.zeros((8, 8), dtype=np.int8), 0, 0)
    # ====================================================
    #
    # ====================================================
    from app.state.moves import has_available_moves
    has_available_moves(np.zeros((8, 8), dtype=np.int8), np.empty((0, 2, 3), dtype=np.int8))

    end_time = time()
    print(BHGREEN + f"Numba JIT compilation warmed up in {end_time - start_time:.3f} seconds." + RESET)
