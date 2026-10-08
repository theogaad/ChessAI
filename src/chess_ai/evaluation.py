from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType


class Evaluation:
    def evaluate_position(self, position: Position) -> int:
        score: int = 0

        for piece_type in PieceType:
            for color in Color:
                coeff: int = 1 if color is Color.WHITE else -1
                pieces_count: int = position.piece_bitboards.get_bitboard(color, piece_type).bit_count()

                piece_value: int = 0
                match piece_type:
                    case PieceType.QUEEN:
                        piece_value = 13
                    case PieceType.ROOK:
                        piece_value = 5
                    case PieceType.BISHOP:
                        piece_value = 3
                    case PieceType.KNIGHT:
                        piece_value = 3
                    case PieceType.PAWN:
                        piece_value = 1
                    case _:
                        pass

                score += coeff * pieces_count * piece_value

        if position.side_to_move is Color.BLACK:
            score = -score

        return score