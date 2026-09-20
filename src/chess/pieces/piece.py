from abc import ABC, abstractmethod
from enum import Enum
from src.chess.constants import BOARD_SIZE
from src.chess.position import Position
from src.chess.utils import verify_type



# Enum des couleurs de pièces
class PieceColor(Enum):
    """Enum représantant les deux couleurs possibles au échecs."""
    WHITE = "White"
    BLACK = "Black"



class Piece(ABC):
    """ Classe abstraite représentant une pièce d'échecs.
    
    piece_color -- couleur de la pièce
    has_moved -- permet de savoir si la pièce a déjà bougé
    Les deux attributs sont privés.
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise une Piece avec une couleur donnée, has_moved est à False à la création."""
        verify_type(color, PieceColor, "Piece(color)", "color")
        
        self.__piece_color = color
        self.__has_moved: bool = False


    @property
    def piece_color(self) -> PieceColor:
        """Renvoie la couleur de la Piece."""
        return self.__piece_color


    @piece_color.setter
    def piece_color(self, new_piece_color: PieceColor) -> None:
        """Modifie la couleur de la Piece."""
        verify_type(new_piece_color, PieceColor, "piece_color(new_piece_color)", "new_piece_color")

        self.__piece_color = new_piece_color


    @property
    def has_moved(self) -> bool:
        """Renvoie l'attribut has_moved."""
        return self.__has_moved


    @has_moved.setter
    def has_moved(self, new_has_moved: bool) -> None:
        """Modifie l'attribut has_moved."""
        verify_type(new_has_moved, bool, "set_has_moved(new_has_moved)", "new_has_moved")

        self.__has_moved = new_has_moved


    def get_reachable_sliding_positions_from_position(self, position: Position, directions: list[tuple[int, int]]) -> list[Position]:
        """Calcule les positions atteignables en fonction de la position de départ et des directions.
        
        position -- position de départ
        directions -- liste des directions
        Renvoie une liste de Position.
        """
        verify_type(position, Position, "get_sliding_positions(position, offsets)", "position")
        verify_type(directions, list[tuple[int, int]], "get_sliding_positions(position, offsets)", "offsets")

        list_of_positions: list[Position] = []

        for direction in directions:
            i = 1
            
            while 0 <= position.line + direction[0] * i < BOARD_SIZE and 0 <= position.column + direction[1] * i < BOARD_SIZE:
                list_of_positions.append(Position(position.line + direction[0] * i, position.column + direction[1] * i))
                i += 1

        return list_of_positions


    def __repr__(self) -> str:
        """Définis la représentation en chaîne de caractères d'une Piece."""
        return f"{type(self).__name__}[color: {self.piece_color.value}, has_moved: {self.has_moved}]"


    def __eq__(self, value) -> bool:
        """Compare le type des Piece et leur couleur, renvoie leur égalité."""
        return type(self).__name__ == type(value).__name__ and self.piece_color == value.piece_color

    
    @abstractmethod
    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Calcule les positions atteignables par la Piece en fonction de son type et de sa position.
        
        position -- position de départ
        Renvoie une liste de Position.
        """
        pass