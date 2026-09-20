from dataclasses import dataclass
from src.chess.constants import BOARD_SIZE
from src.chess.exceptions.illegal_position_error import IllegalPositionError
from src.chess.utils import verify_type



@dataclass
class Position:
    line: int
    column: int


    def __post_init__(self):
        verify_type(self.line, int, "Position(line, column)", "line")
        verify_type(self.column, int, "Position(line, column)", "column")
        
        if not 0 <= self.line < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut line doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")

        if not 0 <= self.column < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut column doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")


    def __repr__(self) -> str:
        return f"({self.line}, {self.column})"