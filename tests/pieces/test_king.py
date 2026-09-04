import pytest
from src.chess.pieces.piece import PieceColor
from src.chess.pieces.king import King

@pytest.fixture
def white_king():
    return King(PieceColor.WHITE)

@pytest.mark.parametrize("piece_color", PieceColor)
def test_king_creation(piece_color: PieceColor):
    king = King(piece_color)
    assert king.piece_color == piece_color
    assert king.has_moved == False

@pytest.mark.parametrize("piece_color", ["test_wrong_color", 12345678, False])
def test_king_wrong_creation(piece_color):
    with pytest.raises(ValueError):
        King(piece_color)

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), [(1, 0), (1, 1), (0, 1)]), 
    ((4, 4), [(5, 4), (5, 5), (4, 5), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3)]), 
    ((3, 7), [(4, 7), (2, 7), (2, 6), (3, 6), (4, 6)])])
def test_king_get_moves(white_king: King, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    assert white_king.get_moves(start[0], start[1]) == expected_end_position