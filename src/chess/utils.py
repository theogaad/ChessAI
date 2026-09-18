from src.chess.constants import BOARD_SIZE
from src.chess.exceptions.illegal_position_error import IllegalPositionError



def get_sliding_moves(line: int, column: int, offsets: list[tuple[int, int]]) -> list[tuple[int, int]]:
    list_of_possible_moves: list[tuple[int, int]] = []

    # "offset" désigne un mouvement/direction possible de la pièce
    for offset in offsets:
        i = 1
        
        while 0 <= line + offset[0] * i < BOARD_SIZE and 0 <= column + offset[1] * i < BOARD_SIZE:
            new_position = (line + offset[0] * i, column + offset[1] * i)
            list_of_possible_moves.append(new_position)
            i += 1

    return list_of_possible_moves


def is_valid_position(line: int, column: int, function_name: str) -> None:
    if (not isinstance(line, int) or 
        not isinstance(column, int)):
        raise TypeError("is_valid_position(line, column, function_name) Les paramètre line et column doivent être du type int.")

    if not isinstance(function_name, str):
        raise TypeError("is_valid_position(line, column, function_name) Le paramètre function_name doit être du type str.")
    
    if not (0 <= line < BOARD_SIZE and 0 <= column < BOARD_SIZE):
        raise IllegalPositionError(function_name + " Le couple (line, column) doit être une coordonnée valide comprise entre 0 et BOARD_SIZE.")