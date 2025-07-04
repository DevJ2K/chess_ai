from app.parser.Parser import Parser

def test_pawn_move():
    move = "e4"
    parsed_move = Parser.parse_move(move)
    assert parsed_move == ("e", "4")
