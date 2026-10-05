import pytest

from src.chess_engine.constants import (
    BOARD_SIZE,
    NUMBER_OF_SQUARES,
)
from src.chess_engine.move import Move
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.position import Position
from src.chess_engine.types import (
    CastlingRights,
    Color,
    MoveType,
    PieceType,
)
from src.chess_engine.zobrist import Zobrist


@pytest.fixture
def zobrist() -> Zobrist:
    return Zobrist(seed=42)


@pytest.fixture
def move_executor(zobrist: Zobrist) -> MoveExecutor:
    return MoveExecutor(zobrist)


def initialize_position(position: Position, zobrist: Zobrist) -> None:
    """Initialise le hash Zobrist d'une position."""
    position.zobrist_hash = zobrist.hash_position(position)


def assert_position_matches_fen(
    position: Position,
    fen: str,
    zobrist: Zobrist,
) -> None:
    """Vérifie qu'une position correspond exactement à une FEN."""
    expected = Position(fen)

    assert position.piece_bitboards._bitboards == expected.piece_bitboards._bitboards
    assert position.side_to_move is expected.side_to_move
    assert position.castling_rights == expected.castling_rights
    assert position.en_passant_square == expected.en_passant_square
    assert position.halfmove_clock == expected.halfmove_clock
    assert position.fullmove_number == expected.fullmove_number
    assert position.zobrist_hash == zobrist.hash_position(position)


