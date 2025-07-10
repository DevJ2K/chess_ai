from app.utils.Colors import BHMAG, BHGREEN, BHCYAN, RESET
from time import time
import numpy as np
from pathlib import Path


import ast
import os

def njit_functions(directory):
    count = 0
    functions = []
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".py"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    try:
                        tree = ast.parse(file.read(), filename=filename)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):  # fonction trouvée
                                for decorator in node.decorator_list:
                                    if (
                                        isinstance(decorator, ast.Name) and decorator.id == "njit"
                                    ) or (
                                        isinstance(decorator, ast.Attribute) and decorator.attr == "njit"
                                    ):
                                        functions.append((filename, node.name))
                                        count += 1
                    except SyntaxError:
                        print(f"⚠️ SyntaxError dans {filename} (ignoré)")
    return functions

def get_board() -> np.ndarray:
    return np.zeros((8, 8), dtype=np.int8)

def warm_up_jit():
    # WARMUP Numba JIT compilation
    functions_to_warm_up = njit_functions(Path(__file__).resolve().parent.parent)
    functions_test = []

    filename_test = ""
    def test(function_name: str = ""):
        functions_test.append((filename_test + ".py", function_name))

    print(BHCYAN + f"{len(functions_to_warm_up)} functions decorated with @njit will be warmed up." + RESET)
    print(BHMAG + "Warming up Numba JIT compilation..." + RESET)
    start_time = time()

    # ====================================================
    from app.movements.piece_moves import (
        get_pawn_moves, get_knight_moves, get_bishop_moves,
        get_rook_moves, get_queen_moves, get_king_moves)
    filename_test = "piece_moves"

    get_pawn_moves(get_board(), 0, 0, True), test("get_pawn_moves")
    get_knight_moves(get_board(), 0, 0), test("get_knight_moves")
    get_bishop_moves(get_board(), 0, 0), test("get_bishop_moves")
    get_rook_moves(get_board(), 0, 0), test("get_rook_moves")
    get_queen_moves(get_board(), 0, 0), test("get_queen_moves")
    get_king_moves(get_board(), 0, 0, False, False, False), test("get_king_moves")
    # ====================================================
    #
    # ====================================================
    from app.movements.get_moves import is_not_dangerous_for_king, get_valid_moves, is_move_startswith
    filename_test = "get_moves"

    get_valid_moves(
        get_board(),
        np.empty((0, 2, 3), dtype=np.int8),
    ), test("get_valid_moves")
    is_not_dangerous_for_king(
        get_board(),
        np.array([0, 0], dtype=np.int8),
        np.array([0, 0], dtype=np.int8),
        is_white_turn=True
    ), test("is_not_dangerous_for_king")
    is_move_startswith(
        np.empty((0, 2, 3), dtype=np.int8),
        np.array([[0, 0, 0], [0, 0, 0]], dtype=np.int8)
    ), test("is_move_startswith")
    # ====================================================
    #
    # ====================================================
    from app.movements.king_movement_utils import is_square_under_attack, can_castle_kingside, can_castle_queenside
    filename_test = "king_movement_utils"

    is_square_under_attack(get_board(), 0, 0, is_white_piece=True), test("is_square_under_attack")
    can_castle_kingside(get_board(), 0, 0, False), test("can_castle_kingside")
    can_castle_queenside(get_board(), 0, 0, False), test("can_castle_queenside")
    # ====================================================
    #
    # ====================================================
    from app.movements.piece_utils import is_in_board
    filename_test = "piece_utils"

    is_in_board(get_board(), 0, 0), test("is_in_board")
    # ====================================================
    #
    # ====================================================
    from app.state.king import is_king_in_check
    filename_test = "king"

    is_king_in_check(get_board(), 0, 0), test("is_king_in_check")
    # ====================================================
    #
    # ====================================================
    from app.state.moves import has_available_moves
    filename_test = "moves"

    has_available_moves(get_board(), np.empty((0, 2, 3), dtype=np.int8)), test("has_available_moves")
    # ====================================================
    #
    # ====================================================
    from app.movements.apply_move import apply_move
    filename_test = "apply_move"

    apply_move(get_board(), np.array([[0, 0, 1], [1, 1, 0]], dtype=np.int8), promotion=5), test("apply_move")
    # ====================================================
    #
    # ====================================================
    from app.algorithm.minimax import minimax
    filename_test = "minimax"

    minimax(
        get_board(),
        np.empty((0, 2, 3), dtype=np.int8),
        depth=0,
        max_depth=0
    ), test("minimax")
    # ====================================================
    #
    # ====================================================
    from app.state.evaluate import evaluate_board
    filename_test = "evaluate"

    evaluate_board(get_board(), np.empty((0, 2, 3), dtype=np.int8)), test("evaluate_board")

    end_time = time()

    count = len(functions_test)
    if count != len(functions_to_warm_up):
        print(BHMAG + f"⚠️ Error: {len(functions_to_warm_up) - count} functions were not warmed up." + RESET)
        print("".join(
            f"  - {filename}::{function_name}\n"
            for filename, function_name in functions_to_warm_up if (filename, function_name) not in functions_test
        ))
        exit(1)
    else:
        print(BHGREEN + f"✅ All {count} functions were warmed up successfully." + RESET)

    print(BHGREEN + f"Numba JIT compilation warmed up in {end_time - start_time:.3f} seconds." + RESET)
