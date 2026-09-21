from dataclasses import dataclass
from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import verify_type



@dataclass
class Case:
    """Dataclass représentant une case dans un plateau d'échecs.
    
    position (private) -- position de la case dans le plateau
    content (private) -- contenu de la case : vide ou éventuellement une Piece (par défault None)
    """
    __position: Position
    __content: None | Piece = None


    def __post_init__(self):
        """Vérifie le type des attributs."""
        verify_type(self.position, Position, "Case(position)", "position")

        if not isinstance(self.content, Piece) and self.content is not None:
            raise TypeError("Case(position, content) Le paramètre content doit être du type None ou Piece.")


    def __repr__(self) -> str:
        """Définis la représentation en chaîne de caractères d'une Case."""
        return f"Case[{self.position}, {self.content}]"


    def __eq__(self, value) -> bool:
        return self.position == value.position


    @property
    def position(self) -> Position:
        """Renvoie la position de la Case."""
        return self.__position

    @position.setter
    def position(self, new_position: Position):
        """Modifie la position de la Case."""
        verify_type(new_position, Position, "position(new_position)", "new_position")

        self.__position = new_position

    @property
    def content(self) -> None | Piece:
        """Renvoie le contenu de la Case."""
        return self.__content

    @content.setter
    def content(self, new_content: None | Piece):
        """Modifie le contenu de la Case."""
        verify_type(new_content, Piece, "content(new_content)", "new_content", or_none=True)
        
        self.__content = new_content