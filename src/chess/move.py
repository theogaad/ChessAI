from dataclasses import dataclass
from enum import Enum
from src.chess.case import Case
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.knight import Knight
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook



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


    def __post_init__(self) -> None:
        if not isinstance(self.special_move, SpecialMove):
            raise TypeError("L'attribut special_move doit être du type SpecialMove.")
        
        if self.promotion_piece_type not in (Bishop, Knight, Queen, Rook) and self.promotion_piece_type is not None:
            raise TypeError("L'attribut promotion_piece_type doit être du type None, Bishop, Knight, Queen ou Rook.")