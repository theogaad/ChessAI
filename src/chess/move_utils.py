from src.chess.constants import BOARD_SIZE

def get_sliding_moves(line: int, column: int, offsets: list[tuple[int, int]]) -> list[tuple[int, int]]:
    list_of_possible_moves: list[tuple[int, int]] = []
    for offset in offsets:
        i = 1
        while 0 <= line + offset[0] * i < BOARD_SIZE and 0 <= column + offset[1] * i < BOARD_SIZE:
            new_position = (line + offset[0] * i, column + offset[1] * i)
            list_of_possible_moves.append(new_position)
            i += 1
    return list_of_possible_moves