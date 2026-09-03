from src.chess.pieces.piece import Piece, PieceColor
from src.chess.constants import BOARD_SIZE

class King(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)
        self.has_moved = False

    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        list_of_possible_moves: list[tuple[int, int]] = []
        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for offset in offsets:
            if 0 <= line + offset[0] < BOARD_SIZE and 0 <= column + offset[1] < BOARD_SIZE:
                list_of_possible_moves.append((line + offset[0], column + offset[1]))
        return list_of_possible_moves