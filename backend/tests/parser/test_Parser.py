from app.parser.Parser import Parser

def test_pawn_move():
    """
    (piece, line, column)
    """

    assert Parser.parse_move("e4") == (1, 3, 4)
    assert Parser.parse_move("a3") == (1, 3, 7)


def test_bishop_move():
    assert Parser.parse_move("Bc4") == (2, 3, 2)
    assert Parser.parse_move("Bb5") == (2, 4, 1)


def test_knight_move():
    assert Parser.parse_move("Nf3") == (3, 5, 6)
    assert Parser.parse_move("Nc6") == (3, 6, 2)


def test_rook_move():
    assert Parser.parse_move("Ra1") == (4, 0, 0)
    assert Parser.parse_move("Rf8") == (4, 7, 5)


def test_queen_move():
    assert Parser.parse_move("Qd1") == (5, 0, 3)
    assert Parser.parse_move("Qh5") == (5, 4, 7)


def test_king_move():
    assert Parser.parse_move("Ke1") == (6, 0, 4)
    assert Parser.parse_move("Kg8") == (6, 7, 6)

def test_invalid_move():
    assert Parser.parse_move("e9") == None
    assert Parser.parse_move("x3") == None
    assert Parser.parse_move("a0") == None
    assert Parser.parse_move("h9") == None
    assert Parser.parse_move("Qz1") == None
    assert Parser.parse_move("N@3") == None
    assert Parser.parse_move("R#1") == None
    assert Parser.parse_move("B$4") == None
