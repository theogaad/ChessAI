from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position
from src.chess.utils import verify_type



class Rook(Piece):
    def __init__(self, color: PieceColor) -> None:
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        list_of_positions: list[Position] = self.get_reachable_sliding_positions_from_position(position, offsets)
        
        return list_of_positions