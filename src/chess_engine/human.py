from queue import Queue

from src.chess_engine.move import Move
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType


class Human(Player):
    """Représente un joueur humain. 
    
    Cette classe implémente l'interface ``Player`` pour un joueur dont le 
    choix des coups est effectué par une couche externe, telle qu'une 
    interface utilisateur. 
    
    Attributes: 
        color: Couleur des pièces contrôlées par le joueur.
        _queue: Queue permettant de communiquer avec l'interface graphique.
    """

    def __init__(self, color: Color, queue: Queue) -> None:
        """Initialise un joueur humain.

        Args:
            color: Couleur des pièces contrôlées par le joueur.
        """
        super().__init__(color)
        self._queue: Queue = queue

    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move | None:
        """Attend et retourne le coup sélectionné par l'utilisateur.
        
        Cette méthode bloque son exécution jusqu'à ce qu'un coup soit fourni 
        via ``self._queue``. La vérification de la légalité du coup relève de la 
        responsabilité de la partie.
        
        Args:
            position: Position actuelle de la partie.
            legal_moves: Liste des coups légaux disponibles.
            
        Returns:
            Le coup sélectionné par l'utilisateur.
        """
        return self._queue.get()

    def ask_for_promotion(self) -> PieceType:
        return PieceType.QUEEN