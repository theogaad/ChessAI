from dataclasses import dataclass
from src.chess.pieces.piece import Piece
from src.chess.position import Position



# Classe représentant une case d'échecs, contenant sa position et éventuellement une pièce
@dataclass
class Case:
    position: Position
    content: Piece | None = None


    def __post_init__(self):
        if not isinstance(self.content, Piece) and self.content is not None:
            raise TypeError("Case (position, content) L'attribut content doit être du type None ou Piece.")