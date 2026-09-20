from src.chess.case import Case
from src.chess.constants import BOARD_SIZE
from src.chess.exceptions.chess_error import ChessError
from src.chess.move import Move, SpecialMove
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.position import Position
from src.chess.utils import verify_type



# Classe représentant un plateau d'échecs, contenant une grille (8x8) de cases
class Board:
    def __init__(self) -> None:
        self.grid: list[list[Case]] = [[Case(Position(i, j)) for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]


    def get_initial_board_config(self) -> list[list[Piece | None]]:
            return [
                    [Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), 
                     King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
                    [Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
                    [None for _ in range(BOARD_SIZE)],
                    [None for _ in range(BOARD_SIZE)],
                    [None for _ in range(BOARD_SIZE)],
                    [None for _ in range(BOARD_SIZE)],
                    [Pawn(PieceColor.BLACK) for _ in range(BOARD_SIZE)],
                    [Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), 
                     King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]
            ]


    def fill(self, pieces: list[list[Piece | None]]) -> None:
        if (len(pieces) != BOARD_SIZE or 
            any(len(row) != BOARD_SIZE for row in pieces) or 
            not all((isinstance(obj, Piece) or obj is None for obj in row) for row in pieces)):
            raise ValueError(f"fill(self, pieces) Le tableau de pièces doit être de taille {BOARD_SIZE}x{BOARD_SIZE} contenant des objets de type Piece ou None.")

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                piece = pieces[i][j]

                if piece is not None:
                    self.grid[i][j].content = piece

                else:
                    self.grid[i][j].content = None


    def set_to_initial_board(self) -> None:
        self.fill(self.get_initial_board_config())


    def get_color_all_pieces(self, color: PieceColor) -> list[Piece]:
        verify_type(color, PieceColor, "get_color_all_pieces(self, color)")
        if not isinstance(color, PieceColor):
            raise TypeError("get_color_all_pieces(self, color) Le paramètre color doit être du type PieceColor.")

        pieces: list[Piece] = []

        for row in self.grid:
            for case in row:
                if isinstance(case.content, Piece) and case.content.piece_color == color:
                    pieces.append(case.content)

        return pieces


    def get_piece_position(self, piece: Piece) -> Position:
        if not isinstance(piece, Piece):
            raise TypeError("get_piece_position(self, piece) Le paramètre piece doit être du type Piece.")

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.grid[i][j].content == piece:
                    return Position(i, j)

        raise ChessError("get_piece_position(self, piece) Le paramètre piece doit être une Piece contenue dans le board.")


    def get_reachable_cases_from_position(self, sarting_position: Position) -> list[Case]:
        starting_case: Case = self.grid[sarting_position.line][sarting_position.column]

        if starting_case.content is None:
            return []
        
        reachable_cases: list[Case] = []
        piece: Piece = starting_case.content
        positions: list[Position] = piece.get_reachable_positions(sarting_position)
        forbidden_offset: list[tuple[int, int]] = []

        for position in positions:
            offset_move: tuple[int, int] = ((position.line - sarting_position.line > 0) - (position.line - sarting_position.line < 0), 
                                            (position.column - sarting_position.column > 0) - (position.column - sarting_position.column < 0))

            if offset_move in forbidden_offset and not isinstance(piece, Knight):
                continue

            reachable_case: Case = self.grid[position.line][position.column]

            if reachable_case.content is not None:
                reachable_piece: Piece = reachable_case.content

                if isinstance(piece, Pawn):
                    if abs(offset_move[0]) == abs(offset_move[1]) and reachable_piece.piece_color == piece.piece_color:
                        continue

                    elif abs(offset_move[0]) != abs(offset_move[1]):
                        forbidden_offset.append(offset_move)
                        continue

                elif reachable_piece.piece_color == piece.piece_color:
                    forbidden_offset.append(offset_move)
                    continue

                forbidden_offset.append(offset_move)

            elif isinstance(piece, Pawn) and reachable_case.content is None and abs(offset_move[0]) == abs(offset_move[1]):
                continue

            reachable_cases.append(reachable_case)

        return reachable_cases


    def get_every_reachable_cases_color(self, color: PieceColor) -> list[Case]:
        if not isinstance(color, PieceColor):
            raise TypeError("get_color_every_possible_moves(self, color) Le paramètre color doit être du type PieceColor.")
        
        every_possible_moves: list[Case] = []

        for line in self.grid:
            for case in line:
                if case.content is not None and case.content.piece_color == color:
                    for move in self.get_reachable_cases_from_position(case.position):
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
                        pawn_reachable_positions: list[Position] = case.content.get_reachable_positions(case.position)

                        for position in pawn_reachable_positions:
                            if position.column != case.position.column:
                                attacked_cases.append(self.grid[position.line][position.column])

                    else:
                        attacked_cases.extend(self.get_reachable_cases_from_position(case.position))

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
        
        if isinstance(move.start_case.content, (King, Pawn, Rook)) and not move.start_case.content.has_moved:
            move.start_case.content.has_moved = True

        move.end_case.content = move.start_case.content
        move.start_case.content = None

        if move.special_move == SpecialMove.EN_PASSANT:
            self.grid[move.start_case.position.line][move.end_case.position.column].content = None