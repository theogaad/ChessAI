from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import PieceColor, verify_type



class King(Piece):
    """Classe représentant un Roi, descendant de la classe abstraite Piece.
        
    piece_color (private) -- couleur de la pièce
    has_moved (private) -- permet de savoir si la pièce a déjà bougé (par défault False)
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise un King avec une couleur donnée, has_moved est à False à la création."""
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Calcule les positions atteignables par le King en fonction de sa position.
                        
        position -- position de départ
        Renvoie une liste de Position.
        """
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        list_of_positions: list[Position] = []
        directions: list[tuple[int, int]] = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

        for direction in directions:
            list_of_positions.append(Position(position.line + direction[0], position.column + direction[1]))
                
        return list_of_positions