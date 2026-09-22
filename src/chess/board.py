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
from src.chess.utils import BOARD_SIZE, WHITE, BLACK, verify_type



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
    # TODO Ajouter la méthode get_reachable_cases_of_color(self, color).
    # TODO Ajouter la méthode get_attacked_cases_by_color(self, color).
    # TODO Ajouter la méthode get_piece_type_case(self, piece_type, color).
    # TODO Ajouter la méthode is_check(self, color).
    """Représente un échiquier.
    
    Attributes:
        grid: Grille de 8x8 cases.
    """
    def __init__(self) -> None:
        """Initialise un échiquier avec toutes les cases vides."""
        self.__grid: list[list[Case]] = [[Case(Position(i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]


    def get_reachable_cases_from_position(self, position: Position) -> list[Case]:
        # TODO: Ajouter la documentation.
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


    def apply_move(self, move: Move) -> None:
        """Modifie l'échiquier pour appliquer le mouvement donné."""
        move.end_case.content = move.start_case.content
        move.start_case.content = None
        if move.promotion_piece_type:
            move.end_case.content = move.promotion_piece_type(move.moving_piece.piece_color)


    def unapply_move(self, move: Move) -> None:
        """Modifie l'échiquier pour annuler l'application du mouvement donné."""
        move.start_case.content = move.moving_piece
        move.end_case.content = move.captured_piece


    def fill(self, new_configuration: list[list[None | Piece]]) -> None:
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


    def get_case(self, position: Position) -> Case:
        """Retourne la case de l'échiquier déterminée à partir de la position donnée."""
        return self.grid[position.line][position.column]


    def get_case_content(self, position: Position) -> None | Piece:
        """Retourne le contenu de la case de l'échiquier déterminée à partir de la position donnée."""
        return self.get_case(position).content


    def get_piece(self, position: Position) -> Piece:
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


    @property
    def grid(self) -> list[list[Case]]:
        """Retourne la grille de cases."""
        return self.__grid

    @grid.setter
    def grid(self, new_grid: list[list[Case]]) -> None:
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