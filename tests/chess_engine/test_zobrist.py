import pytest

from src.chess_engine.constants import (
    BOARD_SIZE,
    DIFFERENT_PIECES_NUMBER,
    NUMBER_OF_SQUARES,
)
from src.chess_engine.fen import fen_to_bitboards
from src.chess_engine.position import Position
from src.chess_engine.types import CastlingRights, Color, PieceType
from src.chess_engine.zobrist import Zobrist


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def create_zobrist(seed: int = 42) -> Zobrist:
    """Crée une instance de Zobrist avec un seed déterministe."""
    return Zobrist(seed=seed)


def create_empty_position(
    side_to_move: str = "w",
    castling_rights: str = "-",
    en_passant_square: str = "-",
) -> Position:
    """Crée une position vide avec les paramètres indiqués."""
    return Position(
        f"8/8/8/8/8/8/8/8 "
        f"{side_to_move} {castling_rights} {en_passant_square} 0 1"
    )


# ---------------------------------------------------------------------------
# Initialization
# ---------------------------------------------------------------------------


def test_initialization_piece_keys_dimensions() -> None:
    zobrist = create_zobrist()

    assert len(zobrist._piece_keys) == DIFFERENT_PIECES_NUMBER, (
        "Le nombre de groupes de clés de pièces doit être égal "
        "au nombre de pièces différentes."
    )

    assert all(
        len(piece_keys) == NUMBER_OF_SQUARES
        for piece_keys in zobrist._piece_keys
    ), (
        "Chaque groupe de clés de pièces doit contenir une clé "
        "pour chacune des 64 cases."
    )


def test_initialization_castling_keys_dimensions() -> None:
    zobrist = create_zobrist()

    assert len(zobrist._castling_keys) == 4, (
        "Il doit y avoir une clé Zobrist pour chacun des quatre droits de roque."
    )


def test_initialization_en_passant_keys_dimensions() -> None:
    zobrist = create_zobrist()

    assert len(zobrist._en_passant_keys) == BOARD_SIZE * 2, (
        "Il doit y avoir 16 clés pour les cases d'en passant "
        "des rangées 3 et 6."
    )


def test_initialization_keys_are_64_bit_integers() -> None:
    zobrist = create_zobrist()

    all_keys = (
        [
            key
            for piece_keys in zobrist._piece_keys
            for key in piece_keys
        ]
        + [zobrist._side_to_move_key]
        + zobrist._castling_keys
        + zobrist._en_passant_keys
    )

    assert all(isinstance(key, int) for key in all_keys), (
        "Toutes les clés Zobrist doivent être représentées par des entiers."
    )

    assert all(0 <= key < (1 << NUMBER_OF_SQUARES) for key in all_keys), (
        "Toutes les clés Zobrist doivent être des entiers non signés "
        "sur 64 bits."
    )


@pytest.mark.parametrize("seed", [0, 1, 42, 1234, 999999])
def test_same_seed_generates_same_keys(seed: int) -> None:
    first = Zobrist(seed=seed)
    second = Zobrist(seed=seed)

    assert first._piece_keys == second._piece_keys, (
        f"Le seed {seed} doit produire exactement les mêmes clés de pièces."
    )

    assert first._side_to_move_key == second._side_to_move_key, (
        f"Le seed {seed} doit produire exactement la même clé de changement "
        "de joueur."
    )

    assert first._castling_keys == second._castling_keys, (
        f"Le seed {seed} doit produire exactement les mêmes clés de roque."
    )

    assert first._en_passant_keys == second._en_passant_keys, (
        f"Le seed {seed} doit produire exactement les mêmes clés d'en passant."
    )


@pytest.mark.parametrize(
    ("first_seed", "second_seed"),
    [
        (0, 1),
        (1, 2),
        (42, 43),
        (123, 456),
        (999, 1000),
    ],
)
def test_different_seeds_generate_different_keys(
    first_seed: int,
    second_seed: int,
) -> None:
    first = Zobrist(seed=first_seed)
    second = Zobrist(seed=second_seed)

    assert first._piece_keys != second._piece_keys, (
        f"Les seeds {first_seed} et {second_seed} doivent normalement "
        "produire des clés de pièces différentes."
    )


