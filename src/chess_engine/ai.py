from queue import Queue

from src.chess_ai.ai_request import AIRequest
from src.chess_engine.move import Move
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import Color


class AI(Player):
    """Représente un joueur AI. 
    
    Cette classe implémente l'interface ``Player`` pour un joueur dont le 
    choix des coups est effectué par une couche externe, telle qu'un moteur
    de recherche des meilleurs coups. 
    
    Attributes: 
        color: Couleur des pièces contrôlées par le joueur.
        _queue: Queue permettant de communiquer avec l'interface graphique.
        _ai_request_queue: Queue permettant de communiquer avec le moteur de recherche.
        _ai_response_queue: Queue permettant de communiquer avec le moteur de recherche.
        _depth: Profondeur de recherche souhaitée pour les algorithmes de recherche.
    """

    def __init__(
        self, 
        color: Color, 
        ai_request_queue: Queue, 
        ai_response_queue: Queue, 
        depth: int
    ) -> None:
        """Initialise un joueur AI.
        
        Args:
            color: Couleur des pièces contrôlées par l'AI.
            ai_request: Queue pour envoyer des requêtes à AIWorker.
            ai_response: Queue pour recevoir des réponses de AIWorker.
            depth: Profondeur de recherche souhaitée pour les algorithmes de recherche.
        """
        super().__init__(color)

        self._ai_request_queue: Queue = ai_request_queue
        self._ai_response_queue: Queue = ai_response_queue
        self._depth: int = depth

    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move | None:
        """Choisit un coup parmi les coups légaux disponibles.

        Args:
            position: Position actuelle de la partie.
            legal_moves: Liste des coups légaux disponibles.

        Returns:
            Le coup choisi par l'ia.
        """
        ai_request: AIRequest = AIRequest(position, legal_moves, self._depth)
        self._ai_request_queue.put(ai_request)
        move: Move | None = self._ai_response_queue.get()

        return move