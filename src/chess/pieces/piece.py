from abc import ABC, abstractmethod
from enum import Enum
from src.chess.constants import BOARD_SIZE
from src.chess.position import Position



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


    def get_sliding_moves(self, position: Position, offsets: list[tuple[int, int]]) -> list[Position]:
        list_of_possible_moves: list[Position] = []

        # "offset" désigne un mouvement/direction possible de la pièce
        for offset in offsets:
            i = 1
            
            while 0 <= position.line + offset[0] * i < BOARD_SIZE and 0 <= position.column + offset[1] * i < BOARD_SIZE:
                new_position: Position = Position(position.line + offset[0] * i, position.column + offset[1] * i)
                list_of_possible_moves.append(new_position)
                i += 1

        return list_of_possible_moves


    @abstractmethod
    def get_reachable_positions(self, position: Position) -> list[Position]:
        pass

