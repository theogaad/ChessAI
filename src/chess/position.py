from dataclasses import dataclass
from src.chess.constants import BOARD_SIZE
from src.chess.exceptions.illegal_position_error import IllegalPositionError



@dataclass
class Position:
    line: int
    column: int


    def __post_init__(self):
        if not isinstance(self.line, int):
            raise TypeError("Position(line, column) L'atribut line doit être du type int.")

        if not isinstance(self.column, int):
            raise TypeError("Position(line, column) L'atribut column doit être du type int.")
        
        if not 0 <= self.line < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut line doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")

        if not 0 <= self.column < BOARD_SIZE:
            raise IllegalPositionError(f"Position(line, column) L'attribut column doit être supérieur ou égal à 0 et inférieur à {BOARD_SIZE}.")


    #def is_equal(self, position: Position) -> bool:
        #if not isinstance(position, Position):
            #raise TypeError("is_equal(self, position) Le paramètre position doit être du type Position.")

        #return self.line == position.line and self.column == position.column