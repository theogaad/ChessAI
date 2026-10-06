import pytest

from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.constants import INITIAL_FEN
from src.chess_engine.game import Game
from src.chess_engine.history import History
from src.chess_engine.move import Move
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.move_generator import MoveGenerator
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import (
    CastlingRights,
    Color,
    DrawReason,
    GameStatus,
    MoveType,
    PieceType,
)
from src.chess_engine.zobrist import Zobrist


class DummyPlayer(Player):
    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move:
        return legal_moves[0]


@pytest.fixture
def zobrist() -> Zobrist:
    return Zobrist(seed=42)


@pytest.fixture
def attack_generator() -> AttackGenerator:
    return AttackGenerator()


@pytest.fixture
def move_executor(zobrist: Zobrist) -> MoveExecutor:
    return MoveExecutor(zobrist)


@pytest.fixture
def move_generator(
    attack_generator: AttackGenerator,
    move_executor: MoveExecutor,
) -> MoveGenerator:
    return MoveGenerator(attack_generator, move_executor)


@pytest.fixture
def white_player() -> DummyPlayer:
    return DummyPlayer(Color.WHITE)


@pytest.fixture
def black_player() -> DummyPlayer:
    return DummyPlayer(Color.BLACK)


@pytest.fixture
def game(
    move_generator: MoveGenerator,
    move_executor: MoveExecutor,
    zobrist: Zobrist,
    white_player: DummyPlayer,
    black_player: DummyPlayer,
) -> Game:
    return Game(
        INITIAL_FEN,
        white_player,
        black_player,
        move_generator,
        move_executor,
        zobrist,
    )


def test_init(game: Game, zobrist: Zobrist) -> None:
    assert game.position.side_to_move is Color.WHITE
    assert game.white_player.color is Color.WHITE
    assert game.black_player.color is Color.BLACK
    assert isinstance(game.history, History)
    assert game.status is GameStatus.ONGOING
    assert game.draw_reason is None
    assert game.position.zobrist_hash == zobrist.hash_position(game.position)
    assert game.history.initial_zobrist_hash == game.position.zobrist_hash


@pytest.mark.parametrize(
    ("side_to_move", "expected_color"),
    [
        (Color.WHITE, Color.WHITE),
        (Color.BLACK, Color.BLACK),
    ],
)
def test_current_player(
    game: Game,
    side_to_move: Color,
    expected_color: Color,
) -> None:
    game.position.side_to_move = side_to_move

    assert game.current_player().color is expected_color


def test_legal_moves(game: Game) -> None:
    legal_moves = game.legal_moves()

    assert len(legal_moves) == 20
    assert all(move in game.legal_moves() for move in legal_moves)


def test_make_move(game: Game) -> None:
    move = Move(
        start_square=52,
        end_square=36,
        move_type=MoveType.NORMAL,
    )

    initial_hash = game.position.zobrist_hash

    game.make_move(move)

    assert game.position.side_to_move is Color.BLACK
    assert game.position.piece_bitboards.get_piece_at(36) == (
        Color.WHITE,
        PieceType.PAWN,
    )
    assert game.position.piece_bitboards.get_piece_at(52) is None

    assert len(game.history.moves) == 1
    assert len(game.history.undo_infos) == 1
    assert len(game.history.zobrist_hashes) == 1

    assert game.position.zobrist_hash != initial_hash
    assert (
        game.history.get_last_zobrist_hash()
        == game.position.zobrist_hash
    )

    assert game.status is GameStatus.ONGOING


def test_make_move_rejects_illegal_move(game: Game) -> None:
    illegal_move = Move(
        start_square=52,
        end_square=43,
        move_type=MoveType.NORMAL,
    )

    initial_position_fen = game.position
    initial_hash = game.position.zobrist_hash

    with pytest.raises(ValueError):
        game.make_move(illegal_move)

    assert game.position.zobrist_hash == initial_hash
    assert len(game.history.moves) == 0
    assert game.position is initial_position_fen