# ---------------------------------------------------------------------------
# piece_key
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("color", list(Color))
@pytest.mark.parametrize("piece_type", list(PieceType))
@pytest.mark.parametrize("square", range(NUMBER_OF_SQUARES))
def test_piece_key_returns_correct_key(
    color: Color,
    piece_type: PieceType,
    square: int,
) -> None:
    zobrist = create_zobrist()

    expected_index = color.value * len(PieceType) + piece_type.value
    expected_key = zobrist._piece_keys[expected_index][square]

    assert zobrist.piece_key(color, piece_type, square) == expected_key, (
        f"La clé de {color.name} {piece_type.name} sur la case {square} "
        "doit correspondre à la clé stockée dans le tableau."
    )


# ---------------------------------------------------------------------------
# side_to_move_key
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seed", [0, 1, 42, 1234, 999999])
def test_side_to_move_key_returns_stored_key(seed: int) -> None:
    zobrist = create_zobrist(seed)

    assert zobrist.side_to_move_key() == zobrist._side_to_move_key, (
        f"La clé de changement de joueur doit être celle générée avec "
        f"le seed {seed}."
    )


# ---------------------------------------------------------------------------
# castling_key
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("castling_rights", "expected_indices"),
    [
        (CastlingRights.NONE, []),
        (CastlingRights.WHITE_KINGSIDE, [0]),
        (CastlingRights.WHITE_QUEENSIDE, [1]),
        (CastlingRights.BLACK_KINGSIDE, [2]),
        (CastlingRights.BLACK_QUEENSIDE, [3]),
        (CastlingRights.WHITE_KINGSIDE | CastlingRights.WHITE_QUEENSIDE, [0, 1]),
        (CastlingRights.WHITE_KINGSIDE | CastlingRights.BLACK_KINGSIDE, [0, 2]),
        (CastlingRights.WHITE_KINGSIDE | CastlingRights.BLACK_QUEENSIDE, [0, 3]),
        (CastlingRights.WHITE_QUEENSIDE | CastlingRights.BLACK_KINGSIDE, [1, 2]),
        (CastlingRights.WHITE_QUEENSIDE | CastlingRights.BLACK_QUEENSIDE, [1, 3]),
        (CastlingRights.BLACK_KINGSIDE | CastlingRights.BLACK_QUEENSIDE, [2, 3]),
        (
            CastlingRights.WHITE_KINGSIDE
            | CastlingRights.WHITE_QUEENSIDE
            | CastlingRights.BLACK_KINGSIDE,
            [0, 1, 2],
        ),
        (
            CastlingRights.WHITE_KINGSIDE
            | CastlingRights.WHITE_QUEENSIDE
            | CastlingRights.BLACK_QUEENSIDE,
            [0, 1, 3],
        ),
        (
            CastlingRights.WHITE_KINGSIDE
            | CastlingRights.BLACK_KINGSIDE
            | CastlingRights.BLACK_QUEENSIDE,
            [0, 2, 3],
        ),
        (
            CastlingRights.WHITE_QUEENSIDE
            | CastlingRights.BLACK_KINGSIDE
            | CastlingRights.BLACK_QUEENSIDE,
            [1, 2, 3],
        ),
        (
            CastlingRights.WHITE_KINGSIDE
            | CastlingRights.WHITE_QUEENSIDE
            | CastlingRights.BLACK_KINGSIDE
            | CastlingRights.BLACK_QUEENSIDE,
            [0, 1, 2, 3],
        ),
    ],
)
def test_castling_key_combines_rights_with_xor(
    castling_rights: CastlingRights,
    expected_indices: list[int],
) -> None:
    zobrist = create_zobrist()

    expected_key = 0
    for index in expected_indices:
        expected_key ^= zobrist._castling_keys[index]

    assert zobrist.castling_key(castling_rights) == expected_key, (
        f"Les droits de roque {castling_rights} doivent produire la combinaison "
        "XOR des clés correspondant aux droits actifs."
    )


