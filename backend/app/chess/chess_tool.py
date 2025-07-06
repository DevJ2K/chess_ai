import numpy as np
from app.movements.piece_movements import get_pawn_movement, get_knight_movement, get_bishop_movement, get_rook_movement, get_queen_movement, get_king_movement
from app.movements.king_movement_utils import is_king_in_check
from numba import njit

# class ChessTool:

#     @staticmethod

@njit
def get_valid_moves(board: np.ndarray, nb_moves: int) -> np.ndarray:
    # Tableau pré-alloué : (x0, y0, x1, y1, piece_type)
    MAX_MOVES = 323

    all_moves = np.zeros((MAX_MOVES, 5), dtype=np.int8)
    move_count = 0

    is_white_turn = nb_moves % 2 == 0

    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            piece = board[y, x]
            if (is_white_turn and piece > 0) or (not is_white_turn and piece < 0):
                abs_piece = abs(piece)

                if abs_piece == 1:  # Pawn
                    moves = get_pawn_movement(board, x, y, is_white_turn)
                elif abs_piece == 2:  # Bishop
                    moves = get_bishop_movement(board, x, y)
                elif abs_piece == 3:  # Knight
                    moves = get_knight_movement(board, x, y)
                elif abs_piece == 4:  # Rook
                    moves = get_rook_movement(board, x, y)
                elif abs_piece == 5:  # Queen
                    moves = get_queen_movement(board, x, y)
                elif abs_piece == 6:  # King
                    moves = get_king_movement(board, x, y, False, False, False)
                else:
                    continue

                # Stocker tous les mouvements valides de cette pièce
                for i in range(moves.shape[0]):
                    dest_x, dest_y = moves[i]
                    if is_not_dangerous_for_king(board, np.array([x, y]), np.array([dest_x, dest_y]), is_white_turn):
                        all_moves[move_count, :5] = [x, y, dest_x, dest_y, abs_piece]
                        move_count += 1

                        if move_count >= MAX_MOVES:
                            break  # éviter overflow

    # Retourner uniquement la partie remplie
    return all_moves[:move_count]

# @njit
def _get_valid_moves(board: np.ndarray, move_history: list[str]) -> dict[str, tuple]:
    all_moves = []

    if len(move_history) % 2 == 0:  # White's turn
        for y in range(len(board)):
            for x in range(len(board[y])):
                if (board[y][x] > 0):
                    if False:
                        pass
                    if board[y][x] == 1:  # Pawn
                        all_moves.append([np.array([x, y], dtype=np.int8), get_pawn_movement(board, x, y, is_white_turn=True)])
                    elif board[y][x] == 2:  # Bishop
                        all_moves.append([np.array([x, y], dtype=np.int8), get_bishop_movement(board, x, y)])
                    elif board[y][x] == 3:  # Knight
                        all_moves.append([np.array([x, y], dtype=np.int8), get_knight_movement(board, x, y)])
                    elif board[y][x] == 4:  # Rook
                        all_moves.append([np.array([x, y], dtype=np.int8), get_rook_movement(board, x, y)])
                    elif board[y][x] == 5:  # Queen
                        all_moves.append([np.array([x, y], dtype=np.int8), get_queen_movement(board, x, y)])
                    elif board[y][x] == 6:  # King
                        all_moves.append([np.array([x, y], dtype=np.int8), get_king_movement(board, x, y, king_has_moved=False, rook_kingside_moved=False, rook_queenside_moved=False)])


        # # Remove duplicates and filter out moves that would put the king in check
        # moves = list(set(moves))

            # print()
        filtered_moves = []
        for initial_pos, moves in all_moves:
            for move in moves:
            # print(move)
                x, y = move
                # board[y, x] = 14  # Mark the move on the board for visualization
                if is_not_dangerous_for_king(board, initial_pos, move, is_white_turn=True):
                    # print(f"Valid move for white: {initial_pos} -> {move}")
                    filtered_moves.append((initial_pos, move))
                else:
                    # print(f"Invalid move for white: {initial_pos} -> {move}")
                    pass

        for initial_pos, move in filtered_moves:
            x, y = move
            board[y, x] = 14
        return filtered_moves
        # print(board)
    else:  # Black's turn
        pass

@njit
def is_not_dangerous_for_king(board: np.ndarray, initial_pos: np.ndarray, new_pos: np.ndarray, is_white_turn: bool) -> bool:
    # On doit appliquer le vecteur sur le board
    initial_x, initial_y = initial_pos
    new_x, new_y = new_pos

    initial_value = board[initial_y, initial_x]
    new_pos_value = board[new_y, new_x]
    board[initial_y, initial_x] = new_pos_value
    board[new_y, new_x] = initial_value

    king_value = 6 if is_white_turn else -6

    positions = np.where(board == king_value)
    if len(positions[0]) > 0:
        y, x = positions[0][0], positions[1][0]

        result = not is_king_in_check(board, x, y)

        board[initial_y, initial_x] = initial_value
        board[new_y, new_x] = new_pos_value

        return result
    return False
