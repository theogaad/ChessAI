from src.chess.pieces.piece import Piece, PieceColor
from src.chess.constants import BOARD_SIZE
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.board import Board
from tests.test_board import test_board_get_color_every_possible_move


board = Board()

initial_configuration: list[list[Piece|None]] = \
    [[Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
    [Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [None for _ in range(BOARD_SIZE)],
    [Pawn(PieceColor.BLACK) for _ in range(BOARD_SIZE)],
    [Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]]
board.fill(initial_configuration)

test_board_get_color_every_possible_move(board, PieceColor.WHITE, [(2, 2), (2, 0), (2, 7), (2, 5), (2, 0), (3, 0), (2, 1), (3, 1), (2, 2), (3, 2), (2, 3), (3, 3), (2, 4), (3, 4), (2, 5), (3, 5), (2, 6), (3, 6), (2, 7), (3, 7)])
