from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
import pytest

def test_piece_creation_white_king():
    roi = King(PieceColor.WHITE)
    assert roi.piece_color == PieceColor.WHITE

@pytest.mark.parametrize("piece_color", PieceColor)
def test_piece_creation_all_colors(piece_color):
    piece = King(piece_color)
    assert piece.piece_color == piece_color