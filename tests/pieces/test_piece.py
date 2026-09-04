from src.chess.pieces.piece import PieceColor
from src.chess.pieces.king import King
import pytest

def test_piece_creation_white_king():
    roi = King(PieceColor.WHITE)
    assert roi.piece_color == PieceColor.WHITE

@pytest.mark.parametrize("piece_color", PieceColor)
def test_piece_creation_all_colors(piece_color):
    piece = King(piece_color)
    assert piece.piece_color == piece_color