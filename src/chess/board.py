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
    """Représente un échiquier de 8x8 Case."""
    def __init__(self) -> None:
        self.__grid: list[list[Case]] = [[Case(Position(i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]


    def apply_move(self, move: Move) -> None:
        move.end_case.content = move.start_case.content
        move.start_case.content = None
        if move.promotion_piece_type:
            move.end_case.content = move.promotion_piece_type(move.moving_piece.piece_color)


    def unapply_move(self, move: Move) -> None:
        move.start_case.content = move.moving_piece
        move.end_case.content = move.captured_piece


    def fill(self, new_configuration: list[list[None | Piece]]) -> None:
        verify_type(new_configuration, list, "fill(new_configuration)", "new_configuration")

        if len(new_configuration) != BOARD_SIZE:
            raise ChessError(f"fill(new_configuration) Le paramètre new_configuration doit être une list de list de None ou Piece de taille {BOARD_SIZE}x{BOARD_SIZE}")

        for new_row in new_configuration:
            verify_type(new_row, list, "fill(new_configuration)", "new_configuration[x]")

            if len(new_row) != BOARD_SIZE:
                raise ChessError(f"fill(new_configuration) Le paramètre new_configuration doit être une list de list de None ou Piece de taille {BOARD_SIZE}x{BOARD_SIZE}")
            
            for obj in new_row:
                verify_type(obj, Piece, "fill(new_configuration)", "new_configuration[x][x]", or_none=True)

    def get_case(self, position: Position) -> Case:
        return self.grid[position.line][position.column]


    def get_case_content(self, position: Position) -> None | Piece:
        return self.get_case(position).content
    

    @property
    def grid(self) -> list[list[Case]]:
        return self.__grid

    @grid.setter
    def grid(self, new_grid: list[list[Case]]) -> None:
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