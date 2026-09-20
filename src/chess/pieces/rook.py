from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position



class Rook(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)
        self.has_moved = False


    def get_positions(self, position: Position) -> list[Position]:
        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        list_of_possible_moves: list[Position] = self.get_sliding_moves(position, offsets)
        
        return list_of_possible_moves