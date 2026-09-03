from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook

BOARD_SIZE = 8

INITIAL_BOARD_CONFIG: list[list[Piece|None]] = \
[[Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
[Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
[None for _ in range(BOARD_SIZE)],
[None for _ in range(BOARD_SIZE)],
[None for _ in range(BOARD_SIZE)],
[None for _ in range(BOARD_SIZE)],
[Pawn(PieceColor.BLACK) for _ in range(BOARD_SIZE)],
[Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]]
