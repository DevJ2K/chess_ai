import os
import time
from numba import jit

# 🔒 Désactiver multi-thread pour Numba/LLVM/BLAS
os.environ["NUMBA_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["VECLIB_MAXIMUM_THREADS"] = "1"  # Pour macOS
os.environ["NUMEXPR_NUM_THREADS"] = "1"

# 🔥 Compilation sans parallélisme
@jit(nopython=True, parallel=False, fastmath=False, cache=False)
def loop(n: int):
    count = 0
    for i in range(n):
        count += 1
    return count


# 🌡️ Warm-up phase (JIT compilation)
start_time = time.time()
loop(1)  # Petit appel pour compiler la fonction
warmup_duration = time.time() - start_time
print(f"Warm-up (JIT compilation) duration: {warmup_duration:.6f} seconds")

# 🏁 Mesure de l'exécution réelle
start_time = time.time()
result = loop(1_000_000_000)
execution_duration = time.time() - start_time
print(f"Execution result: {result}")
print(f"Execution time: {execution_duration:.6f} seconds")
