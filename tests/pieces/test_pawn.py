import pytest
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.pawn import Pawn

@pytest.fixture
def white_pawn():
    return Pawn(PieceColor.WHITE)

@pytest.fixture
def black_pawn():
    return Pawn(PieceColor.BLACK)

@pytest.mark.parametrize("piece_color", PieceColor)
def test_pawn_creation(piece_color: PieceColor):
    pawn = Pawn(piece_color)
    assert pawn.piece_color == piece_color
    assert pawn.has_moved == False

@pytest.mark.parametrize("piece_color", ["test_wrong_color", 12345678, False])
def test_pawn_wrong_creation(piece_color):
    with pytest.raises(ValueError):
        Pawn(piece_color)

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), [(1, 0), (1, 1), (2, 0)]), 
    ((4, 4), [(5, 4), (5, 5), (5, 3), (6, 4)]), 
    ((3, 7), [(4, 7), (4, 6), (5, 7)]),
    ((7, 7), [])])
def test_white_pawn_get_moves(white_pawn: Pawn, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    assert white_pawn.get_moves(start[0], start[1]) == expected_end_position

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), []), 
    ((4, 4), [(3, 4), (3, 5), (3, 3), (2, 4)]), 
    ((3, 7), [(2, 7), (2, 6), (1, 7)]),
    ((7, 7), [(6, 7), (6, 6), (5, 7)])])
def test_black_pawn_get_moves(black_pawn: Pawn, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    assert black_pawn.get_moves(start[0], start[1]) == expected_end_position

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), [(1, 0), (1, 1)]), 
    ((4, 4), [(5, 4), (5, 5), (5, 3)]), 
    ((3, 7), [(4, 7), (4, 6)]),
    ((7, 7), [])
])
def test_white_pawn_has_moved_get_moves(white_pawn: Pawn, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    white_pawn.has_moved = True
    assert white_pawn.get_moves(start[0], start[1]) == expected_end_position

@pytest.mark.parametrize("start, expected_end_position", [
    ((0, 0), []), 
    ((4, 4), [(3, 4), (3, 5), (3, 3)]), 
    ((3, 7), [(2, 7), (2, 6)]),
    ((7, 7), [(6, 7), (6, 6)])])
def test_black_pawn_has_moved_get_moves(black_pawn: Pawn, start: tuple[int, int], expected_end_position: list[tuple[int, int]]):
    black_pawn.has_moved = True
    assert black_pawn.get_moves(start[0], start[1]) == expected_end_position
