from numba import njit
import numpy as np
from app.state.king import is_king_in_check
from app.state.moves import has_available_moves

@njit
def is_terminate_state(board: np.ndarray, move_history: np.ndarray) -> bool:
    """
    Checks if the game is in a terminal state (checkmate or stalemate).
    
    Args:
        board (np.ndarray): The current state of the chess board.
        move_history (np.ndarray): The history of moves made in the game.
        
    Returns:
        bool: True if the game is in a terminal state, False otherwise.
    """
    # Check for checkmate
            
    # king_value = 6 if len(move_history) % 2 == 0 else -6
    # positions = np.where(board == king_value)
    # if len(positions[0]) > 0:
    #     y, x = positions[0][0], positions[1][0]
    #     state = np.array([
    #         is_king_in_check(board, x, y),
    #         has_available_moves(board, move_history)
    #     ], dtype=np.int8)
    return has_available_moves(board, move_history)

    return True