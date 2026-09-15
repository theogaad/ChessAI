from abc import ABC, abstractmethod
from enum import Enum



# Enum des couleurs de pièces
class PieceColor(Enum):
    WHITE = "white"
    BLACK = "black"



# Classe représentant une pièce d'échecs, contenant son type et sa couleur
class Piece(ABC):
    def __init__(self, color: PieceColor) -> None:
        if not isinstance(color, PieceColor):
            raise TypeError("Piece(self, color) L'attribut color doit être du type PieceColor.")
        
        self.piece_color = color


    @abstractmethod
    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        pass

