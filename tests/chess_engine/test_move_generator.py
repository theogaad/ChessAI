import pytest

from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.move import Move
from src.chess_engine.move_generator import MoveGenerator
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.position import Position
from src.chess_engine.types import Color, MoveType, PieceType
from src.chess_engine.zobrist import Zobrist


@pytest.fixture
def move_generator() -> MoveGenerator:
    """Crée un générateur de coups prêt à être utilisé."""
    return MoveGenerator(
        AttackGenerator(), 
        MoveExecutor(Zobrist(seed=0))
    )


def move_to_tuple(move: Move) -> tuple:
    """Convertit un coup en tuple afin de faciliter les comparaisons."""
    return (
        move.start_square,
        move.end_square,
        move.move_type,
        move.promotion_piece_type,
    )


def moves_to_set(moves: list[Move]) -> set[tuple]:
    """Convertit une liste de coups en ensemble de tuples."""
    return {move_to_tuple(move) for move in moves}


@pytest.mark.parametrize(
    ("fen", "expected_count"),
    [
        # Roi au centre : 8 cases accessibles
        ("8/8/8/3K4/8/8/8/8 w - - 0 1", 8),

        # Roi dans un coin : 3 cases accessibles
        ("7K/8/8/8/8/8/8/8 w - - 0 1", 3),

        # Cavalier au centre
        ("8/8/8/3N4/8/8/8/8 w - - 0 1", 8),

        # Cavalier dans un coin
        ("7N/8/8/8/8/8/8/8 w - - 0 1", 2),

        # Fou au centre
        ("8/8/8/3B4/8/8/8/8 w - - 0 1", 13),

        # Tour au centre
        ("8/8/8/3R4/8/8/8/8 w - - 0 1", 14),

        # Dame au centre
        ("8/8/8/3Q4/8/8/8/8 w - - 0 1", 27),
    ],
)
def test_generate_piece_moves_count(
    move_generator: MoveGenerator,
    fen: str,
    expected_count: int,
) -> None:
    """Vérifie le nombre de coups pseudo-légaux des pièces simples."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    assert len(moves) == expected_count


@pytest.mark.parametrize(
    ("fen", "expected_moves"),
    [
        # Roi e4
        (
            "8/8/8/8/4K3/8/8/8 w - - 0 1",
            {
                (35, 26),
                (35, 27),
                (35, 28),
                (35, 34),
                (35, 36),
                (35, 42),
                (35, 43),
                (35, 44),
            },
        ),

        # Cavalier e4
        (
            "8/8/8/8/4N3/8/8/8 w - - 0 1",
            {
                (35, 18),
                (35, 20),
                (35, 25),
                (35, 29),
                (35, 41),
                (35, 45),
                (35, 50),
                (35, 52),
            },
        ),
    ],
)
def test_generate_king_and_knight_moves(
    move_generator: MoveGenerator,
    fen: str,
    expected_moves: set[tuple[int, int]],
) -> None:
    """Vérifie précisément les déplacements du roi et du cavalier."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    generated = {
        (move.start_square, move.end_square)
        for move in moves
    }

    assert generated == expected_moves


@pytest.mark.parametrize(
    ("fen", "expected_count"),
    [
        # Fou bloqué par un allié
        ("8/8/8/3B4/2P1P3/8/8/8 w - - 0 1", 8),

        # Tour bloquée par des alliés
        ("8/8/8/3R4/3P4/8/3P4/8 w - - 0 1", 11),

        # Dame bloquée par des alliés
        ("8/8/8/3Q4/2P1P3/8/3P4/8 w - - 0 1", 22),

        # Fou pouvant capturer mais pas traverser une pièce ennemie
        ("8/8/2p5/3B4/8/8/8/8 w - - 0 1", 11),
    ],
)
def test_sliding_piece_blockers(
    move_generator: MoveGenerator,
    fen: str,
    expected_count: int,
) -> None:
    """Vérifie la gestion des cases occupées par les pièces glissantes."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    assert len(moves) == expected_count


@pytest.mark.parametrize(
    ("fen", "expected_moves"),
    [
        # Pion blanc e2 : avance simple + double
        (
            "8/8/8/8/8/8/4P3/8 w - - 0 1",
            {(51, 43), (51, 35)},
        ),

        # Pion noir e7 : avance simple + double
        (
            "8/4p3/8/8/8/8/8/8 b - - 0 1",
            {(11, 19), (11, 27)},
        ),

        # Pion blanc e3 avec deux captures
        (
            "8/8/8/8/3p1p2/4P3/8/8 w - - 0 1",
            {(43, 34), (43, 35), (43, 36)},
        ),

        # Pion bloqué
        (
            "8/8/8/8/4p3/4P3/8/8 w - - 0 1",
            set(),
        ),
    ],
)
def test_pawn_moves(
    move_generator: MoveGenerator,
    fen: str,
    expected_moves: set[tuple[int, int]],
) -> None:
    """Vérifie les déplacements, doubles avancées et captures des pions."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    generated = {
        (move.start_square, move.end_square)
        for move in moves
    }

    assert generated == expected_moves


