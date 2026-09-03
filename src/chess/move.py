from src.chess.case import Case
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