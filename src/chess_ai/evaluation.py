from enum import Enum

from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType, PieceValue


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
                        piece_value = PieceValue.QUEEN.value
                    case PieceType.ROOK:
                        piece_value = PieceValue.ROOK.value
                    case PieceType.BISHOP:
                        piece_value = PieceValue.BISHOP.value
                    case PieceType.KNIGHT:
                        piece_value = PieceValue.KNIGHT.value
                    case PieceType.PAWN:
                        piece_value = PieceValue.PAWN.value
                    case _:
                        pass

                score += coeff * pieces_count * piece_value

        if position.side_to_move is Color.BLACK:
            score = -score

        return score