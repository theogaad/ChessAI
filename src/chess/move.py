from dataclasses import dataclass
from enum import Enum
from src.chess.case import Case
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.knight import Knight
from src.chess.pieces.piece import Piece
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
    captured_piece: None | Piece = None


    def __post_init__(self) -> None:
        if not isinstance(self.start, Case):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) L'attribut start doit être du type Case.")

        if not isinstance(self.start.content, Piece):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) La Case contenue dans start doit contenir une Piece.")

        if not isinstance(self.end, Case):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) L'attribut end doit être du type Case.")

        self.moving_piece: Piece = self.start.content

        if not isinstance(self.moving_piece, Piece):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) L'attribut moving_piece doit être du type Piece.")
        
        if not isinstance(self.special_move, SpecialMove):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) L'attribut special_move doit être du type SpecialMove.")
        
        if not (self.promotion_piece_type in (Bishop, Knight, Queen, Rook) or 
                self.promotion_piece_type is None):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) L'attribut promotion_piece_type doit être du type None, Bishop, Knight, Queen ou Rook.")

        if not (isinstance(self.captured_piece, Piece) or 
                self.captured_piece is None):
            raise TypeError("Move(start, end, special_move, promotion_piece_type, captured_piece) L'attribut captured_piece doit être du type Piece ou None.")