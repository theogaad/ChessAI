from dataclasses import dataclass

from src.chess_engine.types import Color, CastlingRights
from src.chess_engine.piece_bitboards import PieceBitboards


@dataclass
class FENData:
    """Représente les données extraites d'une chaîne FEN.

    Attributes:
        piece_bitboards: Représentation des pièces de la position.
        side_to_move: Couleur du joueur dont c'est le tour.
        castling_rights: Droits de roque encore disponibles.
        en_passant_square: Indice de la case pouvant être utilisée pour une
            capture en passant, ou None si aucune capture en passant n'est
            disponible.
        halfmove_clock: Nombre de demi-coups écoulés depuis le dernier
            déplacement de pion ou la dernière capture.
        fullmove_number: Numéro du coup complet dans la partie.
    """

    piece_bitboards: PieceBitboards
    side_to_move: Color
    castling_rights: CastlingRights
    en_passant_square: int | None
    halfmove_clock: int
    fullmove_number: int