def test_castling_key_none_is_zero() -> None:
    zobrist = create_zobrist()

    assert zobrist.castling_key(CastlingRights.NONE) == 0, (
        "Aucun droit de roque ne doit contribuer au hash."
    )


# ---------------------------------------------------------------------------
# en_passant_key
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("square", range(40, 48))
def test_en_passant_key_rank_three(square: int) -> None:
    zobrist = create_zobrist()

    expected_key = zobrist._en_passant_keys[square - 40]

    assert zobrist.en_passant_key(square) == expected_key, (
        f"La case EP {square} de la rangée 3 doit utiliser la clé "
        "correspondante parmi les huit premières clés."
    )


@pytest.mark.parametrize("square", range(16, 24))
def test_en_passant_key_rank_six(square: int) -> None:
    zobrist = create_zobrist()

    expected_key = zobrist._en_passant_keys[square - 16]

    assert zobrist.en_passant_key(square) == expected_key, (
        f"La case EP {square} de la rangée 6 doit utiliser la clé "
        "correspondante parmi les huit dernières clés."
    )


@pytest.mark.parametrize(
    "square",
    [
        *range(0, 16),
        *range(24, 40),
        *range(48, 64),
    ],
)
def test_en_passant_key_invalid_rank_returns_zero(square: int) -> None:
    zobrist = create_zobrist()

    assert zobrist.en_passant_key(square) == 0, (
        f"La case {square}, qui n'est ni sur la rangée 3 ni sur la rangée 6, "
        "ne doit pas avoir de clé d'en passant."
    )


# ---------------------------------------------------------------------------
# en_passant_square_is_pertinent
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fen",
    [
        # Pion blanc à gauche de la case EP.
        "8/8/8/8/3p4/8/8/8 b - e3 0 1",

        # Pion blanc à droite de la case EP.
        "8/8/8/8/5p2/8/8/8 b - e3 0 1",

        # Deux pions blancs peuvent capturer la case EP.
        "8/8/8/8/3p1p2/8/8/8 b - e3 0 1",

        # Pion noir à gauche de la case EP.
        "8/8/8/3P4/8/8/8/8 w - e6 0 1",

        # Pion noir à droite de la case EP.
        "8/8/8/5P2/8/8/8/8 w - e6 0 1",

        # Deux pions noirs peuvent capturer la case EP.
        "8/8/8/3P1P2/8/8/8/8 w - e6 0 1",
    ],
)
def test_en_passant_square_is_pertinent_when_pawn_can_capture(
    fen: str,
) -> None:
    zobrist = create_zobrist()
    position = Position(fen)

    assert zobrist.en_passant_square_is_pertinent(position), (
        f"La case d'en passant doit être pertinente pour la position : {fen}"
    )


@pytest.mark.parametrize(
    "fen",
    [
        # Aucun pion blanc autour de e3.
        "8/8/8/8/8/8/8/8 w - e3 0 1",

        # Pion blanc trop éloigné.
        "8/8/8/8/8/8/P7/8 w - e3 0 1",

        # Pion noir présent mais les blancs sont au trait.
        "8/8/8/8/8/3p4/8/8 w - e3 0 1",

        # Aucun pion noir autour de e6.
        "8/8/8/8/8/8/8/8 b - e6 0 1",

        # Pion noir trop éloigné.
        "8/8/8/8/8/8/8/p7 b - e6 0 1",

        # Pion blanc présent mais les noirs sont au trait.
        "8/8/8/8/8/3P4/8/8 b - e6 0 1",
    ],
)
def test_en_passant_square_is_not_pertinent_when_no_pawn_can_capture(
    fen: str,
) -> None:
    zobrist = create_zobrist()
    position = Position(fen)

    assert not zobrist.en_passant_square_is_pertinent(position), (
        f"La case d'en passant ne doit pas être pertinente pour la position : {fen}"
    )


