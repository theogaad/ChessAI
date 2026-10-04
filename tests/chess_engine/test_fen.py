import pytest

from src.chess_engine.constants import INITIAL_FEN
from src.chess_engine.fen import FENData, parse_fen, fen_to_bitboards, fen_to_piece, fen_to_color, fen_to_castling_rights, fen_to_en_passant_square
from src.chess_engine.piece_bitboards import PieceBitboards
from src.chess_engine.types import Color, PieceType, CastlingRights


def test_fen_data_initialisation() -> None:
    piece_bitboards = PieceBitboards((0,) * 12)

    fen_data = FENData(
        piece_bitboards,
        Color.WHITE,
        CastlingRights.WHITE_KINGSIDE | CastlingRights.WHITE_QUEENSIDE |
        CastlingRights.BLACK_KINGSIDE | CastlingRights.BLACK_QUEENSIDE,
        None,
        0,
        1,
    )

    assert fen_data.piece_bitboards is piece_bitboards
    assert fen_data.side_to_move is Color.WHITE
    assert fen_data.castling_rights == (
        CastlingRights.WHITE_KINGSIDE |
        CastlingRights.WHITE_QUEENSIDE |
        CastlingRights.BLACK_KINGSIDE |
        CastlingRights.BLACK_QUEENSIDE
    )
    assert fen_data.en_passant_square is None
    assert fen_data.halfmove_clock == 0
    assert fen_data.fullmove_number == 1

@pytest.mark.parametrize("char, expected", [
    ('K', (Color.WHITE, PieceType.KING)), 
    ('Q', (Color.WHITE, PieceType.QUEEN)), 
    ('R', (Color.WHITE, PieceType.ROOK)), 
    ('B', (Color.WHITE, PieceType.BISHOP)), 
    ('N', (Color.WHITE, PieceType.KNIGHT)), 
    ('P', (Color.WHITE, PieceType.PAWN)), 
    ('k', (Color.BLACK, PieceType.KING)), 
    ('q', (Color.BLACK, PieceType.QUEEN)), 
    ('r', (Color.BLACK, PieceType.ROOK)), 
    ('b', (Color.BLACK, PieceType.BISHOP)), 
    ('n', (Color.BLACK, PieceType.KNIGHT)), 
    ('p', (Color.BLACK, PieceType.PAWN)), 
])
def test_fen_to_piece(char: str, expected: tuple[Color, PieceType]) -> None:
    assert fen_to_piece(char) == expected, "La pièce renvoyée n'est pas celle attendue."

@pytest.mark.parametrize("char", [
    'a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'o', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'O', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '+', '-', '*', '/', '^', '&', '|', ''
])
def test_fen_to_piece_invalid(char: str) -> None:
    with pytest.raises(ValueError):
        fen_to_piece(char)

@pytest.mark.parametrize("string, expected", [
    ('w', Color.WHITE), 
    ('b', Color.BLACK)
])
def test_fen_to_color(string: str, expected: Color) -> None:
    assert fen_to_color(string) == expected, "La couleur renvoyée n'est pas celle attendue."

@pytest.mark.parametrize("string", [
    'a', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'y', 'z', 
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '+', '-', '*', '/', '^', '&', '|', ''
])
def test_fen_to_color_invalid(string: str) -> None:
    with pytest.raises(ValueError):
        fen_to_color(string)

@pytest.mark.parametrize("string, expected", [
    ('-', CastlingRights.NONE), 
    ('K', CastlingRights.WHITE_KINGSIDE), 
    ('Q', CastlingRights.WHITE_QUEENSIDE), 
    ('k', CastlingRights.BLACK_KINGSIDE), 
    ('q', CastlingRights.BLACK_QUEENSIDE), 
    ('KQ', (CastlingRights.WHITE_KINGSIDE | 
            CastlingRights.WHITE_QUEENSIDE)), 
    ('kq', (CastlingRights.BLACK_KINGSIDE | 
            CastlingRights.BLACK_QUEENSIDE)), 
    ('KQkq', (CastlingRights.WHITE_KINGSIDE | 
              CastlingRights.WHITE_QUEENSIDE | 
              CastlingRights.BLACK_KINGSIDE | 
              CastlingRights.BLACK_QUEENSIDE)), 
])
def test_fen_to_castling_rights(string: str, expected: CastlingRights) -> None:
    assert fen_to_castling_rights(string) == expected, "Les droits de roque renvoyées ne sont pas ceux attendus."

@pytest.mark.parametrize("string", [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '+', '*', '/', '^', '&', '|', '', 
    'KK', 'QQ', 'kk', 'qq', 'KQKQ', 'kqkq'
])
def test_fen_to_castling_rights_invalid(string: str) -> None:
    with pytest.raises(ValueError):
        fen_to_castling_rights(string)