@pytest.mark.parametrize(
    ("fen", "expected_promotion_count"),
    [
        # Promotion sans capture
        ("8/4P3/8/8/8/8/8/8 w - - 0 1", 4),

        # Promotion noire sans capture
        ("8/8/8/8/8/8/4p3/8 b - - 0 1", 4),

        # Promotion avec deux captures
        ("3r1r2/4P3/8/8/8/8/8/8 w - - 0 1", 12),
    ],
)
def test_pawn_promotions(
    move_generator: MoveGenerator,
    fen: str,
    expected_promotion_count: int,
) -> None:
    """Vérifie la génération des différentes promotions."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    promotion_moves = [
        move
        for move in moves
        if move.promotion_piece_type is not None
    ]

    assert len(promotion_moves) == expected_promotion_count

    for move in promotion_moves:
        assert move.promotion_piece_type in {
            PieceType.QUEEN,
            PieceType.ROOK,
            PieceType.BISHOP,
            PieceType.KNIGHT,
        }


@pytest.mark.parametrize(
    ("fen", "expected_castling"),
    [
        # Petit et grand roque blancs
        (
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
            {(59, 57), (59, 61)},
        ),

        # Aucun roque si le roi est en échec
        (
            "r3k2r/8/8/8/8/8/4r3/R3K2R w KQkq - 0 1",
            set(),
        ),

        # Aucun petit roque si f1 est attaquée
        (
            "r3k2r/8/8/8/8/5r2/8/R3K2R w KQkq - 0 1",
            {(59, 61)},
        ),

        # Aucun roque si une case intermédiaire est occupée
        (
            "r3k2r/8/8/8/8/8/8/RN2KB1R w KQkq - 0 1",
            set(),
        ),
    ],
)
def test_castling(
    move_generator: MoveGenerator,
    fen: str,
    expected_castling: set[tuple[int, int]],
) -> None:
    """Vérifie les différentes conditions de génération des roques."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    castling_moves = {
        (move.start_square, move.end_square)
        for move in moves
        if move.move_type is MoveType.CASTLING
    }

    assert castling_moves == expected_castling


@pytest.mark.parametrize(
    ("fen", "expected_en_passant"),
    [
        # Pion blanc e5 capture d6 en passant
        (
            "8/8/8/3pP3/8/8/8/8 w - d6 0 1",
            (27, 20),
        ),

        # Pion noir d4 capture e3 en passant
        (
            "8/8/8/8/3pP3/8/8/8 b - e3 0 1",
            (36, 43),
        ),
    ],
)
def test_en_passant(
    move_generator: MoveGenerator,
    fen: str,
    expected_en_passant: tuple[int, int],
) -> None:
    """Vérifie la génération des captures en passant."""
    position = Position(fen)

    moves = move_generator.generate_pseudo_legal_moves(position)

    en_passant_moves = {
        (move.start_square, move.end_square)
        for move in moves
        if move.move_type is MoveType.EN_PASSANT
    }

    assert en_passant_moves == {expected_en_passant}


@pytest.mark.parametrize(
    "fen",
    [
        # Tour blanche clouée par une tour noire
        "4r1k1/8/8/8/8/8/4R3/4K3 w - - 0 1",

        # Roi blanc en échec par une tour noire
        "4r1k1/8/8/8/8/8/8/4K3 w - - 0 1",

        # Roi noir en échec par une tour blanche
        "4k3/8/8/8/8/8/8/4R1K1 b - - 0 1",
    ],
)
def test_legal_moves_filter_illegal_moves(
    move_generator: MoveGenerator,
    fen: str,
) -> None:
    """Vérifie que les coups laissant le roi en échec sont supprimés."""
    position = Position(fen)

    pseudo_legal_moves = move_generator.generate_pseudo_legal_moves(position)
    legal_moves = move_generator.generate_legal_moves(position)

    assert len(legal_moves) <= len(pseudo_legal_moves)

    for move in legal_moves:
        assert move in pseudo_legal_moves


def test_generate_legal_moves_does_not_modify_position(
    move_generator: MoveGenerator,
) -> None:
    """Vérifie que la génération des coups ne modifie pas la position."""
    fen = "r3k2r/pppq1ppp/2npbn2/8/2B5/2NP1N2/PPPQ1PPP/R3K2R w KQkq - 0 1"
    position = Position(fen)

    initial_fen = fen
    initial_hash = position.zobrist_hash

    move_generator._move_executor._zobrist.hash_position(position)

    move_generator.generate_legal_moves(position)

    assert position.side_to_move is Color.WHITE
    assert position.castling_rights.value == 15
    assert position.en_passant_square is None
    assert position.halfmove_clock == 0
    assert position.fullmove_number == 1
    assert position.zobrist_hash == initial_hash

    # Vérification complète de l'état des pièces via la FEN.
    from src.chess_engine.fen import to_fen

    assert to_fen(position) == initial_fen