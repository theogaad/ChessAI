from src.chess.pieces.piece import Piece, PieceColor
from src.chess.move_utils import get_sliding_moves

class Rook(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)

    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        offsets: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        list_of_possible_moves: list[tuple[int, int]] = get_sliding_moves(line, column, offsets)
        return list_of_possible_moves