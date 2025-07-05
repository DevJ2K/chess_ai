import tests.configuration
from app.chess.PieceMovement import PieceMovement
from app.chess.Chess import Chess
import numpy as np

def test_default_pawn_movement():
    board = Chess.initialize_board()
    piece_movement = PieceMovement()

    # WHITE PAWNS
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True),
        np.array([(0, 2), (0, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=1, y=1, is_white_turn=True),
        np.array([(1, 2), (1, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=2, y=1, is_white_turn=True),
        np.array([(2, 2), (2, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=3, y=1, is_white_turn=True),
        np.array([(3, 2), (3, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=4, y=1, is_white_turn=True),
        np.array([(4, 2), (4, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=5, y=1, is_white_turn=True),
        np.array([(5, 2), (5, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=6, y=1, is_white_turn=True),
        np.array([(6, 2), (6, 3)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=7, y=1, is_white_turn=True),
        np.array([(7, 2), (7, 3)])
    )

    # BLACK PAWNS
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=6, is_white_turn=False),
        np.array([(0, 5), (0, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=1, y=6, is_white_turn=False),
        np.array([(1, 5), (1, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=2, y=6, is_white_turn=False),
        np.array([(2, 5), (2, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=3, y=6, is_white_turn=False),
        np.array([(3, 5), (3, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=4, y=6, is_white_turn=False),
        np.array([(4, 5), (4, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=5, y=6, is_white_turn=False),
        np.array([(5, 5), (5, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=6, y=6, is_white_turn=False),
        np.array([(6, 5), (6, 4)])
    )
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=7, y=6, is_white_turn=False),
        np.array([(7, 5), (7, 4)])
    )

def test_pawn_movement_with_obstacles():
    piece_movement = PieceMovement()

    # black pawn at (0, 2)
    board = Chess.initialize_board()
    board[2, 0] = -1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True),
        np.empty((0, 2))
    )

    # black pawn at (0, 3)
    board = Chess.initialize_board()
    board[3, 0] = -1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True),
        np.array([(0, 2)])
    )

    # white pawn at (0, 5)
    board = Chess.initialize_board()
    board[5, 0] = 1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=6, is_white_turn=False),
        np.empty((0, 2))
    )

    # white pawn at (0, 4)
    board = Chess.initialize_board()
    board[4, 0] = 1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=6, is_white_turn=False),
        np.array([(0, 5)])
    )

    # white pawn at (0, 2)
    board = Chess.initialize_board()
    board[2, 0] = 1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True),
        np.empty((0, 2))
    )

    # black pawn at (0, 5)
    board = Chess.initialize_board()
    board[5, 0] = -1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=6, is_white_turn=False),
        np.empty((0, 2))
    )

def test_pawn_movement_capture():
    piece_movement = PieceMovement()

    # white pawn at (0, 1) capturing black pawn at (1, 2)
    board = Chess.initialize_board()
    board[2, 1] = -1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=1, is_white_turn=True),
        np.array([(0, 2), (0, 3), (1, 2)])
    )

    # black pawn at (0, 6) capturing white pawn at (1, 5)
    board = Chess.initialize_board()
    board[5, 1] = 1
    np.testing.assert_array_equal(
        piece_movement.get_pawn_movement(board, x=0, y=6, is_white_turn=False),
        np.array([(0, 5), (0, 4), (1, 5)])
    )
