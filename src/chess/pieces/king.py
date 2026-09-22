from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import PieceColor, BOARD_SIZE, KING_VALUE, verify_type



class King(Piece):
    """Représente un roi, hérite de la classe abstraite ``Piece``.
        
    Attributes:
        piece_color: Couleur de la pièce.
        has_moved: Indique si la pièce a déjà été déplacée.
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise un roi en utilisant le constructeur de la classe ``Piece``."""
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Détermine les positions atteignables par un roi depuis la position donnée.
        
        Args:
            position: Position de départ.

        Returns:
            Positions qu'un roi peut atteindre depuis la position donnée.

        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        list_of_positions: list[Position] = []
        directions: list[tuple[int, int]] = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for direction in directions:
            if 0 <= position.line + direction[0] <BOARD_SIZE and 0 <= position.column + direction[1] < BOARD_SIZE:
                list_of_positions.append(Position(position.line + direction[0], position.column + direction[1]))
                
        return list_of_positions


    def get_value(self) -> int:
        """Retourne la valeur d'un roi."""
        return KING_VALUE