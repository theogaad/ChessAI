from src.chess.case import Case
from dataclasses import dataclass

@dataclass
class Move:
    start: Case
    end: Case