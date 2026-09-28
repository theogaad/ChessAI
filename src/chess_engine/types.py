from enum import Enum

class Color(Enum):
    """Représente les couleurs des pièces d'échec."""
    
    WHITE = 0
    BLACK = 1

class PieceType(Enum):
    """Représente les types des pièces d'échec."""

    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5

class MoveType(Enum):
    """Représente le type d'un coup aux échecs."""

    NORMAL = "normal"
    CASTLING = "castling"
    EN_PASSANT = "en passant"

class GameStatus(Enum):
    """Représente le status d'une partie d'échecs."""

    ONGOING = "ongoing"
    CHECKMATE = "checkmate"
    DRAW = "draw"
    STALEMATE = "stalemate"
    
class DrawReason(Enum):
    """Représente la raison de la nulle dans une partie d'échecs."""

    REPETITION = "repetition"
    FIFTY_MOVES = "fifty moves"
    INSUFFICIENT_MATERIAL = "insufficient_material"