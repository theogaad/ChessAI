from src.chess_engine.types import Color
from src.chess_engine.position import Position


class AttackGenerator:
    """Génère les cases attaquées par les différentes pièces d'échecs.

    Les attaques des pions, cavaliers et rois sont pré-calculées lors de
    l'initialisation de l'instance, car elles ne dépendent pas de
    l'occupation du plateau.

    Les attaques des pièces glissantes (fous, tours et dames) sont calculées
    dynamiquement en fonction de l'occupation du plateau.

    La classe ne génère pas de coups et ne vérifie pas leur légalité. Une
    attaque représente uniquement les cases contrôlées par une pièce selon
    ses règles de déplacement.

    Attributes:
        _white_pawn_attacks: Table pré-calculée des attaques des pions blancs,
            indexée par case.
        _black_pawn_attacks: Table pré-calculée des attaques des pions noirs,
            indexée par case.
        _knight_attacks: Table pré-calculée des attaques des cavaliers,
            indexée par case.
        _king_attacks: Table pré-calculée des attaques des rois, indexée par
            case.
    """

    def __init__(self) -> None:
        """Initialise le générateur d'attaques.

        Les tables d'attaques des pions, cavaliers et rois sont calculées
        lors de l'initialisation.
        """
        # TODO

    def pawn_attacks(self, square: int, color: Color) -> int:
        """Retourne les cases attaquées par un pion.

        Args:
            square: Indice de la case occupée par le pion.
            color: Couleur du pion.

        Returns:
            Bitboard des cases attaquées par le pion.
        """
        # TODO

    def knight_attacks(self, square: int) -> int:
        """Retourne les cases attaquées par un cavalier.

        Args:
            square: Indice de la case occupée par le cavalier.

        Returns:
            Bitboard des cases attaquées par le cavalier.
        """
        # TODO

    def king_attacks(self, square: int) -> int:
        """Retourne les cases attaquées par un roi.

        Args:
            square: Indice de la case occupée par le roi.

        Returns:
            Bitboard des cases attaquées par le roi.
        """
        # TODO

    def bishop_attacks(self, square: int, occupied: int) -> int:
        """Retourne les cases attaquées par un fou.

        Les cases attaquées sont déterminées en fonction de l'occupation
        actuelle du plateau. Le calcul s'arrête lorsqu'une pièce bloque
        chaque direction de déplacement.

        Args:
            square: Indice de la case occupée par le fou.
            occupied: Bitboard représentant les cases occupées.

        Returns:
            Bitboard des cases attaquées par le fou.
        """
        # TODO

    def rook_attacks(self, square: int, occupied: int) -> int:
        """Retourne les cases attaquées par une tour.

        Les cases attaquées sont déterminées en fonction de l'occupation
        actuelle du plateau. Le calcul s'arrête lorsqu'une pièce bloque
        chaque direction de déplacement.

        Args:
            square: Indice de la case occupée par la tour.
            occupied: Bitboard représentant les cases occupées.

        Returns:
            Bitboard des cases attaquées par la tour.
        """
        # TODO

    def queen_attacks(self, square: int, occupied: int) -> int:
        """Retourne les cases attaquées par une dame.

        Les attaques d'une dame correspondent à l'union de ses attaques
        diagonales et orthogonales.

        Args:
            square: Indice de la case occupée par la dame.
            occupied: Bitboard représentant les cases occupées.

        Returns:
            Bitboard des cases attaquées par la dame.
        """
        # TODO

    def is_square_attacked(
        self,
        position: Position,
        square: int,
        by_color: Color,
    ) -> bool:
        """Détermine si une case est attaquée par une couleur donnée.

        Cette méthode considère les attaques de toutes les pièces de la
        couleur spécifiée présentes sur la position.

        Args:
            position: Position dans laquelle vérifier l'attaque.
            square: Indice de la case à vérifier.
            by_color: Couleur dont les pièces doivent être prises en compte.

        Returns:
            True si la case est attaquée par au moins une pièce de la couleur
            spécifiée, sinon False.
        """
        # TODO