import numpy as np
import re
# import tests.configuration  # un-comment to ignore Numba JIT annotations
from app.movements.get_moves import get_valid_moves
from app.utils.Colors import REDHB, RESET
from app.chess.ChessPresets import ChessPresets
from app.movements.movement_representation import move_to_str
from app.movements.apply_move import apply_move
from app.state.king import is_king_in_check
from app.state.moves import has_available_moves


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
        self.move_history_str: list[str] = []

    @staticmethod
    def initialize_board() -> np.ndarray:
        return ChessPresets.default()

    def __str__(self):
        return Chess.board_to_str(self.board)

    @staticmethod
    def board_to_str(board: np.ndarray) -> str:
        if board.shape != (8, 8):
            return f"Invalid board shape: {board.shape}. Expected (8, 8)."

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

        print(f"Move piece {Chess.PIECES[piece]} from ({start_x}, {start_y}) to ({dest_x}, {dest_y}) |")
        if display_schema:
            board = np.full((8, 8), 15, dtype=np.int8)
            board[start_y, start_x] = piece
            board[dest_y, dest_x] = captured_piece
            print(Chess.board_to_str(board))

    def apply_move_str(self, move_representation: str) -> bool:
        moves = self.get_valid_moves()
        if move_representation not in moves:
            print(f"Invalid move: {move_representation}. Available moves: {list(moves.keys())}")
            return False

        promotion_str = re.search(r"=(\w)", move_representation)
        promotion = 5
        if promotion_str:
            promotion = {'Q': 5, 'R': 4, 'B': 3, 'N': 2}.get(promotion_str.group(1), 5)
        apply_move(self.board, moves[move_representation], promotion=promotion)

        self.move_history = np.append(self.move_history, np.expand_dims(moves[move_representation], axis=0), axis=0)
        self.move_history_str.append(move_representation)

        if move_representation.endswith('#'):
            print("Checkmate! Game over.")
            return True
        elif move_representation.endswith('='):
            print("Draw! No valid moves left for the opponent.")
            return True

    def get_valid_moves(self) -> dict[str, np.ndarray]:
        moves = get_valid_moves(self.board, np.array(self.move_history, dtype=np.int8))
        all_str_moves = []

        # Content: (king is in check(0-1), moves available(0-1))
        game_status_per_move = np.zeros((len(moves), 2), dtype=np.int8)

        for i, move in enumerate(moves):
            after_move_board = self.__simulate_move__(move)
            if after_move_board is None:
                continue

            king_value = 6 if (len(self.move_history) + 1) % 2 == 0 else -6

            positions = np.where(after_move_board == king_value)
            if len(positions[0]) > 0:
                y, x = positions[0][0], positions[1][0]

                game_status_per_move[i] = np.array([
                    is_king_in_check(after_move_board, x, y),
                    has_available_moves(after_move_board, np.append(self.move_history, np.expand_dims(move, axis=0), axis=0))
                ], dtype=np.int8)

                str_moves = move_to_str(after_move_board, move, game_status_per_move[i])
                for str_move in str_moves:
                    all_str_moves.append([str_move, move])

        counts = {}
        for row in all_str_moves:
            counts[row[0]] = counts.get(row[0], 0) + 1

        # Garder ceux qui apparaissent une seule fois en première colonne
        filter_moves = [row for row in all_str_moves if counts[row[0]] == 1]
        return {k: v for k, v in filter_moves}

    def __simulate_move__(self, move: np.ndarray) -> np.ndarray:
        """
        Simulates a move on the board without modifying the original board.
        Returns a new board state after the move.
        """
        if move.shape != (2, 3):
            print(f"Invalid move shape: {move.shape}. Expected (2, 3).")
            return None

        new_board = self.board.copy()
        apply_move(new_board, move, promotion=5)

        return new_board


