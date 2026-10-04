import pytest

from src.chess_engine.move import Move
from src.chess_engine.types import PieceType, MoveType


def test_move_initialisation() -> None:
    move = Move(
        start_square=59,
        end_square=43,
        move_type=MoveType.NORMAL,
    )

    assert move.start_square == 59, "La valeur de l'attribut 'start_square' n'est pas celle attendue."
    assert move.end_square == 43, "La valeur de l'attribut 'end_square' n'est pas celle attendue."
    assert move.move_type is MoveType.NORMAL, "La valeur de l'attribut 'move_type' n'est pas celle attendue."
    assert move.promotion_piece_type is None, "La valeur de l'attribut 'promotion_piece_type' n'est pas celle attendue."

def test_move_promotion() -> None:
    move = Move(
        start_square=15,
        end_square=7,
        move_type=MoveType.NORMAL,
        promotion_piece_type=PieceType.QUEEN,
    )

    assert move.start_square == 15, "La valeur de l'attribut 'start_square' n'est pas celle attendue."
    assert move.end_square == 7, "La valeur de l'attribut 'end_square' n'est pas celle attendue."
    assert move.move_type is MoveType.NORMAL, "La valeur de l'attribut 'move_type' n'est pas celle attendue."
    assert move.promotion_piece_type is PieceType.QUEEN, "La valeur de l'attribut 'promotion_piece_type' n'est pas celle attendue."

@pytest.mark.parametrize("move_1, move_2, is_equal", [
    (Move(59, 43, MoveType.NORMAL), Move(59, 43, MoveType.NORMAL), True), 
    (Move(59, 43, MoveType.CASTLING), Move(59, 43, MoveType.CASTLING), True), 
    (Move(59, 43, MoveType.EN_PASSANT), Move(59, 43, MoveType.EN_PASSANT), True), 
    (Move(59, 43, MoveType.NORMAL), Move(58, 43, MoveType.NORMAL), False), 
    (Move(59, 43, MoveType.NORMAL), Move(59, 42, MoveType.NORMAL), False), 
    (Move(59, 43, MoveType.NORMAL), Move(59, 43, MoveType.CASTLING), False), 
    (Move(59, 43, MoveType.NORMAL), Move(59, 43, MoveType.EN_PASSANT), False), 
])
def test_move_equality(move_1: Move, move_2: Move, is_equal: bool) -> None:
    assert (move_1 == move_2) == is_equal, "L'égalité des deux Move n'est pas celle attendue."