@pytest.mark.parametrize(
    "fen",
    [
        "8/8/8/3P4/8/8/8/8 w - e6 0 1",
        "8/8/8/8/3p4/8/8/8 b - e3 0 1",
    ],
)
def test_en_passant_square_is_pertinent_requires_correct_side_to_move(
    fen: str,
) -> None:
    zobrist = create_zobrist()
    position = Position(fen)

    assert zobrist.en_passant_square_is_pertinent(position), (
        f"La pertinence de l'EP doit dépendre du joueur au trait : {fen}"
    )


@pytest.mark.parametrize(
    "fen",
    [
        "8/8/8/8/8/3P4/8/8 w - e4 0 1",
        "8/8/8/8/8/3P4/8/8 w - e2 0 1",
        "8/3p4/8/8/8/8/8/8 b - e5 0 1",
        "8/3p4/8/8/8/8/8/8 b - e7 0 1",
    ],
)
def test_en_passant_square_is_not_pertinent_outside_valid_ep_ranks(
    fen: str,
) -> None:
    zobrist = create_zobrist()
    position = Position(fen)

    assert not zobrist.en_passant_square_is_pertinent(position), (
        f"Une case EP située sur une rangée invalide ne doit pas être "
        f"considérée comme pertinente : {fen}"
    )


# ---------------------------------------------------------------------------
# hash_position - basic properties
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fen",
    [
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "8/8/8/8/8/8/8/8 b - - 0 1",
        "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 10 20",
    ],
)
def test_hash_position_is_deterministic_for_same_position(
    fen: str,
) -> None:
    zobrist = create_zobrist()

    first_position = Position(fen)
    second_position = Position(fen)

    first_hash = zobrist.hash_position(first_position)
    second_hash = zobrist.hash_position(second_position)

    assert first_hash == second_hash, (
        f"Une même position doit toujours produire le même hash : {fen}"
    )


@pytest.mark.parametrize(
    "fen",
    [
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    ],
)
def test_same_position_and_same_seed_produce_same_hash(
    fen: str,
) -> None:
    first = Zobrist(seed=42)
    second = Zobrist(seed=42)
    position = Position(fen)

    first_hash = first.hash_position(position)
    second_hash = second.hash_position(position)

    assert first_hash == second_hash, (
        f"Deux instances utilisant le même seed doivent produire le même "
        f"hash pour la position : {fen}"
    )


@pytest.mark.parametrize(
    ("fen_white", "fen_black"),
    [
        (
            "8/8/8/8/8/8/8/8 w - - 0 1",
            "8/8/8/8/8/8/8/8 b - - 0 1",
        ),
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
            "4k3/8/8/8/8/8/8/4K3 b - - 0 1",
        ),
        (
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR b KQkq - 0 1",
        ),
    ],
)
def test_hash_changes_when_side_to_move_changes(
    fen_white: str,
    fen_black: str,
) -> None:
    zobrist = create_zobrist()

    white_hash = zobrist.hash_position(Position(fen_white))
    black_hash = zobrist.hash_position(Position(fen_black))

    assert white_hash != black_hash, (
        "Le hash doit être différent lorsque seul le joueur au trait change."
    )


# ---------------------------------------------------------------------------
# hash_position - pieces
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fen_first", "fen_second"),
    [
        (
            "4K3/8/8/8/8/8/8/4k3 w - - 0 1",
            "3K4/8/8/8/8/8/8/4k3 w - - 0 1",
        ),
        (
            "4K3/8/8/8/8/8/8/4k3 w - - 0 1",
            "4Q3/8/8/8/8/8/8/4k3 w - - 0 1",
        ),
        (
            "4K3/8/8/8/8/8/8/4k3 w - - 0 1",
            "4R3/8/8/8/8/8/8/4k3 w - - 0 1",
        ),
        (
            "4K3/8/8/8/8/8/8/4k3 w - - 0 1",
            "4B3/8/8/8/8/8/8/4k3 w - - 0 1",
        ),
        (
            "4K3/8/8/8/8/8/8/4k3 w - - 0 1",
            "4N3/8/8/8/8/8/8/4k3 w - - 0 1",
        ),
        (
            "4K3/8/8/8/8/8/8/4k3 w - - 0 1",
            "4P3/8/8/8/8/8/8/4k3 w - - 0 1",
        ),
    ],
)
def test_hash_changes_when_piece_configuration_changes(
    fen_first: str,
    fen_second: str,
) -> None:
    zobrist = create_zobrist()

    first_hash = zobrist.hash_position(Position(fen_first))
    second_hash = zobrist.hash_position(Position(fen_second))

    assert first_hash != second_hash, (
        "Une modification de la configuration des pièces doit modifier le hash."
    )


