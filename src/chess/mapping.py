from src.chess.exceptions.chess_error import ChessError
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook



def str_to_promotion_piece_type(string: str) -> type[Bishop | Knight | Queen | Rook]:
    if string == "Bishop":
        return Bishop

    elif string == "Knight":
        return Knight

    elif string == "Queen":
        return Queen

    elif string == "Rook":
        return Rook

    else:
        raise ChessError("str_to_promotion_piece_type(string) Le paramètre string doit être une chaîne de caractères parmi 'Bishop', 'Knight', 'Queen' et 'Rook'.")