from src.chess.constants import BOARD_SIZE
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.utils import is_valid_position



class Knight(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)


    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        is_valid_position(line, column, "get_moves(self, line, column)")

        list_of_possible_moves: list[tuple[int, int]] = []
        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

        for offset in offsets:
            new_position: tuple[int, int] = (line + offset[0], column + offset[1])

            if 0 <= new_position[0] < BOARD_SIZE and 0 <= new_position[1] < BOARD_SIZE:
                list_of_possible_moves.append(new_position)

        return list_of_possible_moves