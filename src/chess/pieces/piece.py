from abc import ABC, abstractmethod
from src.chess.position import Position
from src.chess.utils import PieceColor, BOARD_SIZE, verify_type



class Piece(ABC):
    """Classe abstraite représentant une pièce d'échecs.
    
    Attributes:
        piece_color: Couleur de la pièce.
        has_moved: Indique si la pièce a déjà été déplacée.
    """
    def __init__(self, color: PieceColor) -> None:
        """Initialise une pièce avec la couleur donnée.
        
        La propriété ``has_move`` est initialisée à ``False``
    
        Args:
            color: Couleur de la pièce.

        Raises:
            TypeError: Si ``color`` n'est pas une instance de ``PieceColor``.
        """
        verify_type(color, PieceColor, "Piece(color)", "color")
        
        self._piece_color = color
        self._has_moved: bool = False


    @abstractmethod
    def get_reachable_positions_from_position(self, position: Position) -> list[Position]:
        """Détermine les positions atteignables par la pièce depuis la position donnée.
        
        Cette méthode doit être implémentée par chaque classe représentant un type de pièce.

        Args:
            position: Position de départ.

        Returns:
            Positions que la pièce peut atteindre selon son mouvement.
        """
        pass


    def get_reachable_sliding_positions_from_position(
            self, 
            position: Position, 
            directions: list[tuple[int, int]]
        ) -> list[Position]:
        """Détermine les positions atteignables en suivant les directions données.

        Pour chaque direction, les positions sont ajoutées successivement jusqu'à atteindre le bord de l'échiquier.
        
        Args:
            position: Position de départ.
            directions: Directions de déplacement sous forme de couples ``(ligne, colonne)``.

        Returns:
            La liste des positions situées dans les direction données jusqu'au bord de l'échiquier.

        Raises:
            TypeError: Si ``position`` ou ``directions`` ne respectent pas le type attendu,
                ou si une direction n'est pas un tuple de 2 entiers.
        """
        verify_type(position, Position, "get_sliding_positions(position, directions)", "position")
        verify_type(directions, list, "get_sliding_positions(position, directions)", "offsets")

        list_of_positions: list[Position] = []

        for direction in directions:
            verify_type(direction, tuple, "get_reachable_sliding_positions_from_position(position, directions)", "directions[x]")

            if len(direction) != 2:
                raise TypeError("get_reachable_sliding_positions_from_position(position, directions) Le paramètre directions[x] doit être un tuple contenant exactement 2 entiers.")
            
            for obj in direction:
                verify_type(obj, int, "get_reachable_sliding_positions_from_position(position, directions)", "directions[x][x]")

            i = 1
            
            while 0 <= position.line + direction[0] * i < BOARD_SIZE and 0 <= position.column + direction[1] * i < BOARD_SIZE:
                list_of_positions.append(Position(position.line + direction[0] * i, position.column + direction[1] * i))
                i += 1

        return list_of_positions


    def is_white(self) -> bool:
        """Indique si la couleur de la pièce est blanche."""
        return self.piece_color == PieceColor.WHITE


    def __repr__(self) -> str:
        """Retourne la représentation textuelle d'une pièce."""
        return f"{type(self).__name__}[color: {self.piece_color.value}, has_moved: {self.has_moved}]"


    def __eq__(self, value: object) -> bool:
        """Compare cette pièce à un objet selon leur type et leur couleur.
        
        L'état ``has_moved`` n'est pas pris en compte dans la comparaison.

        Args:
            value: Objet auquel cette pièce est comparée.

        Returns:
            Un booléen indiquant si cette pièce et l'objet ont le même type et la même couleur.
        """
        if not isinstance(value, Piece):
            return False

        return type(self) is type(value) and self.piece_color == value.piece_color


    @property
    def piece_color(self) -> PieceColor:
        """Retourne la couleur actuelle de la pièce."""
        return self._piece_color

    @piece_color.setter
    def piece_color(self, new_piece_color: PieceColor) -> None:
        """Modifie la couleur de la pièce après avoir vérifié son type.
        
        Args:
            new_piece_color: Nouvelle couleur de la pièce.
            
        Raises:
            TypeError: Si ``new_piece_color`` n'est pas une instance de ``PieceColor``.
        """
        verify_type(new_piece_color, PieceColor, "piece_color(new_piece_color)", "new_piece_color")

        self._piece_color = new_piece_color

    @property
    def has_moved(self) -> bool:
        """Indique si la pièce a déjà été déplacée."""
        return self._has_moved

    @has_moved.setter
    def has_moved(self, new_has_moved: bool) -> None:
        """Modifie l'état indiquant si la pièce a déjà été déplacée.
        
        Args:
            new_has_moved: Nouvel état indiquant si la pièce a déjà été déplacée.

        Raises:
            TypeError: Si ``new_has_moved`` n'est pas un booléen.
        """
        verify_type(new_has_moved, bool, "has_moved(new_has_moved)", "new_has_moved")

        self._has_moved = new_has_moved