from abc import ABC, abstractmethod

from src.chess_engine.game import Game
from src.chess_engine.move import Move


class UI(ABC):
    """Interface abstraite d'une interface utilisateur d'échecs.

    Définit les opérations nécessaires à l'affichage d'une partie
    et à la récupération des coups du joueur humain.
    """

    @abstractmethod
    def display_position(self, game: Game) -> None:
        """Affiche la position actuelle de la partie.

        Args:
            game: Partie dont la position doit être affichée.
        """

    @abstractmethod
    def get_move(self, game: Game) -> Move:
        """Récupère le prochain coup joué par l'utilisateur.

        Args:
            game: Partie en cours.

        Returns:
            Coup choisi par l'utilisateur.
        """