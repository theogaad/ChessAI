from src.chess_engine.undo_info import UndoInfo
from src.chess_engine.types import Color, PieceType, CastlingRights


def test_undo_info_initialisation() -> None:
    undo_info = UndoInfo(
        captured_piece=None,
        previous_castling_rights=CastlingRights.NONE,
        previous_en_passant_square=None,
        previous_halfmove_clock=0,
        previous_fullmove_number=1,
        previous_zobrist_hash=123456789,
    )

    assert undo_info.captured_piece is None, "La valeur de l'attribut 'captured_piece' n'est pas celle attendue."
    assert undo_info.previous_castling_rights is CastlingRights.NONE, "La valeur de l'attribut 'previous_castling_rights' n'est pas celle attendue."
    assert undo_info.previous_en_passant_square is None, "La valeur de l'attribut 'previous_en_passant_square' n'est pas celle attendue."
    assert undo_info.previous_halfmove_clock == 0, "La valeur de l'attribut 'previous_halfmove_clock' n'est pas celle attendue."
    assert undo_info.previous_fullmove_number == 1, "La valeur de l'attribut 'previous_fullmove_number' n'est pas celle attendue."
    assert undo_info.previous_zobrist_hash == 123456789, "La valeur de l'attribut 'previous_zobrist_hash' n'est pas celle attendue."

def test_undo_info_capture() -> None:
    undo_info = UndoInfo(
        captured_piece=(Color.BLACK, PieceType.KNIGHT),
        previous_castling_rights=(
            CastlingRights.WHITE_KINGSIDE
            | CastlingRights.BLACK_QUEENSIDE
        ),
        previous_en_passant_square=43,
        previous_halfmove_clock=12,
        previous_fullmove_number=27,
        previous_zobrist_hash=987654321,
    )

    assert undo_info.captured_piece == (Color.BLACK, PieceType.KNIGHT), "La valeur de l'attribut 'captured_piece' n'est pas celle attendue."
    assert undo_info.previous_castling_rights == (
        CastlingRights.WHITE_KINGSIDE
        | CastlingRights.BLACK_QUEENSIDE
    ), "La valeur de l'attribut 'previous_castling_rights' n'est pas celle attendue."
    assert undo_info.previous_en_passant_square == 43, "La valeur de l'attribut 'previous_en_passant_square' n'est pas celle attendue."
    assert undo_info.previous_halfmove_clock == 12, "La valeur de l'attribut 'previous_halfmove_clock' n'est pas celle attendue."
    assert undo_info.previous_fullmove_number == 27, "La valeur de l'attribut 'previous_fullmove_number' n'est pas celle attendue."
    assert undo_info.previous_zobrist_hash == 987654321, "La valeur de l'attribut 'previous_zobrist_hash' n'est pas celle attendue."