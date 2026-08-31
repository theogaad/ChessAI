from src.chess.pieces.piece import Piece
from dataclasses import dataclass
from src.chess.constants import BOARD_SIZE

# Classe représentant une case d'échecs, contenant sa position et éventuellement une pièce
@dataclass
class Case:
    line: int
    column: int
    content: Piece | None = None

    def __post_init__(self):
        if not (0 <= self.line < BOARD_SIZE and 0 <= self.column < BOARD_SIZE):
            raise ValueError("Invalid position")