@pytest.mark.parametrize("string, expected", [
    ('-', None), 
    ('a2', 55), ('b2', 54), ('c2', 53), ('d2', 52), ('e2', 51), ('f2', 50), ('g2', 49), ('h2', 48), 
    ('a7', 15), ('b7', 14), ('c7', 13), ('d7', 12), ('e7', 11), ('f7', 10), ('g7', 9), ('h7', 8), 
])
def test_fen_to_en_passant_square(string: str, expected: int | None) -> None:
    assert fen_to_en_passant_square(string) == expected, "La case renvoyée n'est pas celle attendue."

@pytest.mark.parametrize("string", [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'l', 'm', 'n', 'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
    '+', '*', '/', '^', '&', '|', '', 
    'a0', 'a9', 'A1', 'A8', 'h0', 'h9', 'H1', 'H8', 'i1', 'i8', 
    '2a', '2h', '7a', '7h'
])
def test_fen_to_en_passant_square_invalid(string: str) -> None:
    with pytest.raises(ValueError):
        fen_to_en_passant_square(string)

def test_fen_to_bitboards_intitial_position() -> None:
    piece_bitboards: PieceBitboards = fen_to_bitboards(INITIAL_FEN.split()[0])

    assert piece_bitboards.bitboards == (
        0x0800000000000000, 
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
        0x000000000000FF00, 
    ), "Les bitboards renvoyés ne sont pas ceux attendus."

def test_fen_to_bitboards_empty_position() -> None:
    piece_bitboards = fen_to_bitboards("8/8/8/8/8/8/8/8")

    assert piece_bitboards.bitboards == (0,) * 12, "Les bitboards renvoyés ne sont pas ceux attendus."
    assert piece_bitboards.occupied == 0, "Les bitboards renvoyés ne sont pas ceux attendus."

@pytest.mark.parametrize("string, square, expected", [
    ("7K/8/8/8/8/8/8/8", 0, (Color.WHITE, PieceType.KING)), 
    ("K7/8/8/8/8/8/8/8", 7, (Color.WHITE, PieceType.KING)), 
    ("8/8/8/8/8/8/8/K7", 63, (Color.WHITE, PieceType.KING)), 
    ("8/8/8/8/8/8/8/7K", 56, (Color.WHITE, PieceType.KING))
])
def test_fen_to_bitboards_square_conversion(string, square, expected) -> None:
    piece_bitboards = fen_to_bitboards(string)

    assert piece_bitboards.get_piece_at(square) == expected, "Les bitboards renvoyés ne sont pas ceux attendus."

@pytest.mark.parametrize("string", [
    "", 
    "8/8/8/8/8/8/8", 
    "8/8/8/8/8/8/8/9", 
    "8/8/8/8/8/8/8/7", 
    "8/8/8/8/8/8/8/9", 
    "8/8/8/8/8/8/8/ABCDEFGH", 
    "8/8/8/8/8/8/8/111111111"
])
def test_fen_to_bitboards_invalid(string) -> None:
    with pytest.raises(ValueError):
        fen_to_bitboards(string)

def test_parse_fen_initial_position() -> None:
    fen_data = parse_fen(INITIAL_FEN)

    assert fen_data.side_to_move is Color.WHITE
    assert fen_data.castling_rights == (
        CastlingRights.WHITE_KINGSIDE
        | CastlingRights.WHITE_QUEENSIDE
        | CastlingRights.BLACK_KINGSIDE
        | CastlingRights.BLACK_QUEENSIDE
    )
    assert fen_data.en_passant_square is None
    assert fen_data.halfmove_clock == 0
    assert fen_data.fullmove_number == 1

def test_parse_fen() -> None:
    fen_data = parse_fen(
        "r3k2r/8/8/3pP3/8/8/8/R3K2R b Kq e6 17 42"
    )

    assert fen_data.side_to_move is Color.BLACK
    assert fen_data.castling_rights == (
        CastlingRights.WHITE_KINGSIDE | CastlingRights.BLACK_QUEENSIDE
    )
    assert fen_data.en_passant_square == 19
    assert fen_data.halfmove_clock == 17
    assert fen_data.fullmove_number == 42

@pytest.mark.parametrize("string", [
    "",
    "8/8/8/8/8/8/8/8",
    "8/8/8/8/8/8/8/8 w",
    "8/8/8/8/8/8/8/8 w - -",
    "8/8/8/8/8/8/8/8 w - - 0",
    "8/8/8/8/8/8/8/8 w - - 0 1 extra", 
    "8/8/8/8/8/8/8/8 w - - -1 1",
    "8/8/8/8/8/8/8/8 w - - 0 0",
    "8/8/8/8/8/8/8/8 w - - abc 1",
    "8/8/8/8/8/8/8/8 w - - 0 abc"
])
def test_parse_fen_invalid(string) -> None:
    with pytest.raises(ValueError):
        parse_fen(string)