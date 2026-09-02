from src.chess.exceptions.chess_error import ChessError

class IllegalMoveError(ChessError):
    def __init__(self, *args):
        super().__init__(*args)