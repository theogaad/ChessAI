from src.chess_engine.move import Move
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import Color


class Human(Player):
    """Représente un joueur humain.

    Cette classe implémente l'interface ``Player`` pour un joueur dont les
    coups sont sélectionnés par une interaction avec l'utilisateur.

    La classe ne dépend pas directement d'une interface graphique ou d'une
    bibliothèque particulière. La manière dont l'utilisateur sélectionne
    son coup sera définie par une couche externe dédiée à l'interface
    utilisateur.

    Attributes:
        color: Couleur des pièces contrôlées par le joueur.
    """

    def __init__(self, color: Color) -> None:
        """Initialise un joueur humain.

        Args:
            color: Couleur des pièces contrôlées par le joueur.
        """
        # TODO

    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move:
        """Choisit un coup parmi les coups légaux disponibles.

        La sélection du coup est effectuée par l'utilisateur via une
        interface externe.

        Args:
            position: Position actuelle de la partie.
            legal_moves: Liste des coups légaux disponibles.

        Returns:
            Le coup choisi par l'utilisateur.
        """
        # TODO