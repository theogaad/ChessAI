from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import PieceColor, ROOK_VALUE, verify_type



class Rook(Piece):
    """Représente une tour, hérite de la classe abstraite ``Piece``.
        
    Attributes:
        piece_color: Couleur de la pièce.
        has_moved: Indique si la pièce a déjà été déplacée.
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise une tour en utilisant le constructeur de la classe ``Piece``."""
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Détermine les positions atteignables par une tour depuis la position donnée.
        
        Args:
            position: Position de départ.

        Returns:
            Positions qu'une tour peut atteindre depuis la position donnée.

        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        directions: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        list_of_positions: list[Position] = self.get_reachable_sliding_positions_from_position(position, directions)
        
        return list_of_positions


    def get_value(self) -> int:
        """Retourne la valeur d'une tour."""
        return ROOK_VALUE