import pytest
from src.chess.pieces.piece import PieceColor
from src.chess.pieces.knight import Knight

@pytest.fixture
def white_knight() -> Knight:
    return Knight(PieceColor.WHITE)

@pytest.mark.parametrize("piece_color", PieceColor)
def test_knight_creation(piece_color: PieceColor) -> None:
    knight = Knight(piece_color)
    assert knight.piece_color == piece_color

@pytest.mark.parametrize("piece_color", ["test_wrong_color", 12345678, False])
def test_knight_wrong_creation(piece_color) -> None:
    with pytest.raises(ValueError):
        Knight(piece_color)

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), [(1, 2), (2, 1)]), 
    ((4, 4), [(5, 6), (6, 5), (3, 6), (2, 5), (5, 2), (6, 3), (3, 2), (2, 3)]), 
    ((3, 7), [(4, 5), (5, 6), (2, 5), (1, 6)])])
def test_knight_get_moves(white_knight: Knight, start: tuple[int, int], expected_end_position: list[tuple[int, int]]) -> None:
    assert white_knight.get_moves(start[0], start[1]) == expected_end_position