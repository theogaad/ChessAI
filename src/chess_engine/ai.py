from queue import Queue

from src.chess_ai.ai_request import AIRequest
from src.chess_engine.move import Move
from src.chess_engine.player import Player
from src.chess_engine.position import Position


class AI(Player):
    def __init__(self, color, ai_request: Queue, ai_response: Queue, depth: int):
        super().__init__(color)

        self._ai_request_queue: Queue = ai_request
        self._ai_response_queue: Queue = ai_response
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