from dataclasses import dataclass
from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import verify_type



# Classe représentant une case d'échecs, contenant sa position et éventuellement une pièce
@dataclass
class Case:
    """Dataclass représentant une case dans un plateau d'échecs.
    
    position (private) -- position de la case dans le plateau
    content (private) -- contenu de la case : vide ou éventuellement une Piece
    """
    __position: Position
    __content: None | Piece = None


    def __post_init__(self):
        """Vérification des types des attributs."""
        verify_type(self.position, Position, "Case(position)", "position")

        if not isinstance(self.content, Piece) and self.content is not None:
            raise TypeError("Case(position, content) Le paramètre content doit être du type None ou Piece.")


    @property
    def position(self) -> Position:
        """Renvoie la position de la case."""
        return self.__position


    @position.setter
    def position(self, new_position: Position):
        """Modifie la position de la case."""
        verify_type(new_position, Position, "position(new_position)", "new_position")

        self.__position = new_position


    @property
    def content(self) -> None | Piece:
        """Renvoie le contenu de la case."""
        return self.__content


    @content.setter
    def content(self, new_content):
        """Modifie le contenu de la case."""
        if not isinstance(new_content, Piece) and new_content is not None:
            raise TypeError("content(new_content) Le paramètre new_content doit être du type None ou Piece.")

        self.__content = new_content