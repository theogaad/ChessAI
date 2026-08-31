from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.board import Board
from tests.test_board import test_board_get_possible_moves_knight_ennemy_piece
empty_board = Board()
test_board_get_possible_moves_knight_ennemy_piece(empty_board)

board = Board()

white_pawn = Pawn(PieceColor.WHITE)
black_pawn = Pawn(PieceColor.BLACK)

configuration_initiale: list[list[Piece|None]] = \
    [[Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
    [white_pawn for i in range(8)],
    [None for i in range(8)],
    [None for i in range(8)],
    [None for i in range(8)],
    [None for i in range(8)],
    [black_pawn for i in range(8)],
    [Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]]

board.fill(configuration_initiale)