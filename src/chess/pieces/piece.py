from abc import ABC, abstractmethod
from enum import Enum
from src.chess.constants import BOARD_SIZE
from src.chess.position import Position
from src.chess.utils import verify_type



# Enum des couleurs de pièces
class PieceColor(Enum):
    WHITE = "White"
    BLACK = "Black"



# Classe représentant une pièce d'échecs, contenant sa couleur, et l'information sur son premier mouvement
class Piece(ABC):
    def __init__(self, color: PieceColor) -> None:
        verify_type(color, PieceColor, "Piece(color)", "color")
        
        self.__piece_color = color
        self.__has_moved: bool = False


    @property
    def piece_color(self) -> PieceColor:
        return self.__piece_color


    @piece_color.setter
    def piece_color(self, new_piece_color: PieceColor) -> None:
        verify_type(new_piece_color, PieceColor, "piece_color(new_piece_color)", "new_piece_color")

        self.__piece_color = new_piece_color


    @property
    def has_moved(self) -> bool:
        return self.__has_moved


    @has_moved.setter
    def has_moved(self, new_has_moved: bool) -> None:
        verify_type(new_has_moved, bool, "set_has_moved(new_has_moved)", "new_has_moved")

        self.__has_moved = new_has_moved


    def get_reachable_sliding_positions_from_position(self, position: Position, offsets: list[tuple[int, int]]) -> list[Position]:
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


    def __repr__(self) -> str:
        return f"{type(self).__name__}[color: {self.piece_color.value}, has_moved: {self.has_moved}]"

    
    @abstractmethod
    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        pass