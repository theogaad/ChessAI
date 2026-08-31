from src.chess.pieces.piece import Piece
from src.chess.case import Case
from src.chess.constants import BOARD_SIZE
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn

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