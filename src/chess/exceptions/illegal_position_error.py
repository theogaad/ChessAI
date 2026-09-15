from src.chess.exceptions.chess_error import ChessError



class IllegalPositionError(ChessError):
    def __init__(self, *args):
        super().__init__(*args)