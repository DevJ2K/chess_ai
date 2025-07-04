from numba import njit, prange
import numpy as np
import time

@njit(parallel=True)
def loop(n: int):
    tmp = np.empty(n, dtype=np.int64)
    for i in prange(n):
        tmp[i] = i
    return tmp


loop(1) # WARM UP

start_time = time.time()
# loop(1_000_000_000)
loop(10_000_000)
print(f"Execution time: {time.time() - start_time} seconds")