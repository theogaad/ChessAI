from src.chess.move import Move, SpecialMove
from src.chess.case import Case

def test_move_creation() -> None:
    start_case: Case = Case(0, 0)
    end_case: Case = Case(0, 1)
    move: Move = Move(start_case, end_case)
    assert move.start == start_case
    assert move.end == end_case
    assert move.special_move == SpecialMove.NONE