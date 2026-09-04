import pytest
from src.chess.pieces.piece import PieceColor
from src.chess.pieces.rook import Rook

@pytest.fixture
def white_rook():
    return Rook(PieceColor.WHITE)

@pytest.mark.parametrize("piece_color", PieceColor)
def test_rook_creation(piece_color: PieceColor):
    rook = Rook(piece_color)
    assert rook.piece_color == piece_color
    assert rook.has_moved == False

@pytest.mark.parametrize("piece_color", ["test_wrong_color", 12345678, False])
def test_rook_wrong_creation(piece_color):
    with pytest.raises(ValueError):
        Rook(piece_color)

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7)]), 
    ((4, 4), [(5, 4), (6, 4), (7, 4), (4, 5), (4, 6), (4, 7), (3, 4), (2, 4), (1, 4), (0, 4), (4, 3), (4, 2), (4, 1), (4, 0)]), 
    ((3, 7), [(4, 7), (5, 7), (6, 7), (7, 7), (2, 7), (1, 7), (0, 7), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1), (3, 0)])])
def test_rook_get_moves(white_rook: Rook, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    assert white_rook.get_moves(start[0], start[1]) == expected_end_position