from dataclasses import dataclass

from src.chess_engine.types import Color, PieceType, CastlingRights


@dataclass
class UndoInfo:
    """Contient les informations nécessaires pour annuler un coup.

    Cette classe sauvegarde les informations de la position précédente qui
    peuvent être modifiées lors de l'application d'un coup. Elle est utilisée
    par le mécanisme de ``make_move`` et ``undo_move`` afin de restaurer
    efficacement l'état précédent de la partie.

    Les informations relatives aux bitboards ne sont pas sauvegardées.
    Elles sont restaurées directement à partir du coup annulé.

    Attributes:
        captured_piece: Pièce capturée lors du coup, ou None si aucune pièce
            n'a été capturée.
        previous_castling_rights: Droits de roque disponibles avant
            l'application du coup.
        previous_en_passant_square: Case en passant disponible avant
            l'application du coup, ou None si aucune capture en passant
            n'était possible.
        previous_halfmove_clock: Valeur du compteur de demi-coups avant
            l'application du coup.
        previous_fullmove_number: Numéro du coup complet avant l'application
            du coup.
        previous_zobrist_hash: Valeur du hash Zobrist avant l'application
            du coup.
    """

    captured_piece: tuple[Color, PieceType] | None
    previous_castling_rights: CastlingRights
    previous_en_passant_square: int | None
    previous_halfmove_clock: int
    previous_fullmove_number: int
    previous_zobrist_hash: int