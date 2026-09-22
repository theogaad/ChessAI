from dataclasses import dataclass
from random import choice
from src.chess.board import Board
from src.chess.profile import Profile
from src.chess.utils import PieceColor, WHITE, BLACK, verify_type, get_opposite_color



@dataclass
class Player:
    """Représente un joueur dans une partie d'échec.
    
    Attributes:
        profile: Profil de l'utilisateur associé au joueur.
        color: Couleur du joueur pendant la partie
        board_value: Valeur de toutes les pièces du joueur.
    """
    __profile: Profile
    __color: PieceColor
    __board_value: int = 0


    def __post_init__(self):
        """Vérifie que chaque propriété est du type attendu.
        
        Raises:
            TypeError: Si une des propriétés n'est pas du type attendu.
        """
        verify_type(self.profile, Profile, "Player(profile, color, board_value=0)", "profile")
        verify_type(self.color, PieceColor, "Player(profile, color, board_value=0)", "color")
        verify_type(self.board_value, int, "Player(profile, color, board_value=0)", "board_value")


    def update_board_value(self, board: Board) -> None:
        """Actualise la valeur de la propriété ``board_value`` en fonction des pièces de l'échiquier donné.

        Raises:
            TypeError: Si ``board`` n'est pas une instance de ``Board``.
        """
        verify_type(board, Board, "update_board_value(board)", "board")

        self.board_value = board.get_board_value_of_color(self.color)


    def set_random_color(self, obj: object = None):
        verify_type(obj, Player, "set_random_color(obj=None)", "obj", or_none=True)

        if isinstance(obj, Player):
            self.color = get_opposite_color(obj.color)

        else:
            self.color = choice([WHITE, BLACK])


    @property
    def profile(self) -> Profile:
        """Retourne le profil de l'utilisateur associé à ce joueur."""
        return self.__profile

    @profile.setter
    def profile(self, new_profile: Profile) -> None:
        """Modifie le profil de l'utilisateur associé à ce joueur."""
        verify_type(new_profile, Profile, "profile(new_profile)", "new_profile")

        self.__profile = new_profile

    @property
    def color(self) -> PieceColor:
        """Retourne la couleur du ce joueur."""
        return self.__color

    @color.setter
    def color(self, new_color: PieceColor) -> None:
        """Modifie la couleur de ce joueur."""
        verify_type(new_color, PieceColor, "color(new_color)", "new_color")

        self.__color = new_color

    @property
    def board_value(self) -> int:
        """Retourne la valeur des pièces que possèdent ce joueur."""
        return self.__board_value

    @board_value.setter
    def board_value(self, new_board_value: int) -> None:
        """Modifie la valeur des pièces que possède ce joueur."""
        verify_type(new_board_value, int, "board_value(new_board_value)", "new_board_value")

        self.__board_value = new_board_value