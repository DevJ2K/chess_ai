import numpy as np
from numba import njit
import time

# @njit
def initialize_board() -> np.ndarray:
    board = np.zeros((8, 8), dtype=np.int8)
    board[1, :] = 1   # white pawns
    board[6, :] = -1  # black pawns

start_time = time.time()
initialized_board = initialize_board()
end_time = time.time()
print(f"Board initialized in {end_time - start_time:.6f} seconds")