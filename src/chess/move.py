from src.chess.case import Case
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.knight import Knight
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from dataclasses import dataclass
from enum import Enum

class SpecialMove(Enum):
    NONE = "none"
    CASTLING = "roque"
    PROMOTION = "promotion"
    EN_PASSANT = "en_passant"

@dataclass
class Move:
    start: Case
    end: Case
    special_move: SpecialMove = SpecialMove.NONE
    promotion_piece_type: None | type[Bishop|Knight|Queen|Rook] = None