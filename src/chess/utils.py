from src.chess.constants import BOARD_SIZE
from src.chess.position import Position



def get_sliding_moves(position: Position, offsets: list[tuple[int, int]]) -> list[Position]:
    list_of_possible_moves: list[Position] = []

    # "offset" désigne un mouvement/direction possible de la pièce
    for offset in offsets:
        i = 1
        
        while 0 <= position.line + offset[0] * i < BOARD_SIZE and 0 <= position.column + offset[1] * i < BOARD_SIZE:
            new_position: Position = Position(position.line + offset[0] * i, position.column + offset[1] * i)
            list_of_possible_moves.append(new_position)
            i += 1

    return list_of_possible_moves


def verify_type(obj_to_verify: object, type: type, function_name: str, variable_name: str) -> None:
    if not isinstance(obj_to_verify, type):
        raise TypeError(f"{function_name} Le paramètre {variable_name} doit être du type {type}.")