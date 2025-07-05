import numpy as np
from app.chess.ChessTool import ChessTool

class Chess:
    def __init__(self, board: np.ndarray = None):
        if board is not None:
            self.board: np.ndarray = board
        else:
            self.board: np.ndarray = Chess.initialize_board()
        self.move_history: list[str] = []

    @staticmethod
    def initialize_board() -> np.ndarray:
        board = np.zeros((8, 8), dtype=np.int8)

        # White pieces
        board[1, :] = 1   # pawns
        board[0, 2] = board[0, 5] = 2   # bishops
        board[0, 1] = board[0, 6] = 3   # knights
        board[0, 0] = board[0, 7] = 4   # rooks
        board[0, 3] = 5   # queen
        board[0, 4] = 6   # king

        # Black pieces
        board[6, :] = -1  # pawns
        board[7, 2] = board[7, 5] = -2  # bishops
        board[7, 1] = board[7, 6] = -3  # knights
        board[7, 0] = board[7, 7] = -4  # rooks
        board[7, 3] = -5  # queen
        board[7, 4] = -6  # king

        # print(board, board.shape)
        return board

    def __str__(self):
        string = "Chess Board:\n"
        pieces = {
            -1: '♙', 1: '♟',
            -2: '♗', 2: '♝',
            -3: '♘', 3: '♞',
            -4: '♖', 4: '♜',
            -5: '♕', 5: '♛',
            -6: '♔', 6: '♚'
        }

        for y in range(len(self.board)):
            string += f"{8 - y} | "
            for x in range(len(self.board[y])):
                piece = self.board[7 - y][x]
                if piece != 0:
                    string += pieces[piece] + " "
                else:
                    string += "· "
            string += "\n"
        string += "  | - - - - - - - -\n"
        string += "    a b c d e f g h\n"
        return string

    def apply_move(self, move: str):
        pass

    def get_valid_moves(self) -> list[str]:
        ChessTool.get_valid_moves(self.board, self.move_history)
        # if len(self.move_history) % 2 == 0:  # White's turn
        #     pass
        # else:  # Black's turn
        #     pass
        # # for line in self.board
        # return []


if __name__ == "__main__":
    chess_game = Chess()
    print(chess_game)
    # chess_game.get_valid_moves()

    # example_move = "e4"
    # chess_game.apply_move(example_move)
    # print("Move applied:", example_move)
