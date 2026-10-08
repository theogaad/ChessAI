from src.chess_engine.move import Move
from src.chess_engine.position import Position


class AIRequest:
    def __init__(self, position: Position, legal_moves: list[Move], depth: int):
        self.position: Position = position
        self.legal_moves: list[Move] = legal_moves
        self.depth: int = depth