if __name__ == "__main__":
    from benchmark.MeasureTime import MeasureTime
    from app.optimization.jit_configuration import warm_up_jit

    # measureTime = MeasureTime(start=True)
    # np.array([[[0, 0, 0], [0, 0, 0]]], dtype=np.int8)
    # measureTime.stop()
    # exit(0)
    measureTime = MeasureTime(start=True)
    warm_up_jit()
    warm_up_duration = measureTime.stop(get_str=True)

    print(f"Warm-up duration: {warm_up_duration}")
#     GAME = [
#     "c4", "e5",
#     "e4", "d6",
#     "Nf3", "Bg4",
#     "h3", "Bxf3",
#     "gxf3", "Nf6",
#     "Bd3", "Be7",
#     "O-O", "O-O",
#     "Nc3", "Nh5",
#     "a4", "a5",
#     "Rb1", "b6",
#     "b4", "axb4",
#     "Rxb4", "Nc6",
#     "Rb1", "Nd4",
#     "Ba3", "c6",
#     "Re1", "Qd7",
#     "f4", "Qxh3",
#     "Re3", "Qh4",
#     "Rxb6", "c5",
#     "Nb5", "Rxa4",
#     "Qxa4", "Nxf4",
#     "Qd1", "Qg5+",
#     "Kf1", "Qg2+",
#     "Ke1", "Qg1+",
#     "Bf1", "Ng2#"
# ]
    GAME = [
        "e4", "e5",
        "Nf3", "Nf6",
        "d3", "Nc6",
        "g3", "Bb4+",
        "c3", "Ba5",
        "b4", "Bb6",
        "Bh3", "g5",
        "Nxg5", "Qe7",
        "Ba3", "d5",
        "b5", "Bxh3",
        "Bxe7", "Kxe7",
        "Nxh3", "Rhg8",
        "O-O", "Ng4",
        "exd5", "Na5",
        "d4", "Rad8",
        "Re1", "Rg6",
        "dxe5", "c6",
        "Nf4", "Rh6",
        "d6+", "Kf8",
        "e6", "Rxh2",
        "Qxg4", "Bxf2+",
        "Kxh2", "Nc4",
        "e7+", "Ke8",
        "Rd1", "Ne5",
        "d7+", "Rxd7",
        "Qh3", "Rxd1",
        "Qc8+", "Kxe7",
        "Kh3", "Rh1+",
        "Kg2", "Ng4",
        "Kxh1", "Bxg3",
        "Qxg4", "Bf2",
        "Na3", "h5",
        "Qe2+", "Kf8",
        "Qxf2", "f6",
        "Nxh5", "f5",
        "Qxf5+", "Ke8",
        "bxc6", "Kd8",
        "cxb7", "Kc7",
        "Rb1", "a6",
        "b8=Q+", "Kc6",
        "Rb6#"
    ]

    import time
    import os
    chess_game = Chess()
    # print(chess_game)
    # input("Press Enter to start the game...")
    # iteration = 0
    # for move in GAME:
    #     chess_game.apply_move_str(move)
    #     print(chess_game)
    #     print(f"Tuple number: {iteration // 2}/{len(GAME) / 2}")
    #     iteration += 1
    #     # time.sleep(0.2)
    #     os.system('clear')
    # print(chess_game)
    # print(chess_game.move_history_str == GAME)

    # while True:
    #     os.system('clear')
    #     print(chess_game)
    #     user_input = input("Enter your move (or 'exit' to quit): ")
    #     if user_input.lower() in ['exit', 'quit', 'q']:
    #         break
    #     if chess_game.apply_move_str(user_input):
    #         break
    # print(chess_game)
    print(chess_game.move_history_str)

    print(chess_game)
    measureTime = MeasureTime(start=True)
    for _ in range(1):
        chess_game.get_valid_moves()
    measureTime.stop()
    print(chess_game)

    # example_move = "e4"
    # chess_game.apply_move(example_move)
    # print("Move applied:", example_move)
