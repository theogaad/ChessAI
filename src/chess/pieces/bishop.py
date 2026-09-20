from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position
from src.chess.utils import verify_type



class Bishop(Piece):
    """Classe représentant un Fou, descendant de la classe abstraite Piece.
    
    piece_color (private) -- couleur de la pièce
    has_moved (private) -- permet de savoir si la pièce a déjà bougé
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise un Bishop avec une couleur donnée, has_moved est à False à la création."""
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Calcule les positions atteignables par la Piece en fonction de son type et de sa position.
                
        position -- position de départ
        Renvoie une liste de Position.
        """
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        directions: list[tuple[int, int]] = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        list_of_positions: list[Position] = self.get_reachable_sliding_positions_from_position(position, directions)
        
        return list_of_positions