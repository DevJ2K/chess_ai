import numpy as np
from app.movements.apply_movement import apply_move

PIECE = {
    0: '',
    1: '',
    2: 'B',
    3: 'N',
    4: 'R',
    5: 'Q',
    6: 'K',
}


def move_to_str(board: np.ndarray, move: np.ndarray, opponent_king_status: np.ndarray) -> list[str]:
    if move.shape != (2, 3):
        print(f"Invalid move shape: {move.shape}. Expected (2, 3).")
        return ""
    start_x, start_y, piece = move[0]
    abs_piece = abs(piece)
    dest_x, dest_y, dest_piece = move[1]

    if piece == 6 and (start_x, start_y) == (4, 0) and (dest_x, dest_y) == (6, 0):
        return ["O-O"]
    elif piece == 6 and (start_x, start_y) == (4, 0) and (dest_x, dest_y) == (2, 0):
        return ["O-O-O"]
    elif piece == -6 and (start_x, start_y) == (4, 7) and (dest_x, dest_y) == (6, 7):
        return ["O-O"]
    elif piece == -6 and (start_x, start_y) == (4, 7) and (dest_x, dest_y) == (2, 7):
        return ["O-O-O"]

    start_col = chr(ord('a') + start_x)
    start_row = str(start_y + 1)

    dest_col = chr(ord('a') + dest_x)
    dest_row = str(dest_y + 1)

    if dest_col == "d" and dest_row == "6":
        print("DEBUG: Move to d6 detected")
        apply_move(board, move, 0)  # Apply the move without promotion
        from app.chess.Chess import Chess
        print(Chess.board_to_str(board))
        print(opponent_king_status)

    # GAME STATE
    is_capture = dest_piece != 0 and piece * dest_piece < 0

    REPR_PIECE = "" if abs_piece == 1 else PIECE[abs_piece]

    START_POS = ["", start_col, start_row]

    CAPTURED = "x" if is_capture else ""

    DEST = f"{dest_col}{dest_row}"

    PROMOTION = [""]
    if abs_piece == 1 and (dest_y == 7 or dest_y == 0):  # Pawn
        PROMOTION = ["=Q", "=R", "=B", "=N"]
    END_GAME = ""

    if opponent_king_status[0]:  # If the opponent's king is in check
        if opponent_king_status[1]:  # If the opponent has valid moves
            END_GAME += '+'
        else:  # If the opponent has no valid moves
            END_GAME += '#'
    else:
        if opponent_king_status[1] == 0:
            END_GAME += '='

    return [f"{REPR_PIECE}{start_pos}{CAPTURED}{DEST}{promotion}{END_GAME}"
            for start_pos in START_POS
            for promotion in PROMOTION
            ]
