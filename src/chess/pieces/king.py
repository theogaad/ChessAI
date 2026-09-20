from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position



class King(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)
        self.has_moved = False


    def get_positions(self, position: Position) -> list[Position]:
        list_of_possible_moves: list[Position] = []
        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for offset in offsets:
            list_of_possible_moves.append(Position(position.line + offset[0], position.column + offset[1]))
                
        return list_of_possible_moves