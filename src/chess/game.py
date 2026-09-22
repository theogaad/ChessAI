from random import shuffle
from src.chess.board import Board
from src.chess.player import Player
from src.chess.profile import Profile

class Game:
    """Représente une partie d'échec."""
    def __init__(
        self, 
        profiles: tuple[Profile, Profile]
    ) -> None:
        self.board = Board()