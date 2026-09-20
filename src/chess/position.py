from dataclasses import dataclass
from src.chess.constants import BOARD_SIZE
from src.chess.exceptions.illegal_position_error import IllegalPositionError
from src.chess.utils import verify_type



@dataclass
class Position:
    """Dataclass représentant une position valide dans un plateau d'échecs.
    
    line (public) -- valeur de la verticalité
    column (public) -- valeur de l'horizontalité
    """
    line: int
    column: int


    def __post_init__(self):
        """Vérifie la validité de la position en vérifiant les types et valeurs des attributs line et column."""
        verify_type(self.line, int, "Position(line, column)", "line")
        verify_type(self.column, int, "Position(line, column)", "column")
        
        if not 0 <= self.line < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut line doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")

        if not 0 <= self.column < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut column doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")


    def __repr__(self) -> str:
        """Définis la représentation en chaîne de caractères d'une Position."""
        return f"({self.line}, {self.column})"