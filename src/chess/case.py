from dataclasses import dataclass
from src.chess.pieces.piece import Piece
from src.chess.utils import is_valid_position



# Classe représentant une case d'échecs, contenant sa position et éventuellement une pièce
@dataclass
class Case:
    line: int
    column: int
    content: Piece | None = None


    def __post_init__(self):
        is_valid_position(self.line, self.column, "Case(line, column, content)")

        if not isinstance(self.content, Piece) and self.content is not None:
            raise TypeError("Case (line, column, content) L'attribut content doit être du type None ou Piece.")