from random import shuffle
from src.chess.board import Board
from src.chess.player import Player
from src.chess.profile import Profile
from src.chess.utils import PieceColor, WHITE, BLACK, verify_type

class Game:
    """Représente une partie d'échec."""
    def __init__(
        self, 
        profiles: tuple[Profile, Profile]
    ) -> None:
        self.players: tuple[Player, Player]
        self.board: Board = Board()


    def init_players(self, profiles: tuple[Profile, Profile]) -> None:
        """Initialise les joueurs à partir des profils donnés et en leur attribuant une couleur aléatoire.
        
        Args:
            profiles: Tuple de profils auquel les joueurs sont associés.
            
        Raises:
            TypeError: Si ``profiles`` n'est pas un tuple ou si ses éléments ne sont pas des instances de ``Profile``."""
        verify_type(profiles, tuple, "init_players(profiles)", "profiles")

        for profile in profiles:
            verify_type(profile, Profile, "init_players(profiles)", "profiles[x]")

        colors: list[PieceColor] = [WHITE, BLACK]
        shuffle(colors)
        self.players = (Player(profiles[0], colors[0]), Player(profiles[1], colors[1]))
        