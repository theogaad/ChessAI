from random import choice

from src.chess_ai.ai_request import AIRequest
from src.chess_engine.move import Move


class Search:
    def __init__(self):
        pass

    def find_best_move(self, ai_request: AIRequest) -> Move | None:
        if len(ai_request.legal_moves) == 0:
            return None

        return choice(ai_request.legal_moves)