import pytest

from src.chess_engine.piece_bitboards import PieceBitboards, TupleBitboards
from src.chess_engine.types import Color, PieceType


@pytest.fixture
def empty_piece_bitboards() -> PieceBitboards:
    return PieceBitboards((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

@pytest.fixture
def initial_piece_bitboards() -> PieceBitboards:
    return PieceBitboards((0x0800000000000000, 
                           0x1000000000000000, 
                           0x8100000000000000, 
                           0x2400000000000000, 
                           0x4200000000000000, 
                           0x00FF000000000000, 
                           0x0000000000000008, 
                           0x0000000000000010, 
                           0x0000000000000081, 
                           0x0000000000000024, 
                           0x0000000000000042, 
                           0x000000000000FF00))

def test_initialisation() -> None:
    piece_bitboards: PieceBitboards = PieceBitboards((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    assert piece_bitboards.bitboards == (0,) * 12, f"La valeur de tous les bitboards devrait être 0."
    assert piece_bitboards.white_pieces == 0, "La valeur de la propriété _white_piece devrait être 0."
    assert piece_bitboards.black_pieces == 0, "La valeur de la propriété _black_pieces devrait être 0."
    assert piece_bitboards.occupied == 0, "La valeur de la propriété _occupied devrait être 0."

@pytest.mark.parametrize("color, piece_type, square", [
    (Color.WHITE, PieceType.KING, 59),
    (Color.BLACK, PieceType.KING, 3),
    (Color.WHITE, PieceType.ROOK, 63),
    (Color.BLACK, PieceType.ROOK, 0),
    (Color.WHITE, PieceType.PAWN, 49),
    (Color.BLACK, PieceType.PAWN, 14)
])
def test_add_piece(
    empty_piece_bitboards: PieceBitboards, 
    color: Color, 
    piece_type: PieceType, 
    square: int
) -> None:
    empty_piece_bitboards.add_piece(color, piece_type, square)

    assert empty_piece_bitboards.get_bitboard(color, piece_type) & (1 << square) != 0, "La pièce n'a pas été ajoutée."
    assert_invariant_consistency(empty_piece_bitboards)

@pytest.mark.parametrize("color, piece_type, square", [
    (Color.WHITE, PieceType.KING, 59),
    (Color.BLACK, PieceType.KING, 3),
    (Color.WHITE, PieceType.ROOK, 63),
    (Color.BLACK, PieceType.ROOK, 0),
    (Color.WHITE, PieceType.PAWN, 49),
    (Color.BLACK, PieceType.PAWN, 14)
])
def test_remove_piece(
    initial_piece_bitboards: PieceBitboards, 
    color: Color, 
    piece_type: PieceType, 
    square: int
    ) -> None:
    initial_piece_bitboards.remove_piece(color, piece_type, square)
    
    assert initial_piece_bitboards.get_bitboard(color, piece_type) & (1 << square) == 0, "La pièce n'a pas été retirée."
    assert_invariant_consistency(initial_piece_bitboards)

@pytest.mark.parametrize("color, piece_type, start_square, end_square", [
    (Color.WHITE, PieceType.PAWN, 51, 43),
    (Color.WHITE, PieceType.QUEEN, 60, 24),
    (Color.WHITE, PieceType.BISHOP, 58, 37),
    (Color.BLACK, PieceType.PAWN, 11, 27),
    (Color.BLACK, PieceType.QUEEN, 4, 32),
    (Color.BLACK, PieceType.BISHOP, 2, 29),
])
def test_move_piece(
    initial_piece_bitboards: PieceBitboards, 
    color: Color, 
    piece_type: PieceType, 
    start_square: int, 
    end_square: int
) -> None:
    initial_piece_bitboards.move_piece(color, piece_type, start_square, end_square)

    assert initial_piece_bitboards.get_bitboard(color, piece_type) & (1 << start_square) == 0, "La pièce n'a pas été retirée."
    assert initial_piece_bitboards.get_bitboard(color, piece_type) & (1 << end_square) != 0, "La pièce n'a pas été ajoutée."
    assert_invariant_consistency(initial_piece_bitboards)

@pytest.mark.parametrize("square, expected_content", [
    (59, (Color.WHITE, PieceType.KING)), 
    (3, (Color.BLACK, PieceType.KING)), 
    (60, (Color.WHITE, PieceType.QUEEN)), 
    (4, (Color.BLACK, PieceType.QUEEN)), 
    (49, (Color.WHITE, PieceType.PAWN)), 
    (14, (Color.BLACK, PieceType.PAWN)), 
    (38, None), 
    (25, None)
])
def test_get_piece_at(
    initial_piece_bitboards: PieceBitboards, 
    square: int, 
    expected_content: None | tuple[Color, PieceType]
) -> None:
    square_content: None | tuple[Color, PieceType] = initial_piece_bitboards.get_piece_at(square)
    assert square_content == expected_content, "Le contenu de la case n'est pas celui attendu."

@pytest.mark.parametrize("color, piece_type, bitboard_index", [
    (Color.WHITE, PieceType.KING, 0), 
    (Color.WHITE, PieceType.QUEEN, 1), 
    (Color.WHITE, PieceType.PAWN, 5), 
    (Color.BLACK, PieceType.ROOK, 8), 
    (Color.BLACK, PieceType.BISHOP, 9), 
    (Color.BLACK, PieceType.KNIGHT, 10)
])
def test_get_bitboard(
    initial_piece_bitboards: PieceBitboards, 
    color: Color, 
    piece_type: PieceType, 
    bitboard_index: int
) -> None:
    bitboard: int = initial_piece_bitboards.get_bitboard(color, piece_type)
    assert bitboard == initial_piece_bitboards.bitboards[bitboard_index], "Le bitboard obtenu n'est pas le bon."

def test_clear(initial_piece_bitboards: PieceBitboards) -> None:
    initial_piece_bitboards.clear()
    assert initial_piece_bitboards.bitboards == (0,) * 12, f"La valeur de tous les bitboards devrait être 0."
    assert_invariant_consistency(initial_piece_bitboards)

def test_bitboards_returns_tuple(initial_piece_bitboards: PieceBitboards) -> None:
    bitboards: TupleBitboards = initial_piece_bitboards.bitboards
    assert (isinstance(bitboards, tuple) and 
            len(bitboards) == 12 and 
            all(isinstance(bitboard, int) for bitboard in bitboards)), "Le getter ne renvoie pas un tuple de 12 entiers."
    

def assert_invariant_consistency(piece_bitboards: PieceBitboards) -> None:
    white_pieces = 0
    black_pieces = 0

    for piece_type in PieceType:
        white_pieces |= piece_bitboards.get_bitboard(Color.WHITE, piece_type)
        black_pieces |= piece_bitboards.get_bitboard(Color.BLACK, piece_type)

    assert piece_bitboards.white_pieces == white_pieces
    assert piece_bitboards.black_pieces == black_pieces
    assert piece_bitboards.white_pieces & piece_bitboards.black_pieces == 0
    assert piece_bitboards.occupied == piece_bitboards.white_pieces | piece_bitboards.black_pieces