from src.chess.constants import BOARD_SIZE
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position



class Pawn(Piece):
    def __init__(self, color: PieceColor):
        super().__init__(color)
        self.has_moved = False


    def get_positions(self, position: Position) -> list[Position]:
        list_of_possible_moves: list[Position] = []
        coeff: int = 1 if self.piece_color == PieceColor.WHITE else -1
        # "offset" désigne un mouvement/direction possible de la pièce
        offsets: list[tuple[int, int]] = [(1 * coeff, 0), (1 * coeff, 1), (1 * coeff, -1)]

        if not self.has_moved:
            offsets.append((2 * coeff, 0))

        for offset in offsets:
            list_of_possible_moves.append(Position(position.line + offset[0], position.column + offset[1]))

        return list_of_possible_moves