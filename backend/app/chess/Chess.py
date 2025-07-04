import numpy as np


class Chess:
    def __init__(self):
        self.board: np.ndarray = self.__initialize_board__()
        self.current_turn: int = 1  # 1 for white, -1 for black
        self.move_history: list[str] = []

    def __initialize_board__(self) -> np.ndarray:
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

        print(board, board.shape)

    def __str__(self):
        pass

    def apply_move(self, move: str):
        pass


if __name__ == "__main__":
    chess_game = Chess()
    # example_move = "e4"
    # chess_game.apply_move(example_move)
    # print("Move applied:", example_move)