# ---------------------------------------------------------------------------
# hash_position - castling rights
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("first_rights", "second_rights"),
    [
        ("-", "K"),
        ("-", "Q"),
        ("-", "k"),
        ("-", "q"),
        ("K", "Q"),
        ("K", "KQ"),
        ("KQ", "KQk"),
        ("KQk", "KQkq"),
        ("KQkq", "-"),
    ],
)
def test_hash_changes_when_castling_rights_change(
    first_rights: str,
    second_rights: str,
) -> None:
    zobrist = create_zobrist()

    first_position = Position(
        f"4k3/8/8/8/8/8/8/4K3 w {first_rights} - 0 1"
    )
    second_position = Position(
        f"4k3/8/8/8/8/8/8/4K3 w {second_rights} - 0 1"
    )

    first_hash = zobrist.hash_position(first_position)
    second_hash = zobrist.hash_position(second_position)

    assert first_hash != second_hash, (
        f"Les droits de roque {first_rights!r} et {second_rights!r} "
        "doivent produire des hashes différents."
    )


# ---------------------------------------------------------------------------
# hash_position - en passant
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fen_with_ep", "fen_without_ep"),
    [
        (
            "8/8/8/8/3p4/8/8/8 b - e3 0 1",
            "8/8/8/8/3p4/8/8/8 b - - 0 1"
        ),
        (
            "8/8/8/8/5p2/8/8/8 b - e3 0 1",
            "8/8/8/8/5p2/8/8/8 b - - 0 1"
        ),
        (
            "8/8/8/3P4/8/8/8/8 w - e6 0 1",
            "8/8/8/3P4/8/8/8/8 w - - 0 1"
        ),
        (
            "8/8/8/5P2/8/8/8/8 w - e6 0 1",
            "8/8/8/5P2/8/8/8/8 w - - 0 1"
        ),
    ],
)
def test_hash_changes_when_relevant_en_passant_square_changes(
    fen_with_ep: str,
    fen_without_ep: str,
) -> None:
    zobrist = create_zobrist()

    hash_with_ep = zobrist.hash_position(Position(fen_with_ep))
    hash_without_ep = zobrist.hash_position(Position(fen_without_ep))

    assert hash_with_ep != hash_without_ep, (
        "Une case d'en passant pertinente doit contribuer au hash."
    )


@pytest.mark.parametrize(
    ("fen_with_ep", "fen_without_ep"),
    [
        (
            "8/8/8/8/8/8/8/8 w - e3 0 1",
            "8/8/8/8/8/8/8/8 w - - 0 1",
        ),
        (
            "8/8/8/8/8/8/P7/8 w - e3 0 1",
            "8/8/8/8/8/8/P7/8 w - - 0 1",
        ),
        (
            "8/8/8/8/8/8/8/8 b - e6 0 1",
            "8/8/8/8/8/8/8/8 b - - 0 1",
        ),
        (
            "8/8/8/8/8/8/8/p7 b - e6 0 1",
            "8/8/8/8/8/8/8/p7 b - - 0 1",
        ),
    ],
)
def test_hash_ignores_irrelevant_en_passant_square(
    fen_with_ep: str,
    fen_without_ep: str,
) -> None:
    zobrist = create_zobrist()

    hash_with_ep = zobrist.hash_position(Position(fen_with_ep))
    hash_without_ep = zobrist.hash_position(Position(fen_without_ep))

    assert hash_with_ep == hash_without_ep, (
        "Une case d'en passant sans capture possible ne doit pas contribuer "
        "au hash."
    )


