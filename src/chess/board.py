from src.chess.pieces.piece import Piece, PieceColor
from src.chess.case import Case
from src.chess.move import Move
from src.chess.constants import BOARD_SIZE
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook

# Classe représentant un plateau d'échecs, contenant une grille (8x8) de cases
class Board:
    def __init__(self) -> None:
        self.grid: list[list[Case]] = [[Case(i, j) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    def fill(self, pieces: list[list[Piece | None]]) -> None:
        if len(pieces) != BOARD_SIZE or any(
            len(row) != BOARD_SIZE for row in pieces
        ):
            raise ValueError(
                f"Le tableau de pièces doit être de taille {BOARD_SIZE}x{BOARD_SIZE}."
            )
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece = pieces[i][j]
                if piece is not None:
                    self.grid[i][j].content = piece
                else:
                    self.grid[i][j].content = None

    def create_initial_board(self) -> None:
        initial_configuration: list[list[Piece|None]] = \
            [[Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
            [Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
            [None for _ in range(BOARD_SIZE)],
            [None for _ in range(BOARD_SIZE)],
            [None for _ in range(BOARD_SIZE)],
            [None for _ in range(BOARD_SIZE)],
            [Pawn(PieceColor.BLACK) for _ in range(BOARD_SIZE)],
            [Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]]
        self.fill(initial_configuration)

    def get_possible_moves(self, line: int, column: int) -> list[Case]:
        case: Case = self.grid[line][column]
        if case.content is None:
            return []
        
        possible_moves: list[Case] = []
        piece: Piece = case.content
        moves: list[tuple[int, int]] = piece.get_moves(line, column)
        forbidden_offset: list[tuple[int, int]] = []

        for move in moves:
            offset_move: tuple[int, int] = ((move[0] - line > 0) - (move[0] - line < 0), (move[1] - column > 0) - (move[1] - column < 0))
            if offset_move in forbidden_offset and not isinstance(piece, Knight):
                continue
            move_case: Case = self.grid[move[0]][move[1]]

            if move_case.content is not None:
                move_piece: Piece = move_case.content
                if isinstance(piece, Pawn):
                    if abs(offset_move[0]) == abs(offset_move[1]) and move_piece.piece_color == piece.piece_color:
                        continue
                    elif abs(offset_move[0]) != abs(offset_move[1]):
                        forbidden_offset.append(offset_move)
                        continue
                elif move_piece.piece_color == piece.piece_color:
                    forbidden_offset.append(offset_move)
                    continue
                forbidden_offset.append(offset_move)
            elif isinstance(piece, Pawn) and move_case.content is None and abs(offset_move[0]) == abs(offset_move[1]):
                continue
            possible_moves.append(move_case)
        return possible_moves

    def get_color_every_possible_moves(self, color: PieceColor) -> list[Case]:
        every_possible_moves: list[Case] = []
        for line in self.grid:
            for case in line:
                if case.content is not None and case.content.piece_color == color:
                    for move in self.get_possible_moves(case.line, case.column):
                        every_possible_moves.append(move)
        return every_possible_moves

    def get_king_case(self, king_color: PieceColor) -> Case:
        for line in self.grid:
            for case in line:
                if isinstance(case.content, King) and case.content.piece_color == king_color:
                    return case
        raise Exception("Roi manquant")

    def is_checked(self, color: PieceColor) -> bool:
            is_checked: bool = False
            king_case: Case = self.get_king_case(color)
            every_possible_moves = self.get_color_every_possible_moves(PieceColor.WHITE if color == PieceColor.BLACK else PieceColor.BLACK)
            if king_case in every_possible_moves:
                is_checked = True
            return is_checked

    def apply_move(self, move: Move) -> None:
        move.end.content = move.start.content
        move.start.content = None