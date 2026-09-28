from src.chess.exceptions.chess_error import ChessError
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.position import Position
from src.chess.utils import BOARD_SIZE, CASE_SIZE



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


def chess_line_to_pygame_line(line: int) -> int:
    return (BOARD_SIZE - 1 - line) * CASE_SIZE

def chess_position_to_pygame_position(position: Position) -> tuple[int, int]:
    return (position.column * CASE_SIZE, chess_line_to_pygame_line(position.line))

def pygame_line_to_chess_line(line: int) -> int:
    return BOARD_SIZE - 1 - (line // CASE_SIZE)

def pygame_position_to_chess_position(position: tuple[int, int]) -> Position:
    return Position(pygame_line_to_chess_line(position[1]), position[0] // CASE_SIZE)

def piece_type_to_str(piece: Piece) -> str:
    if not isinstance(piece, Piece):
        raise TypeError("piece_type_to_str(piece) Le paramètre piece doit être du type Piece.")
    
    elif isinstance(piece, Bishop):
        return "Bishop"

    elif isinstance(piece, Knight):
        return "Knight"

    elif isinstance(piece, King):
        return "King"

    elif isinstance(piece, Pawn):
        return "Pawn"

    elif isinstance(piece, Queen):
        return "Queen"
    
    elif isinstance(piece, Rook):
        return "Rook"

    else:
        return "None"

def piece_type_to_image_name(piece: Piece) -> str:
    if not isinstance(piece, Piece):
        raise TypeError("piece_type_to_image_name(piece) Le paramètre piece doit être du type Piece.")

    return f"{piece.piece_color.value}_{piece_type_to_str(piece)}"