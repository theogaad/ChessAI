from abc import ABC, abstractmethod

from src.chess_engine.game import Game
from src.chess_engine.types import Color, PieceType, EventType


class UI(ABC):
    """Interface abstraite d'une interface utilisateur d'échecs.

    Définit les opérations nécessaires à l'affichage d'une partie
    et à la récupération des coups du joueur humain.
    """

    def __init__(self) -> None:
        self.event: EventType = EventType.NONE

    @abstractmethod
    def display_position(self, game: Game) -> None:
        """Affiche la position actuelle de la partie.

        Args:
            game: Partie dont la position doit être affichée.
        """

    @abstractmethod
    def update_event(self) -> int | None:
        """Met à jour l'attribut event."""

    def piece_to_image_filename(self, color: Color, piece_type: PieceType) -> str:
        """Transforme une couleur et un type de pièce en nom de fichier d'image.
        
        Args:
            color: Couleur de la pièce donnée.
            piece_type: Type de la pièce donnée.
            
        Returns:
            Une chaîne de caractère représentant le nom du fichier de l'image ou 
            unknown.png si la pièce n'est pas reconnue.
        """
        color_str: str = "White" if color is Color.WHITE else "Black"

        match piece_type:
            case PieceType.KING:
                return f"images\\pieces\\{color_str}_King.png"
            case PieceType.QUEEN:
                return f"images\\pieces\\{color_str}_Queen.png"
            case PieceType.ROOK:
                return f"images\\pieces\\{color_str}_Rook.png"
            case PieceType.BISHOP:
                return f"images\\pieces\\{color_str}_Bishop.png"
            case PieceType.KNIGHT:
                return f"images\\pieces\\{color_str}_Knight.png"
            case PieceType.PAWN:
                return f"images\\pieces\\{color_str}_Pawn.png"
            
            case _:
                return "images\\pieces\\unknown.png"