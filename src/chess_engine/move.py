from dataclasses import dataclass

from src.chess_engine.types import MoveType, PieceType


@dataclass
class Move:
    """Représente un coup d'échecs.

    Un coup est défini par sa case de départ, sa case d'arrivée et son type.
    Pour les coups de promotion, le type de pièce obtenu est également
    renseigné.

    Attributes:
        start_square: Indice de la case de départ.
        end_square: Indice de la case d'arrivée.
        move_type: Type du coup.
        promotion_piece_type: Type de pièce résultant de la promotion, ou
            None si le coup n'est pas une promotion.
    """

    start_square: int
    end_square: int
    move_type: MoveType
    promotion_piece_type: PieceType | None = None