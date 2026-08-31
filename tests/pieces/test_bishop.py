import pytest
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop

@pytest.fixture
def white_bishop():
    return Bishop(PieceColor.WHITE)

@pytest.mark.parametrize("piece_color", PieceColor)
def test_bishop_creation(piece_color: PieceColor):
    bishop = Bishop(piece_color)
    assert bishop.piece_color == piece_color

@pytest.mark.parametrize("piece_color", ["test_wrong_color", 12345678, False])
def test_bishop_wrong_creation(piece_color):
    with pytest.raises(ValueError):
        Bishop(piece_color)

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]), 
    ((4, 4), [(5, 5), (6, 6), (7, 7), (5, 3), (6, 2), (7, 1), (3, 5), (2, 6), (1, 7), (3, 3), (2, 2), (1, 1), (0, 0)]), 
    ((3, 7), [(4, 6), (5, 5), (6, 4), (7, 3), (2, 6), (1, 5), (0, 4)])])
def test_bishop_get_moves(white_bishop: Bishop, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    assert white_bishop.get_moves(start[0], start[1]) == expected_end_position