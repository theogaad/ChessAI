from dataclasses import dataclass

from src.chess_engine.types import Color, CastlingRights
from src.chess_engine.piece_bitboards import PieceBitboards
from src.chess_engine.position import Position


@dataclass
class FENData:
    """Représente les données extraites d'une chaîne FEN.

    Cette classe regroupe les différentes informations nécessaires à la
    construction d'une position d'échecs à partir d'une chaîne FEN.

    Attributes:
        piece_bitboards: Représentation des pièces sous forme de bitboards.
        side_to_move: Couleur du joueur dont c'est le tour.
        castling_rights: Droits de roque encore disponibles.
        en_passant_square: Indice de la case pouvant être utilisée pour une
            capture en passant, ou None si aucune capture en passant n'est
            disponible.
        halfmove_clock: Nombre de demi-coups écoulés depuis le dernier
            déplacement de pion ou de la dernière capture.
        fullmove_number: Numéro du coup complet dans la partie.
    """

    piece_bitboards: PieceBitboards
    side_to_move: Color
    castling_rights: CastlingRights
    en_passant_square: int | None
    halfmove_clock: int
    fullmove_number: int


def parse_fen(fen: str) -> FENData:
    """Analyse une chaîne FEN et extrait les données de la position.

    Args:
        fen: Chaîne représentant une position au format FEN.

    Returns:
        Les données extraites de la chaîne FEN.

    Raises:
        ValueError: Si la chaîne FEN est invalide.
    """
    # TODO


def to_fen(position: Position) -> str:
    """Convertit une position en chaîne FEN.

    Args:
        position: Position à convertir au format FEN.

    Returns:
        Une chaîne représentant la position au format FEN.
    """
    # TODO