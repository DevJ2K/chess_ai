import numba
from app.movements.piece_moves import get_pawn_moves
from app.optimization.jit_configuration import warm_up_jit
from app.chess.Chess import Chess
from benchmark.MeasureTime import MeasureTime


print("Numba JIT : [ON]")

board = Chess.initialize_board()
warm_up_jit()

measureTime = MeasureTime(start=True)
get_pawn_moves(board, x=0, y=1, is_white_turn=True)
measureTime.stop()


print("Numba JIT : [OFF]")

def fake_njit(*args, **kwargs):
    def decorator(func):
        return func
    if len(args) == 1 and callable(args[0]):
        return args[0]
    return decorator

numba.njit = fake_njit

board = Chess.initialize_board()

measureTime = MeasureTime(start=True)
get_pawn_moves(board, x=0, y=1, is_white_turn=True)
measureTime.stop()