# ---------------------------------------------------------------------------
# hash_position - complete position changes
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fen_first", "fen_second", "description"),
    [
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
            "4k3/8/8/8/8/8/8/4K3 b - - 0 1",
            "changement du joueur au trait",
        ),
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
            "4k3/8/8/8/8/8/8/4K3 w K - 0 1",
            "ajout du petit roque blanc",
        ),
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
            "4k3/8/8/8/8/8/4P3/4K3 w - - 0 1",
            "ajout d'un pion",
        ),
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1",
            "4k3/8/8/8/8/8/8/3K4 w - - 0 1",
            "déplacement du roi",
        ),
    ],
)
def test_different_position_components_produce_different_hashes(
    fen_first: str,
    fen_second: str,
    description: str,
) -> None:
    zobrist = create_zobrist()

    first_hash = zobrist.hash_position(Position(fen_first))
    second_hash = zobrist.hash_position(Position(fen_second))

    assert first_hash != second_hash, (
        f"Le changement de position ({description}) doit modifier le hash."
    )


# ---------------------------------------------------------------------------
# Hash range
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "fen",
    [
        "8/8/8/8/8/8/8/8 w - - 0 1",
        "8/8/8/8/8/8/8/8 b - - 0 1",
        "4k3/8/8/8/8/8/8/4K3 w KQkq - 0 1",
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        "r3k2r/8/8/8/8/8/8/R3K2R b KQkq - 50 20",
    ],
)
def test_hash_position_returns_64_bit_integer(fen: str) -> None:
    zobrist = create_zobrist()
    position = Position(fen)

    position_hash = zobrist.hash_position(position)

    assert isinstance(position_hash, int), (
        "Le hash d'une position doit être un entier."
    )

    assert 0 <= position_hash < (1 << NUMBER_OF_SQUARES), (
        "Le hash d'une position doit rester compris dans l'espace "
        "des entiers non signés sur 64 bits."
    )


# ---------------------------------------------------------------------------
# Hash algebra properties
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("color", "piece_type", "square"),
    [
        (Color.WHITE, PieceType.KING, 0),
        (Color.WHITE, PieceType.QUEEN, 7),
        (Color.WHITE, PieceType.ROOK, 16),
        (Color.WHITE, PieceType.BISHOP, 23),
        (Color.WHITE, PieceType.KNIGHT, 40),
        (Color.WHITE, PieceType.PAWN, 63),
        (Color.BLACK, PieceType.KING, 0),
        (Color.BLACK, PieceType.QUEEN, 7),
        (Color.BLACK, PieceType.ROOK, 16),
        (Color.BLACK, PieceType.BISHOP, 23),
        (Color.BLACK, PieceType.KNIGHT, 40),
        (Color.BLACK, PieceType.PAWN, 63),
    ],
)
def test_piece_key_is_reversible_by_xor(
    color: Color,
    piece_type: PieceType,
    square: int,
) -> None:
    zobrist = create_zobrist()

    key = zobrist.piece_key(color, piece_type, square)

    assert key ^ key == 0, (
        "Une clé Zobrist XORée avec elle-même doit s'annuler."
    )


@pytest.mark.parametrize(
    "castling_rights",
    [
        CastlingRights.NONE,
        CastlingRights.WHITE_KINGSIDE,
        CastlingRights.WHITE_QUEENSIDE,
        CastlingRights.BLACK_KINGSIDE,
        CastlingRights.BLACK_QUEENSIDE,
        CastlingRights.WHITE_KINGSIDE | CastlingRights.WHITE_QUEENSIDE,
        CastlingRights.BLACK_KINGSIDE | CastlingRights.BLACK_QUEENSIDE,
        CastlingRights.WHITE_KINGSIDE
        | CastlingRights.WHITE_QUEENSIDE
        | CastlingRights.BLACK_KINGSIDE
        | CastlingRights.BLACK_QUEENSIDE,
    ],
)
def test_castling_key_is_deterministic(
    castling_rights: CastlingRights,
) -> None:
    zobrist = create_zobrist()

    first_key = zobrist.castling_key(castling_rights)
    second_key = zobrist.castling_key(castling_rights)

    assert first_key == second_key, (
        f"Les mêmes droits de roque {castling_rights} doivent toujours "
        "produire la même clé."
    )