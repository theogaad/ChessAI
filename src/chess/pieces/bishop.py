from src.chess.pieces.piece import Piece, PieceColor
from src.chess.utils import get_sliding_moves, is_valid_position



class Bishop(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)


    def get_moves(self, line: int, column: int) -> list[tuple[int, int]]:
        is_valid_position(line, column, "get_moves(self, line, column)")

        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        list_of_possible_moves: list[tuple[int, int]] = get_sliding_moves(line, column, offsets)
        
        return list_of_possible_moves