from queue import Queue
from random import choice

from src.chess_ai.ai_request import AIRequest
from src.chess_engine.move import Move


class AIWorker():
    def __init__(self, ai_request: Queue, ai_response: Queue) -> None:
        self._ai_request_queue: Queue = ai_request
        self._ai_response_queue: Queue = ai_response

    def analyse_request(self) -> None:
        ai_request: AIRequest | None = self.get_request()

        if ai_request is None:
            self.respond(ai_request)
            return

        move: Move = choice(ai_request.legal_moves)

        self.respond(move)

    def get_request(self) -> AIRequest | None:
       return self._ai_request_queue.get()

    def respond(self, move: Move | None) -> None:
        self._ai_response_queue.put(move)