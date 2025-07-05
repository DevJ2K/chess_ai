import numba

def fake_njit(*args, **kwargs):
    def decorator(func):
        return func
    if len(args) == 1 and callable(args[0]):
        return args[0]
    return decorator

# Patch numba.njit to avoid JIT compilation in tests
numba.njit = fake_njit
