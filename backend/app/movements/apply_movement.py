import numpy as np

def apply_move(board: np.ndarray, move: np.ndarray, promotion: np.int8) -> bool:
    if move.shape != (2, 3):
        print(f"Invalid move shape: {move.shape}. Expected (2, 3).")
        return False

    start_x, start_y, piece = move[0]
    dest_x, dest_y, captured_piece = move[1]

    #################################
    # Handle castling
    #################################
    if piece == 6 and (start_x, start_y) == (4, 0) and (dest_x, dest_y) == (6, 0):
        print("White Castling queenside detected!")
        board[0, 7] = 0
        board[0, 5] = 4
    elif piece == 6 and (start_x, start_y) == (4, 0) and (dest_x, dest_y) == (2, 0):
        print("White Castling kingside detected!")
        board[0, 0] = 0
        board[0, 3] = 4
    elif piece == -6 and (start_x, start_y) == (4, 7) and (dest_x, dest_y) == (6, 7):
        print("Black Castling queenside detected!")
        board[7, 7] = 0
        board[7, 5] = -4
    elif piece == -6 and (start_x, start_y) == (4, 7) and (dest_x, dest_y) == (2, 7):
        print("Black Castling kingside detected!")
        board[7, 0] = 0
        board[7, 3] = -4

    #################################
    # Handle promotions
    #################################
    if abs(piece) == 1:  # Pawn
        if (piece > 0 and dest_y == 7) or (piece < 0 and dest_y == 0):
            if promotion not in [2, 3, 4, 5]:  # Invalid promotion
                print("Invalid promotion piece.")
                return False
            board[start_y, start_x] = 0
            board[dest_y, dest_x] = piece * promotion
            print(f"Pawn promoted to {promotion} at ({dest_x}, {dest_y})")
            return True

    board[start_y, start_x] = 0
    board[dest_y, dest_x] = piece
    return True
