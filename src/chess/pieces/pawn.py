from src.chess.pieces.piece import Piece, PieceColor
from src.chess.position import Position
from src.chess.utils import verify_type



class Pawn(Piece):
    """Classe représentant un Pion, descendant de la classe abstraite Piece.
        
    piece_color (private) -- couleur de la pièce
    has_moved (private) -- permet de savoir si la pièce a déjà bougé (par défault False)
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise un Pawn avec une couleur donnée, has_moved est à False à la création."""
        super().__init__(color)


    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Calcule les positions atteignables par le Pawn en fonction de sa position, sa couleur et l'attribut has_moved.
                        
        position -- position de départ
        Renvoie une liste de Position.
        """
        verify_type(position, Position, "get_reachable_positions_from_position(position)", "position")

        list_of_positions: list[Position] = []
        pawn_direction: int = 1 if self.piece_color == PieceColor.WHITE else -1 # Direction verticale du Pawn en fonction de sa couleur
        directions: list[tuple[int, int]] = [(1 * pawn_direction, 0), (1 * pawn_direction, 1), (1 * pawn_direction, -1)]

        if not self.has_moved:
            directions.append((2 * pawn_direction, 0))

        for direction in directions:
            list_of_positions.append(Position(position.line + direction[0], position.column + direction[1]))

        return list_of_positions