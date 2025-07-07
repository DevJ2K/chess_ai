import numpy as np
# import tests.configuration  # un-comment to ignore Numba JIT annotations
from app.movements.get_movements import get_valid_moves
from app.utils.Colors import REDHB, WHITEHB, RESET

class Chess:

    PIECES = {
            0: '·', 14: REDHB + '?' + RESET, 15: ' ',
            -1: '♙', 1: '♟',
            -2: '♗', 2: '♝',
            -3: '♘', 3: '♞',
            -4: '♖', 4: '♜',
            -5: '♕', 5: '♛',
            -6: '♔', 6: '♚'
    }

    def __init__(self, board: np.ndarray = None):
        if board is not None:
            self.board: np.ndarray = board
        else:
            self.board: np.ndarray = Chess.initialize_board()
        self.move_history: np.ndarray = np.empty((0, 2, 3), dtype=np.int8)
        # self.move_history = np.append(self.move_history, np.array([[[0, 0, 0], [0, 0, 0]]], dtype=np.int8), axis=0)

    @staticmethod
    def initialize_board() -> np.ndarray:
        board = np.zeros((8, 8), dtype=np.int8)

        # White pieces
        # board[1, :] = 1   # pawns
        board[0, 2] = board[0, 5] = 2   # bishops
        board[0, 1] = board[0, 6] = 3   # knights
        board[0, 0] = board[0, 7] = 4   # rooks
        board[0, 3] = 5   # queen
        # board[0, 4] = 6   # king
        board[1, 3] = 6   # king

        # Black pieces
        # board[6, :] = -1  # pawns
        board[7, 2] = board[7, 5] = -2  # bishops
        board[7, 1] = board[7, 6] = -3  # knights
        board[7, 0] = board[7, 7] = -4  # rooks
        board[7, 3] = -5  # queen
        board[7, 4] = -6  # king

        # print(board, board.shape)
        return board

    def __str__(self):
        return Chess.board_to_str(self.board)

    @staticmethod
    def board_to_str(board: np.ndarray) -> str:
        # if board.shape != (8, 8):
        #     print(f"Invalid board shape: {board.shape}. Expected (8, 8).")
        #     return

        string = "Chess Board:\n"
        for y in range(len(board)):
            string += f"{8 - y} | "
            for x in range(len(board[y])):
                piece = board[7 - y][x]
                string += Chess.PIECES[piece] + " "
            string += "\n"
        string += "  | - - - - - - - -\n"
        string += "    a b c d e f g h\n"
        return string

    @staticmethod
    def display_move(move: np.ndarray, display_schema: bool = False):
        if move.shape != (2, 3):
            print(f"Invalid move shape: {move.shape}. Expected (2, 3).")
            return
        start_x, start_y, piece = move[0]
        dest_x, dest_y, captured_piece = move[1]

        print(f"Move piece {Chess.PIECES[piece]} from ({start_x}, {start_y}) to ({dest_x}, {dest_y})")
        if display_schema:
            board = np.full((8, 8), 15, dtype=np.int8)
            board[start_y, start_x] = piece
            board[dest_y, dest_x] = captured_piece
            print(Chess.board_to_str(board))


    def apply_move(self, move: str):
        pass

    def get_valid_moves(self) -> list[str]:
        moves = get_valid_moves(self.board, np.array(self.move_history, dtype=np.int8))
        # for move in moves:
        #     if move[0][2] == -5:
        #         Chess.display_move(move, display_schema=True)

if __name__ == "__main__":
    chess_game = Chess()
    from benchmark.MeasureTime import MeasureTime
    from app.optimization.jit_configuration import warm_up_jit

    # measureTime = MeasureTime(start=True)
    # np.array([[[0, 0, 0], [0, 0, 0]]], dtype=np.int8)
    # measureTime.stop()
    # exit(0)
    warm_up_jit()


    print(chess_game)
    measureTime = MeasureTime(start=True)
    chess_game.get_valid_moves()
    measureTime.stop()
    print(chess_game)

    # example_move = "e4"
    # chess_game.apply_move(example_move)
    # print("Move applied:", example_move)
