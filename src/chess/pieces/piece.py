from abc import ABC, abstractmethod
from enum import Enum
from src.chess.constants import BOARD_SIZE
from src.chess.position import Position
from src.chess.utils import verify_type



# Enum des couleurs de pièces
class PieceColor(Enum):
    WHITE = "white"
    BLACK = "black"



# Classe représentant une pièce d'échecs, contenant son type et sa couleur
class Piece(ABC):
    def __init__(self, color: PieceColor) -> None:
        verify_type(color, PieceColor, "Piece(color)", "color")
        
        self.piece_color = color
        self.has_moved: bool = False


    def set_has_moved(self, new_bool: bool) -> None:
        verify_type(new_bool, bool, "set_has_moved(new_bool)", "new_bool")

        self.has_moved = new_bool


    def get_sliding_positions(self, position: Position, offsets: list[tuple[int, int]]) -> list[Position]:
        verify_type(position, Position, "get_sliding_positions(position, offsets)", "position")
        verify_type(offsets, list[tuple[int, int]], "get_sliding_positions(position, offsets)", "offsets")

        list_of_positions: list[Position] = []

        # "offset" désigne un mouvement/direction possible de la pièce
        for offset in offsets:
            i = 1
            
            while 0 <= position.line + offset[0] * i < BOARD_SIZE and 0 <= position.column + offset[1] * i < BOARD_SIZE:
                new_position: Position = Position(position.line + offset[0] * i, position.column + offset[1] * i)
                list_of_positions.append(new_position)
                i += 1

        return list_of_positions


    @abstractmethod
    def get_reachable_positions(self, position: Position) -> list[Position]:
        pass

