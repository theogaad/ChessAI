from enum import Enum, IntFlag

class Color(Enum):
    """Représente les couleurs des pièces d'échec."""
    
    WHITE = 0
    BLACK = 1

    @property
    def opposite(self) -> "Color":
        """Retourne la couleur opposée.

        Returns:
            La couleur opposée à celle de l'instance.
        """

        return Color.BLACK if self is Color.WHITE else Color.WHITE

class PieceType(Enum):
    """Représente les types des pièces d'échec."""

    KING = 0
    QUEEN = 1
    ROOK = 2
    BISHOP = 3
    KNIGHT = 4
    PAWN = 5

class PieceValue(Enum):
    KING = 0
    QUEEN = 13
    ROOK = 5
    BISHOP = 3
    KNIGHT = 3
    PAWN = 1

class MoveType(Enum):
    """Représente le type d'un coup aux échecs."""

    NORMAL = "normal"
    CASTLING = "castling"
    EN_PASSANT = "en passant"

class GameStatus(Enum):
    """Représente le statut d'une partie d'échecs."""

    ONGOING = "ongoing"
    CHECKMATE = "checkmate"
    DRAW = "draw"
    STALEMATE = "stalemate"
    
class DrawReason(Enum):
    """Représente la raison de la nulle dans une partie d'échecs."""

    REPETITION = "repetition"
    FIFTY_MOVES = "fifty moves"
    INSUFFICIENT_MATERIAL = "insufficient_material"

class CastlingRights(IntFlag):
    """Représente les droits de roque disponibles."""

    NONE = 0
    WHITE_KINGSIDE = 1 << 0
    WHITE_QUEENSIDE = 1 << 1
    BLACK_KINGSIDE = 1 << 2
    BLACK_QUEENSIDE = 1 << 3

class EventType(Enum):
    """Représente les types d'évennement possibles dans l'interface graphique."""
    NONE = "None"
    CLICK = "Click"
    QUIT = "Quit"