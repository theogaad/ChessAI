import pytest

from src.chess_engine.history import History
from src.chess_engine.move import Move
from src.chess_engine.types import CastlingRights, Color, MoveType, PieceType
from src.chess_engine.undo_info import UndoInfo


@pytest.fixture
def move() -> Move:
    return Move(
        start_square=59,
        end_square=51,
        move_type=MoveType.NORMAL,
    )


@pytest.fixture
def undo_info() -> UndoInfo:
    return UndoInfo(
        captured_piece=None,
        previous_castling_rights=CastlingRights.NONE,
        previous_en_passant_square=None,
        previous_halfmove_clock=0,
        previous_fullmove_number=1,
        previous_zobrist_hash=123,
    )


@pytest.fixture
def history() -> History:
    return History(initial_zobrist_hash=123)


def test_initialization() -> None:
    history = History(initial_zobrist_hash=123)

    assert history.initial_zobrist_hash == 123
    assert history.moves == []
    assert history.undo_infos == []
    assert history.zobrist_hashes == []


def test_add(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)

    assert history.moves == [move]
    assert history.undo_infos == [undo_info]
    assert history.zobrist_hashes == [456]


def test_add_multiple_entries(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    second_move = Move(
        start_square=51,
        end_square=43,
        move_type=MoveType.NORMAL,
    )
    second_undo_info = UndoInfo(
        captured_piece=(Color.BLACK, PieceType.PAWN),
        previous_castling_rights=CastlingRights.NONE,
        previous_en_passant_square=None,
        previous_halfmove_clock=0,
        previous_fullmove_number=1,
        previous_zobrist_hash=456,
    )

    history.add(move, undo_info, 456)
    history.add(second_move, second_undo_info, 789)

    assert history.moves == [move, second_move]
    assert history.undo_infos == [undo_info, second_undo_info]
    assert history.zobrist_hashes == [456, 789]


def test_remove_last(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)

    history.remove_last()

    assert history.moves == []
    assert history.undo_infos == []
    assert history.zobrist_hashes == []


def test_remove_last_only_removes_last_entry(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    second_move = Move(
        start_square=51,
        end_square=43,
        move_type=MoveType.NORMAL,
    )
    second_undo_info = UndoInfo(
        captured_piece=None,
        previous_castling_rights=CastlingRights.NONE,
        previous_en_passant_square=None,
        previous_halfmove_clock=1,
        previous_fullmove_number=1,
        previous_zobrist_hash=456,
    )

    history.add(move, undo_info, 456)
    history.add(second_move, second_undo_info, 789)

    history.remove_last()

    assert history.moves == [move]
    assert history.undo_infos == [undo_info]
    assert history.zobrist_hashes == [456]


def test_remove_last_empty_history_raises_index_error(
    history: History,
) -> None:
    with pytest.raises(IndexError):
        history.remove_last()


@pytest.mark.parametrize(
    ("searched_hash", "expected_count"),
    [
        (123, 1),
        (456, 0),
    ],
)
def test_count_position_without_moves(
    history: History,
    searched_hash: int,
    expected_count: int,
) -> None:
    assert history.count_position(searched_hash) == expected_count


def test_count_position_includes_initial_position(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)
    history.add(move, undo_info, 789)

    assert history.count_position(123) == 1


def test_count_position_counts_repetitions(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)
    history.add(move, undo_info, 789)
    history.add(move, undo_info, 456)

    assert history.count_position(456) == 2


def test_count_position_counts_initial_position_and_repetition(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)
    history.add(move, undo_info, 123)

    assert history.count_position(123) == 2


def test_get_last_move(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)

    assert history.get_last_move() == move


def test_get_last_move_returns_most_recent_move(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    second_move = Move(
        start_square=51,
        end_square=43,
        move_type=MoveType.NORMAL,
    )

    history.add(move, undo_info, 456)
    history.add(second_move, undo_info, 789)

    assert history.get_last_move() == second_move


def test_get_last_move_empty_history_raises_index_error(
    history: History,
) -> None:
    with pytest.raises(IndexError):
        history.get_last_move()


def test_get_last_undo_info(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)

    assert history.get_last_undo_info() == undo_info


def test_get_last_undo_info_returns_most_recent_info(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    second_undo_info = UndoInfo(
        captured_piece=(Color.BLACK, PieceType.PAWN),
        previous_castling_rights=CastlingRights.NONE,
        previous_en_passant_square=None,
        previous_halfmove_clock=1,
        previous_fullmove_number=1,
        previous_zobrist_hash=456,
    )

    history.add(move, undo_info, 456)
    history.add(move, second_undo_info, 789)

    assert history.get_last_undo_info() == second_undo_info


def test_get_last_undo_info_empty_history_raises_index_error(
    history: History,
) -> None:
    with pytest.raises(IndexError):
        history.get_last_undo_info()


def test_get_last_zobrist_hash(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)

    assert history.get_last_zobrist_hash() == 456


def test_get_last_zobrist_hash_returns_most_recent_hash(
    history: History,
    move: Move,
    undo_info: UndoInfo,
) -> None:
    history.add(move, undo_info, 456)
    history.add(move, undo_info, 789)

    assert history.get_last_zobrist_hash() == 789


def test_get_last_zobrist_hash_empty_history_raises_index_error(
    history: History,
) -> None:
    with pytest.raises(IndexError):
        history.get_last_zobrist_hash()