def test_undo_move(game: Game) -> None:
    initial_hash = game.position.zobrist_hash

    move = Move(
        start_square=52,
        end_square=36,
        move_type=MoveType.NORMAL,
    )

    game.make_move(move)
    game.undo_move()

    assert game.position.side_to_move is Color.WHITE
    assert game.position.piece_bitboards.get_piece_at(52) == (
        Color.WHITE,
        PieceType.PAWN,
    )
    assert game.position.piece_bitboards.get_piece_at(36) is None

    assert len(game.history.moves) == 0
    assert len(game.history.undo_infos) == 0
    assert len(game.history.zobrist_hashes) == 0

    assert game.position.zobrist_hash == initial_hash
    assert game.status is GameStatus.ONGOING
    assert game.draw_reason is None


def test_undo_move_without_history_raises(game: Game) -> None:
    with pytest.raises(IndexError):
        game.undo_move()


@pytest.mark.parametrize(
    ("fen", "expected_status", "expected_reason"),
    [
        (
            "5k2/5Q2/6K1/8/8/8/8/8 b - - 0 1",
            GameStatus.CHECKMATE,
            None,
        ),
        (
            "7k/5Q2/7K/8/8/8/8/8 b - - 0 1",
            GameStatus.STALEMATE,
            None,
        ),
        (
            "8/8/8/8/8/8/8/K6k w - - 100 1",
            GameStatus.DRAW,
            DrawReason.FIFTY_MOVES,
        ),
        (
            "8/8/8/8/8/8/2B5/K5k1 w - - 0 1",
            GameStatus.DRAW,
            DrawReason.INSUFFICIENT_MATERIAL,
        ),
        (
            "8/8/8/8/8/8/8/K6k w - - 0 1",
            GameStatus.DRAW,
            DrawReason.INSUFFICIENT_MATERIAL,
        ),
        (
            "8/8/8/8/8/8/b1B5/K5k1 w - - 0 1",
            GameStatus.DRAW,
            DrawReason.INSUFFICIENT_MATERIAL,
        ),
    ],
)
def test_init_status(
    fen: str,
    expected_status: GameStatus,
    expected_reason: DrawReason | None,
    move_generator: MoveGenerator,
    move_executor: MoveExecutor,
    zobrist: Zobrist,
    white_player: DummyPlayer,
    black_player: DummyPlayer,
) -> None:
    game = Game(
        fen,
        white_player,
        black_player,
        move_generator,
        move_executor,
        zobrist,
    )

    assert game.status is expected_status
    assert game.draw_reason is expected_reason


def test_repetition_draw(
    game: Game,
) -> None:
    moves = [
        Move(62, 45, MoveType.NORMAL),
        Move(6, 21, MoveType.NORMAL),
        Move(45, 62, MoveType.NORMAL),
        Move(21, 6, MoveType.NORMAL),
        Move(62, 45, MoveType.NORMAL),
        Move(6, 21, MoveType.NORMAL),
        Move(45, 62, MoveType.NORMAL),
        Move(21, 6, MoveType.NORMAL),
    ]

    for move in moves:
        game.make_move(move)

    assert game.status is GameStatus.DRAW
    assert game.draw_reason is DrawReason.REPETITION
    assert game.history.count_position(game.position.zobrist_hash) >= 3


def test_is_insufficient_material(game: Game) -> None:
    insufficient_material_fens = [
        "8/8/8/8/8/8/8/K6k w - - 0 1",
        "8/8/8/8/8/8/N7/K6k w - - 0 1",
        "8/8/8/8/8/8/2B5/K5k1 w - - 0 1",
        "8/8/8/8/8/8/B1b5/K5k1 w - - 0 1",
    ]

    for fen in insufficient_material_fens:
        game = Game(
            fen,
            game.white_player,
            game.black_player,
            game._move_generator,
            game._move_executor,
            game._zobrist,
        )

        assert game.is_insufficient_material() is True


def test_sufficient_material(game: Game) -> None:
    sufficient_material_fens = [
        "8/8/8/8/8/8/7Q/K6k w - - 0 1",
        "8/8/8/8/8/8/7R/K6k w - - 0 1",
        "8/8/8/8/8/8/7P/K6k w - - 0 1",
    ]

    for fen in sufficient_material_fens:
        position = Position(fen)
        position.zobrist_hash = game._zobrist.hash_position(position)

        test_game = Game(
            fen,
            game.white_player,
            game.black_player,
            game._move_generator,
            game._move_executor,
            game._zobrist,
        )

        assert test_game.is_insufficient_material() is False