from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position
from src.chess.utils import verify_type



class King(Piece):
    def __init__(self, color: PieceColor) -> None:
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        list_of_positions: list[Position] = []
        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for offset in offsets:
            list_of_positions.append(Position(position.line + offset[0], position.column + offset[1]))
                
        return list_of_positions