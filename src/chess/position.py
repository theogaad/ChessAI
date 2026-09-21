from dataclasses import dataclass
from src.chess.exceptions.illegal_position_error import IllegalPositionError
from src.chess.utils import BOARD_SIZE, verify_type



@dataclass
class Position:
    """Représente une position valide sur l'échiquier.
    
    Attributes:
        line: Indice de la ligne, compris entre 0 et BOARD_SIZE - 1.
        column: Indice de la colonne, compris entre 0 et BOARD_SIZE - 1.
    """
    line: int
    column: int


    def __post_init__(self) -> None:
        """Vérifie les types et valeurs des attributs de la position.
        
        Raises:
            TypeError: Si ``line`` ou ``column`` n'est pas un entier.
            IllegalPositionError: Si ``line`` ou ``column`` est hors des limites de l'échiquier.
        """
        verify_type(self.line, int, "Position(line, column)", "line")
        verify_type(self.column, int, "Position(line, column)", "column")
        
        if not 0 <= self.line < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut line doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")

        if not 0 <= self.column < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut column doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")


    def __repr__(self) -> str:
        """Retourne la représentation textuelle d'une position."""
        return f"({self.line}, {self.column})"