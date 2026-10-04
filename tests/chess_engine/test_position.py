import pytest

from src.chess_engine.constants import INITIAL_FEN
from src.chess_engine.position import Position
from src.chess_engine.types import Color, CastlingRights


def test_position_initialisation() -> None:
    position: Position = Position(INITIAL_FEN)

    assert position.side_to_move is Color.WHITE, "La valeur de l'attribut 'side_to_move' n'est pas celle attendue."
    assert position.castling_rights == (
        CastlingRights.WHITE_KINGSIDE
        | CastlingRights.WHITE_QUEENSIDE
        | CastlingRights.BLACK_KINGSIDE
        | CastlingRights.BLACK_QUEENSIDE
    ), "La valeur de l'attribut 'castling_rights' n'est pas celle attendue."
    assert position.en_passant_square is None, "La valeur de l'attribut 'en_passant_square' n'est pas celle attendue."
    assert position.halfmove_clock == 0, "La valeur de l'attribut 'halfmove_clock' n'est pas celle attendue."
    assert position.fullmove_number == 1, "La valeur de l'attribut 'fullmove_number' n'est pas celle attendue."

def test_position_custom_fen() -> None:
    position: Position = Position(
        "r3k2r/8/8/3pP3/8/8/8/R3K2R b Kq e6 17 42"
    )

    assert position.side_to_move is Color.BLACK, "La valeur de l'attribut 'side_to_move' n'est pas celle attendue."
    assert position.castling_rights == (
        CastlingRights.WHITE_KINGSIDE
        | CastlingRights.BLACK_QUEENSIDE
    ), "La valeur de l'attribut 'castling_rights' n'est pas celle attendue."
    assert position.en_passant_square == 19, "La valeur de l'attribut 'en_passant_square' n'est pas celle attendue."
    assert position.halfmove_clock == 17, "La valeur de l'attribut 'halfmove_clock' n'est pas celle attendue."
    assert position.fullmove_number == 42, "La valeur de l'attribut 'fullmove_number' n'est pas celle attendue."

@pytest.mark.parametrize("string", [
    "",
    "invalid",
    "8/8/8/8/8/8/8/8 x - - 0 1",
    "8/8/8/8/8/8/8/8 w INVALID - 0 1",
    "8/8/8/8/8/8/8/8 w - - -1 1",
])
def test_position_invalid_fen(string: str) -> None:
    with pytest.raises(ValueError):
        Position(string)