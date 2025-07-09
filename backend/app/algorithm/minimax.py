import numpy as np

import tests.configuration

from numba import njit
from app.state.moves import has_available_moves
from app.state.evaluate import evaluate_board
from app.movements.get_moves import get_valid_moves
from app.movements.apply_move import apply_move
from app.movements.MoveResult import MoveResult

@njit
def minimax(
    board: np.ndarray,
    move_history: np.ndarray,
    moves: np.ndarray = np.empty((0, 2, 3), dtype=np.int8),
    alpha: float = -np.inf,
    beta: float = np.inf,
    depth: int = 0,
    max_depth: int = 1
    ) -> np.ndarray:
    """
    Minimax algorithm to evaluate the best move for a player in a chess game.
    
    Args:
        board (np.ndarray): The current state of the chess board.
        move_history (np.ndarray): The history of moves made in the game.
        depth (int): The depth of the search tree.
        is_white_turn (bool): True if it's white's turn, False if it's black's turn. White plays has maximizing_player.
        
    Returns:
        The first array is the initial position.\n
        The second array is the destination position.\n
        The third array contain the evaluation at index 0.\n
        [[1, 1, 1], [2, 2, 2], [146, 0, 0]]
    """

    if not has_available_moves(board, move_history) or depth >= max_depth:
        return np.array([[0, 0, 0], [0, 0, 0], [evaluate_board(board, move_history), 0, 0]], dtype=np.float32)

    is_white_turn = len(move_history) % 2 == 0

    if is_white_turn:
        best_state = -np.inf
        best_move = np.zeros((2, 3), dtype=np.float32)
        
        
        if moves.shape[0] == 0:
            moves = get_valid_moves(board, move_history)
        for move in moves:
            new_board = board.copy()
            if apply_move(new_board, move, promotion=5) != MoveResult.SUCCESS:
                raise ValueError("Failed to apply move on the board.", move, new_board)
            state = minimax(
                board=new_board,
                move_history=np.append(move_history, np.expand_dims(move, axis=0), axis=0),
                depth=depth + 1,
                max_depth=max_depth,
                alpha=alpha,
                beta=beta,
            )
            if state[2, 0] > best_state:
                print("max", state, move)
                best_state = state[2, 0]
                best_move = move
            alpha = max(alpha, best_state)
            if beta <= alpha:
                break

    else:
        best_state = np.inf
        best_move = np.zeros((2, 3), dtype=np.float32)
        
        if moves.shape[0] == 0:
            moves = get_valid_moves(board, move_history)
        for move in moves:
            new_board = board.copy()
            if apply_move(new_board, move, promotion=5) != MoveResult.SUCCESS:
                raise ValueError("Failed to apply move on the board.", move, new_board)
            state = minimax(
                board=new_board,
                move_history=np.append(move_history, np.expand_dims(move, axis=0), axis=0),
                depth=depth + 1,
                max_depth=max_depth,
                alpha=alpha,
                beta=beta,
            )
            # print("min", state[2, 0])
            if state[2, 0] < best_state:
                best_state = state[2, 0]
                best_move = move
            beta = min(beta, best_state)
            if beta <= alpha:
                break
    return np.array([
        best_move[0],
        best_move[1],
        [best_state, 0, 0]
    ], dtype=np.float32)


if __name__ == "__main__":
    # Example usage
    from app.chess.ChessPresets import ChessPresets
    from benchmark.MeasureTime import MeasureTime
    from app.chess.Chess import Chess
    from app.movements.movement_representation import move_to_str
    from app.state.king import is_king_in_check
    from app.optimization.jit_configuration import warm_up_jit
    board = ChessPresets.promotion_mat()

    measure_time = MeasureTime(start=True)
    warm_up_jit()
    measure_time.stop(get_str=True)



    MAX_DEPTH = 3
    maximizing_player = True

    measure_time = MeasureTime(start=True)
    move_history = np.zeros((0, 2, 3), dtype=np.int8)
    score = minimax(
                board=board,
                move_history=move_history,
                depth=0,
                max_depth=MAX_DEPTH
            )
    duration = measure_time.stop(get_str=True)
    print(f"Minimax completed in {duration} with depth {MAX_DEPTH}")

    print(f"Minimax score: {score}")

    print(Chess.board_to_str(board))

    
    

    apply_move(board, np.array([[2,7,4], [5,7,0]], dtype=np.int8), promotion=5)
    print(Chess.board_to_str(board))


    king_value = 6 if len(move_history) % 2 == 0 else -6

    positions = np.where(board == king_value)
    if len(positions[0]) > 0:
        y, x = positions[0][0], positions[1][0]

        game_status = np.array([
            is_king_in_check(board, x, y),
            has_available_moves(board, np.append(move_history, np.expand_dims(score[:2], axis=0), axis=0))
        ], dtype=np.int8)

        print(move_to_str(board, np.array(score[:2], dtype=np.int8), game_status))