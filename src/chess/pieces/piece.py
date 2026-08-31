from enum import Enum
from abc import ABC, abstractmethod

# Enum des couleurs de pièces
class PieceColor(Enum):
    WHITE = "white"
    BLACK = "black"

# Classe représentant une pièce d'échecs, contenant son type et sa couleur
class Piece(ABC):
    def __init__(self, color: PieceColor) -> None:
        if not isinstance(color, PieceColor):
            raise ValueError("Invalid piece color")
        self.piece_color = color

    @abstractmethod
    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        pass

