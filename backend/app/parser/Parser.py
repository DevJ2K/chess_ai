class Parser:
    """Movement ReGex
    (O-O(-O)?|[KQRBN]?[a-h]?[1-8]?[x]?[a-h][1-8](=[QRBN])?[+#]?)

    """
    @staticmethod
    def parse_move(move: str) -> tuple[str, str]:
        return ("e", "")
