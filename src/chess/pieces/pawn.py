from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import PieceColor, BOARD_SIZE, verify_type



class Pawn(Piece):
    """Représente un pion, hérite de la classe abstraite ``Piece``.
        
    Attributes:
        piece_color: Couleur de la pièce.
        has_moved: Indique si la pièce a déjà été déplacée.
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise un pion en utilisant le constructeur de la classe ``Piece``."""
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Détermine les positions atteignables par un pion depuis la position donnée.

        Contrairement aux autres types de pièce, les positions atteignables d'un pion dépendent aussi de sa couleur
        et de l'attribut ``has_moved``.
                
        Args:
            position: Position de départ.

        Returns:
            Positions qu'un pion peut atteindre depuis la position donnée.

        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        list_of_positions: list[Position] = []
        pawn_direction: int = 1 if self.is_white() else -1 # Direction verticale du pion en fonction de sa couleur
        directions: list[tuple[int, int]] = [(1 * pawn_direction, 0), (1 * pawn_direction, 1), (1 * pawn_direction, -1)]

        if not self.has_moved:
            directions.append((2 * pawn_direction, 0))

        for direction in directions:
            if 0 <= position.line + direction[0] <BOARD_SIZE and 0 <= position.column + direction[1] < BOARD_SIZE:
                list_of_positions.append(Position(position.line + direction[0], position.column + direction[1]))

        return list_of_positions