def test_make_move_normal(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "8/8/8/8/8/8/3P4/4K3 w - - 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(52, 44, MoveType.NORMAL)

    undo_info = move_executor.make_move(position, move)

    assert position.piece_bitboards.get_piece_at(52) is None
    assert position.piece_bitboards.get_piece_at(44) == (
        Color.WHITE,
        PieceType.PAWN,
    )
    assert position.side_to_move is Color.BLACK
    assert position.en_passant_square is None
    assert position.halfmove_clock == 0
    assert position.fullmove_number == 1
    assert undo_info.captured_piece is None


def test_make_move_capture(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "8/8/8/3p4/4P3/8/8/4K3 w - - 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(35, 28, MoveType.NORMAL)

    undo_info = move_executor.make_move(position, move)

    assert position.piece_bitboards.get_piece_at(35) is None
    assert position.piece_bitboards.get_piece_at(28) == (
        Color.WHITE,
        PieceType.PAWN,
    )
    assert undo_info.captured_piece == (
        Color.BLACK,
        PieceType.PAWN,
    )
    assert position.halfmove_clock == 0
    assert position.side_to_move is Color.BLACK


def test_make_move_pawn_double_step(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "8/8/8/8/8/8/3P4/4K3 w - - 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(52, 36, MoveType.NORMAL)

    move_executor.make_move(position, move)

    assert position.en_passant_square == 44
    assert position.side_to_move is Color.BLACK
    assert position.halfmove_clock == 0


def test_make_move_non_pawn_non_capture_increments_halfmove_clock(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "8/8/8/8/8/8/3N4/4K3 w - - 12 1"
    )
    initialize_position(position, zobrist)

    move = Move(52, 42, MoveType.NORMAL)

    move_executor.make_move(position, move)

    assert position.halfmove_clock == 13


def test_make_move_black_increments_fullmove_number(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "4k3/8/8/8/8/8/8/4R3 b - - 0 12"
    )
    initialize_position(position, zobrist)

    move = Move(3, 11, MoveType.NORMAL)

    move_executor.make_move(position, move)

    assert position.fullmove_number == 13
    assert position.side_to_move is Color.WHITE


@pytest.mark.parametrize(
    ("fen", "move", "expected_piece"),
    [
        (
            "4k3/4P3/8/8/8/8/8/4K3 w - - 0 1",
            Move(11, 3, MoveType.NORMAL, PieceType.QUEEN),
            (Color.WHITE, PieceType.QUEEN),
        ),
        (
            "4k3/4P3/8/8/8/8/8/4K3 w - - 0 1",
            Move(11, 3, MoveType.NORMAL, PieceType.ROOK),
            (Color.WHITE, PieceType.ROOK),
        ),
        (
            "4k3/4P3/8/8/8/8/8/4K3 w - - 0 1",
            Move(11, 3, MoveType.NORMAL, PieceType.BISHOP),
            (Color.WHITE, PieceType.BISHOP),
        ),
        (
            "4k3/4P3/8/8/8/8/8/4K3 w - - 0 1",
            Move(11, 3, MoveType.NORMAL, PieceType.KNIGHT),
            (Color.WHITE, PieceType.KNIGHT),
        ),
    ],
)
def test_make_move_promotion(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
    fen: str,
    move: Move,
    expected_piece: tuple[Color, PieceType],
) -> None:
    position = Position(fen)
    initialize_position(position, zobrist)

    move_executor.make_move(position, move)

    assert position.piece_bitboards.get_piece_at(move.start_square) is None
    assert position.piece_bitboards.get_piece_at(move.end_square) == expected_piece
    assert position.halfmove_clock == 0


def test_make_move_en_passant(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(27, 20, MoveType.EN_PASSANT)

    undo_info = move_executor.make_move(position, move)

    assert position.piece_bitboards.get_piece_at(27) is None
    assert position.piece_bitboards.get_piece_at(20) == (
        Color.WHITE,
        PieceType.PAWN,
    )
    assert position.piece_bitboards.get_piece_at(11) is None
    assert undo_info.captured_piece == (
        Color.BLACK,
        PieceType.PAWN,
    )
    assert position.en_passant_square is None
    assert position.halfmove_clock == 0


@pytest.mark.parametrize(
    ("fen", "move", "expected_rights"),
    [
        (
            "4k3/8/8/8/8/8/8/4K2R w K - 0 1",
            Move(59, 57, MoveType.CASTLING),
            CastlingRights.NONE,
        ),
        (
            "4k3/8/8/8/8/8/8/R3K3 w Q - 0 1",
            Move(59, 61, MoveType.CASTLING),
            CastlingRights.NONE,
        ),
        (
            "r3k3/8/8/8/8/8/8/8 b q - 0 1",
            Move(3, 5, MoveType.CASTLING),
            CastlingRights.NONE,
        ),
        (
            "4k2r/8/8/8/8/8/8/8 b k - 0 1",
            Move(3, 1, MoveType.CASTLING),
            CastlingRights.NONE,
        ),
    ],
)
def test_make_move_castling_removes_castling_rights(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
    fen: str,
    move: Move,
    expected_rights: CastlingRights,
) -> None:
    position = Position(fen)
    initialize_position(position, zobrist)

    move_executor.make_move(position, move)

    assert position.castling_rights == expected_rights


def test_make_move_castling_white_kingside(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "4k3/8/8/8/8/8/8/4K2R w K - 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(59, 57, MoveType.CASTLING)

    move_executor.make_move(position, move)

    assert position.piece_bitboards.get_piece_at(57) == (
        Color.WHITE,
        PieceType.KING,
    )
    assert position.piece_bitboards.get_piece_at(58) == (
        Color.WHITE,
        PieceType.ROOK,
    )
    assert position.piece_bitboards.get_piece_at(59) is None
    assert position.piece_bitboards.get_piece_at(56) is None


def test_make_move_castling_white_queenside(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "4k3/8/8/8/8/8/8/R3K3 w Q - 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(59, 61, MoveType.CASTLING)

    move_executor.make_move(position, move)

    assert position.piece_bitboards.get_piece_at(61) == (
        Color.WHITE,
        PieceType.KING,
    )
    assert position.piece_bitboards.get_piece_at(60) == (
        Color.WHITE,
        PieceType.ROOK,
    )
    assert position.piece_bitboards.get_piece_at(59) is None
    assert position.piece_bitboards.get_piece_at(63) is None


def test_make_move_updates_zobrist_hash(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
) -> None:
    position = Position(
        "8/8/8/8/8/8/3P4/4K3 w - - 0 1"
    )
    initialize_position(position, zobrist)

    move = Move(52, 44, MoveType.NORMAL)

    move_executor.make_move(position, move)

    assert position.zobrist_hash == zobrist.hash_position(position)


@pytest.mark.parametrize(
    ("fen", "move"),
    [
        (
            "8/8/8/8/8/8/3P4/4K3 w - - 0 1",
            Move(52, 44, MoveType.NORMAL),
        ),
        (
            "8/8/8/3p4/4P3/8/8/4K3 w - - 0 1",
            Move(35, 27, MoveType.NORMAL),
        ),
        (
            "4k3/4P3/8/8/8/8/8/4K3 w - - 0 1",
            Move(11, 3, MoveType.NORMAL, PieceType.QUEEN),
        ),
        (
            "4k3/8/8/3pP3/8/8/8/4K3 w - d6 0 1",
            Move(27, 19, MoveType.EN_PASSANT),
        ),
        (
            "4k3/8/8/8/8/8/8/4K2R w K - 0 1",
            Move(59, 57, MoveType.CASTLING),
        ),
        (
            "4k3/8/8/8/8/8/8/R3K3 w Q - 0 1",
            Move(59, 61, MoveType.CASTLING),
        ),
    ],
)
def test_undo_move_restores_position(
    move_executor: MoveExecutor,
    zobrist: Zobrist,
    fen: str,
    move: Move,
) -> None:
    position = Position(fen)
    initialize_position(position, zobrist)

    initial_bitboards = position.piece_bitboards._bitboards.copy()
    initial_side_to_move = position.side_to_move
    initial_castling_rights = position.castling_rights
    initial_en_passant_square = position.en_passant_square
    initial_halfmove_clock = position.halfmove_clock
    initial_fullmove_number = position.fullmove_number
    initial_zobrist_hash = position.zobrist_hash

    undo_info = move_executor.make_move(position, move)
    move_executor.undo_move(position, move, undo_info)

    assert position.piece_bitboards._bitboards == initial_bitboards
    assert position.side_to_move is initial_side_to_move
    assert position.castling_rights == initial_castling_rights
    assert position.en_passant_square == initial_en_passant_square
    assert position.halfmove_clock == initial_halfmove_clock
    assert position.fullmove_number == initial_fullmove_number
    assert position.zobrist_hash == initial_zobrist_hash