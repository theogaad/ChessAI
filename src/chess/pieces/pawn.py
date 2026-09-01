from src.chess.pieces.piece import Piece, PieceColor
from src.chess.constants import BOARD_SIZE

class Pawn(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)
        self.has_moved = False

    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        list_of_possible_moves: list[tuple[int, int]] = []
        coeff: int = 1 if self.piece_color == PieceColor.WHITE else -1
        offsets: list[tuple[int, int]] = [(1 * coeff, 0), (1 * coeff, 1), (1 * coeff, -1)]
        if not self.has_moved:
            offsets.append((2 * coeff, 0))
        for offset in offsets:
            if 0 <= line + offset[0] < BOARD_SIZE and 0 <= column + offset[1] < BOARD_SIZE:
                list_of_possible_moves.append((line + offset[0], column + offset[1]))
        return list_of_possible_moves