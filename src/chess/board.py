from src.chess.case import Case
from src.chess.exceptions.chess_error import ChessError
from src.chess.move import Move
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.position import Position
from src.chess.utils import BOARD_SIZE, WHITE, BLACK, PieceColor, verify_type, get_opposite_color



# Constante représentant l'état initial d'un échiquier.
INITIAL_BOARD: list[list[None | Piece]] = \
[
    [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
    [Pawn(WHITE) for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [Pawn(BLACK) for _ in range(BOARD_SIZE)],
    [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]
]



class Board:
    """Représente un échiquier.
    
    Attributes:
        grid: Grille de 8x8 cases.
    """
    def __init__(self) -> None:
        """Initialise un échiquier avec toutes les cases vides."""
        self.__grid: list[list[Case]] = [[Case(Position(i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]


    def get_reachable_cases_from_position(
        self, 
        position: Position
    ) -> list[Case]:
        """Retourne les cases atteignables par la pièce à la position donnée.
        
        Args:
            position: Position de départ de la pièce.
        
        Returns:
            Liste de toutes les cases que la pièce située à la position donnée peut atteindre.
        
        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_reachable_cases_from_position(position)", "position")

        reachable_cases: list[Case] = []
        
        piece: Piece = self.get_piece(position)
        piece_reachable_cases: list[Case] = [Case(reachable_position) for reachable_position in piece.get_reachable_positions_from_position(position)]

        # Si la pièce est un cavalier ou un roi, il n'y a pas besoin de vérifier les directions.
        if isinstance(piece, (Knight, King)):
            for reachable_case in piece_reachable_cases:
                if not (reachable_case.contains_a_piece() and piece.has_the_same_color(reachable_case.content)):
                    reachable_cases.append(reachable_case)

            return reachable_cases

        # On détermine les différentes directions dans lesquelles la pièce peut aller.
        directions: list[tuple[int, int]] = []
        direction: tuple[int, int]
        for reachable_case in piece_reachable_cases:
            direction = position.get_direction(reachable_case.position)

            if not direction in directions:
                directions.append(direction)

        i: int = 0
        case: Case = piece_reachable_cases[i]

        # Pour chaque ``direction``, on boucle sur les positions atteignables tant que les positions 
        # sont dans la même direction que ``direction``.
        # Ensuite, tant qu'il n'y a aucun obstacle dans la direction ``direction``, on ajoute la cases
        # aux cases atteignables, sinon on passe à la direction suivante.
        for direction in directions:
            case = piece_reachable_cases[i]

            while position.get_direction(case.position) != direction:
                i += 1
                case = piece_reachable_cases[i]

            while i < len(piece_reachable_cases) and position.get_direction(case.position) == direction:
                if isinstance(piece, Pawn):
                    # Si le pion se déplace en diagonale et que la case contient une pièce adverse.
                    if direction[1] != 0 and case.contains_a_piece() and not piece.has_the_same_color(case.content):
                        reachable_cases.append(case)

                    elif direction[1] == 0 and not case.contains_a_piece():
                        reachable_cases.append(case)

                    else:
                        break

                elif not case.contains_a_piece() or not piece.has_the_same_color(case.content):
                    reachable_cases.append(case)
                    i += 1
                    case = piece_reachable_cases[i]

                else:
                    break


        return piece_reachable_cases


    def get_board_value_of_color(
        self, 
        color: PieceColor
    ) -> int:
        """Retourne la valeur de toute les pièce de la couleur donnée.
        
        Raises:
            TypeError: Si ``color`` n'est pas une instance de ``PieceColor``.
        """
        value: int = 0

        for case in self.get_cases_of_piece_type_and_color((Bishop, King, Knight, Pawn, Queen, Rook), color):
            if isinstance(case.content, Piece):
                value += case.content.get_value()

        return value
    

    def apply_move(
        self, 
        move: Move
    ) -> None:
        """Modifie l'échiquier pour appliquer le mouvement donné."""
        move.end_case.content = move.start_case.content
        move.start_case.content = None
        if move.promotion_piece_type:
            move.end_case.content = move.promotion_piece_type(move.moving_piece.piece_color)


    def unapply_move(
        self, 
        move: Move
    ) -> None:
        """Modifie l'échiquier pour annuler l'application du mouvement donné."""
        move.start_case.content = move.moving_piece
        move.end_case.content = move.captured_piece


    def is_check(
        self, 
        color: PieceColor
    ) -> bool:
        """Indique si le roi de la couleur donnée est en échec.
        
        Raises:
            TypeError: Si color n'est pas une instance de PieceColor.
        """
        verify_type(color, PieceColor, "is_check(color)", "color")

        king_case: Case = self.get_cases_of_piece_type_and_color((King,), color)[0]

        return king_case in self.get_attacked_cases_by_color(get_opposite_color(color))


    def get_attacked_cases_by_color(
        self, 
        color: PieceColor
    ) -> list[Case]:
        """Détermine toutes les cases qui sont menacées par les pièce de la couleur donnée.
        
        Pour les pions, les cases menacées sont les cases se trouvant dans leurs diagonales.

        Args:
            color: Couleur à partir de laquelle on détermine les cases menacées.

        Returns:
            Liste de toutes les cases menacées par toutes les pièces de la couleur données.
        
        Raises:
            TypeError: Si ``color`` n'est pas une instance de ``PieceColor``.
        """
        verify_type(color, PieceColor, "get_attacked_cases_by_color(color)", "color")

        attacked_cases_by_color: list[Case] = []

        for case in self.get_cases_of_piece_type_and_color((Bishop, King, Knight, Pawn, Queen, Rook), color):
            if not isinstance(case.content, Pawn):
                attacked_cases_by_color.extend(self.get_reachable_cases_from_position(case.position))
            else:
                for reachable_case in self.get_reachable_cases_from_position(case.position):
                    if reachable_case.position.get_direction(case.position)[1] != 0:
                        attacked_cases_by_color.append(reachable_case)

        return attacked_cases_by_color


    def get_reachable_cases_of_color(
        self, 
        color: PieceColor
    ) -> list[Case]:
        """Détermine toutes les cases atteignables par les pièces de la couleur donnée.
        
        Args:
            color: Couleur des pièces dont on détermine les cases atteignables.

        Returns:
            Liste de toutes les cases atteignables par toutes les pièces de la couleur donnée.

        Raises:
            TypeError: Si color n'est pas une instance de PieceColor.
        """
        verify_type(color, PieceColor, "get_reachable_cases_of_color(color)","color")

        reachable_cases_of_color: list[Case] = []

        for case in self.get_cases_of_piece_type_and_color((Bishop, King, Knight, Pawn, Queen, Rook), color):
            reachable_cases_of_color.extend(self.get_reachable_cases_from_position(case.position))

        return reachable_cases_of_color


    def fill(
        self, 
        new_configuration: list[list[None | Piece]]
    ) -> None:
        """Modifie le contenu de toutes les cases de l'échiquier selon la configuration donnée.
        
        Args:
            new_configuration: Nouvelle configuration de l'échiquier.

        Raises:
            ChessError: Si ``new_configuration`` n'est pas une liste à deux dimensions de taille 8x8.
            TypeError: Si les éléments de ``new_configuration`` ne sont pas du type ``None`` ou des instances de ``Piece``.
        """
        verify_type(new_configuration, list, "fill(new_configuration)", "new_configuration")

        if len(new_configuration) != BOARD_SIZE:
            raise ChessError(f"fill(new_configuration) Le paramètre new_configuration doit être une list de list de None ou Piece de taille {BOARD_SIZE}x{BOARD_SIZE}")

        for new_row in new_configuration:
            verify_type(new_row, list, "fill(new_configuration)", "new_configuration[x]")

            if len(new_row) != BOARD_SIZE:
                raise ChessError(f"fill(new_configuration) Le paramètre new_configuration doit être une list de list de None ou Piece de taille {BOARD_SIZE}x{BOARD_SIZE}")
            
            for obj in new_row:
                verify_type(obj, Piece, "fill(new_configuration)", "new_configuration[x][x]", or_none=True)

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.grid[i][j].content = new_configuration[i][j]


    def get_piece(
        self, 
        position: Position
    ) -> Piece:
        """Retourne la pièce située à la position donnée.
        
        Args:
            position: Position de la pièce recherchée.
            
        Returns:
            La pièce située à la position donnée.

        Raises:
            TypeError: Si la case située à la position donnée ne contient pas de pièce.
        """
        obj: None | Piece = self.get_case_content(position)

        if obj is None:
            raise TypeError("get_piece(position) La case ne contient pas de pièce.")

        return obj


    def get_cases_of_piece_type_and_color(
        self, 
        piece_types: tuple[type[Piece], ...], 
        color: PieceColor
    ) -> list[Case]:
        """Retourne les cases contenant une pièce d'un des types et de la couleur donnés.
        
        Args:
            piece_types: Tuple contenant les types de pièce recherchés.
            color: Couleur des pièces recherchées.
            
        Returns:
            Liste des cases contenant une pièces d'un des types donnés et de la couleur données.

        Raises:
            TypeError: Si ``piece_types`` n'est pas un type hérité de la classe ``Piece``, 
                ou si ``color`` n'est pas une instance de ``PieceColor``.
        """
        if any(piece_type not in [Bishop, King, Knight, Pawn, Queen, Rook] for piece_type in piece_types):
            raise TypeError("get_cases_of_piece_type_and_color(piece_type, color) L'argument' piece_type doit être un tuple de types parmi 'Bishop', 'King', 'Knight', 'Pawn', 'Queen', 'Rook'.")

        verify_type(color, PieceColor, "get_cases_of_piece_type_and_color(piece_type, color)", "color")

        list_of_cases: list[Case] = []

        for row in self.grid:
            for case in row:
                if isinstance(case.content, piece_types) and isinstance(case.content, Piece) and case.content.is_color(color):
                    list_of_cases.append(case)

        return list_of_cases



    def get_case(
        self, 
        position: Position
    ) -> Case:
        """Retourne la case de l'échiquier déterminée à partir de la position donnée."""
        return self.grid[position.line][position.column]


    def get_case_content(
        self, 
        position: Position
    ) -> None | Piece:
        """Retourne le contenu de la case de l'échiquier déterminée à partir de la position donnée."""
        return self.get_case(position).content


    @property
    def grid(self) -> list[list[Case]]:
        """Retourne la grille de cases."""
        return self.__grid

    @grid.setter
    def grid(
        self, 
        new_grid: list[list[Case]]
    ) -> None:
        """Modifie la grille de cases.
        
        Args:
            new_grid: Nouvelle grille de 8x8 cases.
            
        Raises:
            ChessError: Si ``new_grid`` n'est pas une liste à deux dimensions de taille 8x8.
            TypeError: Si les éléments de ``new_grid`` ne sont pas des instances de ``Case``.
        """
        verify_type(new_grid, list, "grid(new_grid)", "new_grid")

        if len(new_grid) != BOARD_SIZE:
            raise ChessError(f"grid(new_grid) Le paramètre new_grid doit être une list de list de Case de taille {BOARD_SIZE}x{BOARD_SIZE}")

        for new_row in new_grid:
            verify_type(new_row, list, "grid(new_grid)", "new_grid[x]")

            if len(new_row) != BOARD_SIZE:
                raise ChessError(f"grid(new_grid) Le paramètre new_grid doit être une list de list de Case de taille {BOARD_SIZE}x{BOARD_SIZE}")
            
            for obj in new_row:
                verify_type(obj, Case, "grid(new_grid)", "new_grid[x][x]")

        self.__grid = new_grid