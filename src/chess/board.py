from src.chess.case import Case
from src.chess.constants import BOARD_SIZE
from src.chess.move import Move, SpecialMove
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.utils import is_valid_position



# Classe représentant un plateau d'échecs, contenant une grille (8x8) de cases
class Board:
    def __init__(self) -> None:
        self.grid: list[list[Case]] = [[Case(i, j) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]


    def fill(self, pieces: list[list[Piece | None]]) -> None:
        if len(pieces) != BOARD_SIZE or \
        any(len(row) != BOARD_SIZE for row in pieces) or \
        not all((isinstance(obj, Piece) or obj is None for obj in row) for row in pieces):
            raise ValueError(f"fill(self, pieces) Le tableau de pièces doit être de taille {BOARD_SIZE}x{BOARD_SIZE} contenant des objets de type Piece ou None.")

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece = pieces[i][j]

                if piece is not None:
                    self.grid[i][j].content = piece

                else:
                    self.grid[i][j].content = None


    def get_initial_board_config(self) -> list[list[Piece | None]]:
        return [
                [Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
                [Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
                [None for _ in range(BOARD_SIZE)],
                [None for _ in range(BOARD_SIZE)],
                [None for _ in range(BOARD_SIZE)],
                [None for _ in range(BOARD_SIZE)],
                [Pawn(PieceColor.BLACK) for _ in range(BOARD_SIZE)],
                [Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]
        ]


    def create_initial_board(self) -> None:
        self.fill(self.get_initial_board_config())


    def get_possible_moves(self, line: int, column: int) -> list[Case]:
        is_valid_position(line, column, "get_possible_moves(self, line, column)")

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
        if not isinstance(color, PieceColor):
            raise TypeError("get_color_every_possible_moves(self, color) Le paramètre color doit être du type PieceColor.")
        
        every_possible_moves: list[Case] = []

        for line in self.grid:
            for case in line:
                if case.content is not None and case.content.piece_color == color:
                    for move in self.get_possible_moves(case.line, case.column):
                        every_possible_moves.append(move)

        return every_possible_moves


    def get_attacked_cases(self, color: PieceColor) -> list[Case]:
        if not isinstance(color, PieceColor):
            raise TypeError("get_attacked_cases(self, color) Le paramètre color doit être du type PieceColor.")
        
        attacked_cases: list[Case] = []

        for line in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                case: Case = self.grid[line][column]

                if isinstance(case.content, Piece) and case.content.piece_color == color:
                    if isinstance(case.content, Pawn):
                        pawn_possible_moves: list[tuple[int, int]] = case.content.get_moves(case.line, case.column)

                        for move in pawn_possible_moves:
                            if move[1] != case.column:
                                attacked_cases.append(self.grid[move[0]][move[1]])

                    else:
                        attacked_cases.extend(self.get_possible_moves(case.line, case.column))

        return attacked_cases


    def get_king_case(self, color: PieceColor) -> Case:
        if not isinstance(color, PieceColor):
            raise TypeError("get_king_case(self, color) Le paramètre color doit être du type PieceColor.")
        
        for line in self.grid:
            for case in line:
                if isinstance(case.content, King) and case.content.piece_color == color:
                    return case

        raise Exception("Roi manquant")


    def is_checked(self, color: PieceColor) -> bool:
        if not isinstance(color, PieceColor):
            raise TypeError("is_checked(self, color) Le paramètre color doit être du type PieceColor.")
        
        king_case: Case = self.get_king_case(color)
        every_attacked_cases: list[Case] = self.get_attacked_cases(PieceColor.WHITE if color == PieceColor.BLACK else PieceColor.BLACK)

        return king_case in every_attacked_cases

    def apply_move(self, move: Move) -> None:
        if not isinstance(move, Move):
            raise TypeError("apply_move(self, move) Le paramètre move doit être du type Move.")
        
        if isinstance(move.start.content, (King, Pawn, Rook)) and not move.start.content.has_moved:
            move.start.content.has_moved = True

        move.end.content = move.start.content
        move.start.content = None

        if move.special_move == SpecialMove.EN_PASSANT:
            self.grid[move.start.line][move.end.column].content = None