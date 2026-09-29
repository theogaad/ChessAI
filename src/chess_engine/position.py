from src.chess_engine.types import Color, CastlingRights
from src.chess_engine.piece_bitboards import PieceBitboards


class Position:
    """Représente l'état d'une position d'échecs.

    Une position contient l'état des pièces ainsi que les informations
    nécessaires à la gestion des règles et à la génération des coups.

    Les attributs de la classe sont mutables afin de permettre la
    modification directe de la position lors de l'application et de
    l'annulation des coups.

    Attributes:
        piece_bitboards: Représentation des pièces sous forme de bitboards.
        side_to_move: Couleur du joueur dont c'est le tour.
        castling_rights: Droits de roque encore disponibles.
        en_passant_square: Indice de la case pouvant être utilisée pour une
            capture en passant, ou None si aucune capture en passant n'est
            disponible.
        halfmove_clock: Nombre de demi-coups écoulés depuis le dernier
            déplacement de pion ou de la dernière capture.
        fullmove_number: Numéro du coup complet dans la partie. Commence à 1
            et est incrémenté après chaque coup des Noirs.

    """

    def __init__(self, fen: str) -> None:
        """Initialise une position à partir d'une chaîne FEN.

        La chaîne FEN est utilisée pour initialiser l'ensemble des attributs
        de la position.

        Args:
            fen: Chaîne représentant la position au format FEN.
        """
        # TODO