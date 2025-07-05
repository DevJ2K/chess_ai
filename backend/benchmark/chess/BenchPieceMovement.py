import numba
from app.chess.PieceMovement import PieceMovement
from app.chess.Chess import Chess
from benchmark.MeasureTime import MeasureTime


print("Numba JIT : [ON]")

board = Chess.initialize_board()
piece_movement = PieceMovement()

measureTime = MeasureTime(start=True)
piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True)
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
piece_movement = PieceMovement()

measureTime = MeasureTime(start=True)
piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True)
measureTime.stop()
