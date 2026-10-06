from abc import ABC, abstractmethod

from src.chess_engine.move import Move
from src.chess_engine.position import Position
from src.chess_engine.types import Color


class Player(ABC):
    """Classe abstraite représentant un joueur d'échecs.

    Cette classe définit l'interface commune aux différents types de joueurs.
    Chaque joueur doit être capable de sélectionner un coup à partir de la
    position actuelle et des coups légaux disponibles.

    Les classes dérivées sont responsables de la manière dont le coup est
    sélectionné. Un joueur humain peut notamment déléguer cette sélection à
    une interface utilisateur, tandis qu'un joueur contrôlé par une IA peut
    utiliser un algorithme de recherche.

    La classe ne dépend d'aucune interface utilisateur ni d'aucun algorithme
    de recherche particulier.

    Attributes:
        color: Couleur des pièces contrôlées par le joueur.
    """

    def __init__(self, color: Color) -> None:
        """Initialise un joueur.

        Args:
            color: Couleur des pièces contrôlées par le joueur.
        """
        self.color: Color = color

    @abstractmethod
    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move:
        """Choisit un coup parmi les coups légaux disponibles.

        Args:
            position: Position actuelle de la partie.
            legal_moves: Liste des coups légaux disponibles.

        Returns:
            Le coup choisi par le joueur.
        """