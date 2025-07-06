from app.movements.piece_movements import get_pawn_movement, get_knight_movement, get_bishop_movement, get_rook_movement, get_queen_movement, get_king_movement
from app.chess.ChessTool import is_not_dangerous_for_king, get_valid_moves
import numpy as np

def warm_up_jit(
        warmup_movement: bool = True):
    # WARMUP Numba JIT compilation

    if warmup_movement:
        get_pawn_movement(np.zeros((8, 8), dtype=np.int8), 0, 0, True)
        get_knight_movement(np.zeros((8, 8), dtype=np.int8), 0, 0)
        get_bishop_movement(np.zeros((8, 8), dtype=np.int8), 0, 0)
        get_rook_movement(np.zeros((8, 8), dtype=np.int8), 0, 0)
        get_queen_movement(np.zeros((8, 8), dtype=np.int8), 0, 0)
        get_king_movement(np.zeros((8, 8), dtype=np.int8), 0, 0)

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
