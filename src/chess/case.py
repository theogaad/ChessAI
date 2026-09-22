from dataclasses import dataclass
from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import verify_type



@dataclass
class Case:
    """Représente une case d'un échiquier.
    
    Attributes:
        position: Position actuelle dans l'échiquier.
        content: Contenu de la case.
    """
    __position: Position
    __content: None | Piece = None


    def __post_init__(self):
        """Vérifie le type des propriétés.
        
        Raises:
            TypeError: Si les propriétés ne sont pas du type attendu.
        """
        verify_type(self.position, Position, "Case(position, content=None)", "position")
        verify_type(self.content, Piece, "Case(position, content=None)", "content", or_none=True)


    def contains_a_piece(
        self, 
        raise_error: bool = False
    ) -> bool:
        """Indique si le contenu de la case est une pièce et lève une erreur si demandé et si cette case de contient pas de pièce.
        
        Args:
            raise_error: Indique si on doit lever une erreur dans le cas ou cette case ne contient pas de pièce.
        
        Raises:
            TypeError: Si ``raise_error`` est à ``True`` et que le contenu de cette case n'est pas une pièce.
        """
        if raise_error and not isinstance(self.content, Piece):
            raise TypeError("contains_a_piece(raise_error=False) La case est censée contenir une pièce.")
        
        return isinstance(self.content, Piece)


    def __repr__(self) -> str:
        """Retourne la représentation textuelle d'une case."""
        return f"Case[{self.position}, {self.content}]"


    def __eq__(
        self, 
        value: object
    ) -> bool:
        """Compare cette case à un objet selon leur position.
        
        La propriété ``content`` n'est pas utilisée dans la comparaison.

        Returns:
            Un booléen indiquant l'égalité entre cette case et l'objet.
        """
        if not isinstance(value, Case):
            return False
        
        return self.position == value.position


    @property
    def position(self) -> Position:
        """Retourne la position actuelle de la case."""
        return self.__position

    @position.setter
    def position(
        self, 
        new_position: Position
    ) -> None:
        """Modifie la position de la case.
        
        Args:
            new_position: Nouvelle position de la case.

        Raises:
            TypeError: Si ``new_position`` n'est pas une instance de ``Position``.
        """
        verify_type(new_position, Position, "position(new_position)", "new_position")

        self.__position = new_position

    @property
    def content(self) -> None | Piece:
        """Retourne le contenu actuel de la Case."""
        return self.__content

    @content.setter
    def content(
        self, 
        new_content: None | Piece
    ) -> None:
        """Modifie le contenu de la case.
        
        Args:
            new_content: Nouveau contenu de la case.
        
        Raises:
            TypeError: Si ``new_content`` n'est ni de type ``None`` ni une instance de ``Piece``.
        """
        verify_type(new_content, Piece, "content(new_content)", "new_content", or_none=True)

        self.__content = new_content