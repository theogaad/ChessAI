import pytest

from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.constants import INITIAL_FEN
from src.chess_engine.position import Position
from src.chess_engine.types import Color


def bitboard(*squares: int) -> int:
    """Construit un bitboard à partir d'indices de cases."""
    result: int = 0

    for square in squares:
        result |= 1 << square

    return result


@pytest.fixture
def attack_generator() -> AttackGenerator:
    """Retourne un générateur d'attaques."""
    return AttackGenerator()

@pytest.mark.parametrize(
    ("square", "expected"),
    [
        (35, bitboard(26, 28)),  # e4 -> d5, f5
        (27, bitboard(18, 20)),  # e5 -> d6, f6
        (7, 0),        # a8
        (15, bitboard(6)),       # a7 -> b8
        (0, 0),        # h8 -> g7
        (8, bitboard(1)),        # h7 -> g8
    ],
)
def test_white_pawn_attacks(
    attack_generator: AttackGenerator,
    square: int,
    expected: int,
) -> None:
    """Vérifie les attaques des pions blancs."""
    assert attack_generator.pawn_attacks(square, Color.WHITE) == expected, (
        f"Attaques du pion blanc incorrectes pour la case {square}."
    )

@pytest.mark.parametrize(
    ("square", "expected"),
    [
        (35, bitboard(42, 44)),
        (27, bitboard(34, 36)),
        (56, 0),
        (48, bitboard(57)),
        (49, bitboard(56, 58)),
        (57, 0),
    ],
)
def test_black_pawn_attacks(
    attack_generator: AttackGenerator,
    square: int,
    expected: int,
) -> None:
    """Vérifie les attaques des pions noirs."""
    assert attack_generator.pawn_attacks(square, Color.BLACK) == expected, (
        f"Attaques du pion noir incorrectes pour la case {square}."
    )

@pytest.mark.parametrize(
    ("square", "expected"),
    [
        (0, bitboard(10, 17)),  # h8
        (7, bitboard(13, 22)),  # a8
        (56, bitboard(41, 50)),  # h1
        (63, bitboard(46, 53)),  # a1
        (3, bitboard(9, 13, 18, 20)),  # e8
        (24, bitboard(9, 18, 34, 41)),  # h5
        (
            35,
            bitboard(
                18, 20,
                25, 29,
                41, 45,
                50, 52,
            ),
        ),  # e4
    ],
)
def test_knight_attacks(
    attack_generator: AttackGenerator,
    square: int,
    expected: int,
) -> None:
    """Vérifie les attaques des cavaliers."""
    assert attack_generator.knight_attacks(square) == expected, (
        f"Attaques du cavalier incorrectes pour la case {square}."
    )

@pytest.mark.parametrize(
    ("square", "expected"),
    [
        (0, bitboard(1, 8, 9)),        # h8
        (7, bitboard(6, 14, 15)),      # a8
        (56, bitboard(48, 49, 57)),    # h1
        (63, bitboard(54, 55, 62)),    # a1
        (3, bitboard(2, 4, 10, 11, 12)),  # e8
        (59, bitboard(50, 51, 52, 58, 60)),  # e1
        (
            35,
            bitboard(
                26, 27, 28,
                34, 36,
                42, 43, 44,
            ),
        ),  # e4
    ],
)
def test_king_attacks(
    attack_generator: AttackGenerator,
    square: int,
    expected: int,
) -> None:
    """Vérifie les attaques des rois."""
    assert attack_generator.king_attacks(square) == expected, (
        f"Attaques du roi incorrectes pour la case {square}."
    )

@pytest.mark.parametrize(
    ("square", "occupied", "expected"),
    [
        (
            35,
            0,
            bitboard(
                26, 17, 8,
                28, 21, 14, 7,
                42, 49, 56,
                44, 53, 62,
            ),
        ),
        (
            0,
            0,
            bitboard(9, 18, 27, 36, 45, 54, 63),
        ),
        (
            35,
            bitboard(26),
            bitboard(
                26,
                28, 21, 14, 7,
                42, 49, 56,
                44, 53, 62,
            ),
        ),
        (
            35,
            bitboard(17, 21, 49),
            bitboard(
                26, 17,
                28, 21,
                42, 49,
                44, 53, 62,
            ),
        ),
        (
            35,
            bitboard(26, 28, 49, 53),
            bitboard(
                26,
                28,
                42, 49,
                44, 53,
            ),
        ),
    ],
)
def test_bishop_attacks(
    attack_generator: AttackGenerator,
    square: int,
    occupied: int,
    expected: int,
) -> None:
    """Vérifie les attaques des fous."""
    assert attack_generator.bishop_attacks(square, occupied) == expected, (
        f"Attaques du fou incorrectes pour la case {square} "
        f"avec l'occupation {occupied:#018x}."
    )

@pytest.mark.parametrize(
    ("square", "occupied", "expected"),
    [
        (
            35,
            0,
            bitboard(
                27, 19, 11, 3,
                43, 51, 59,
                34, 33, 32,
                36, 37, 38, 39
            ),
        ),
        (
            0,
            0,
            bitboard(
                8, 16, 24, 32, 40, 48, 56,
                1, 2, 3, 4, 5, 6, 7,
            ),
        ),
        (
            35,
            bitboard(27),
            bitboard(
                27,
                43, 51, 59,
                34, 33, 32,
                36, 37, 38, 39
            ),
        ),
        (
            35,
            bitboard(19, 37, 32),
            bitboard(
                27, 19,
                43, 51, 59,
                34, 33, 32,
                36, 37,
            ),
        ),
        (
            35,
            bitboard(27, 51, 33, 38),
            bitboard(
                27,
                43, 51,
                34, 33,
                36, 37, 38,
            ),
        ),
    ],
)
def test_rook_attacks(
    attack_generator: AttackGenerator,
    square: int,
    occupied: int,
    expected: int,
) -> None:
    """Vérifie les attaques des tours."""
    assert attack_generator.rook_attacks(square, occupied) == expected, (
        f"Attaques de la tour incorrectes pour la case {square} "
        f"avec l'occupation {occupied:#018x}."
    )

@pytest.mark.parametrize(
    ("square", "occupied"),
    [
        (35, 0),
        (35, bitboard(26, 28)),
        (0, 0),
        (63, 0),
        (35, bitboard(17, 27, 38, 49)),
    ],
)
def test_queen_attacks_is_bishop_or_rook_attacks(
    attack_generator: AttackGenerator,
    square: int,
    occupied: int,
) -> None:
    """Vérifie que les attaques de la dame combinent fou et tour."""
    expected: int = (
        attack_generator.bishop_attacks(square, occupied)
        | attack_generator.rook_attacks(square, occupied)
    )

    assert attack_generator.queen_attacks(square, occupied) == expected, (
        f"Attaques de la dame incorrectes pour la case {square} "
        f"avec l'occupation {occupied:#018x}."
    )

@pytest.mark.parametrize(
    ("fen", "square", "by_color", "expected"),
    [
        # Roi
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1", 
            51, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/8/8/4K3 w - - 0 1", 
            35, 
            Color.WHITE, 
            False
        ),

        # Cavalier
        (
            "4k3/8/8/8/8/8/3N4/4K3 w - - 0 1", 
            42, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/8/3N4/4K3 w - - 0 1", 
            34, 
            Color.WHITE, 
            False
        ),
        
        # Fou
        (
            "4k3/8/8/8/8/8/2B5/4K3 w - - 0 1", 
            44, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/8/2B5/4K3 w - - 0 1", 
            35, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/3p4/2B5/4K3 w - - 0 1", 
            35, 
            Color.WHITE, 
            False
        ),
        # Tour
        (
            "4k3/8/8/8/8/8/4R3/4K3 w - - 0 1", 
            43, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/8/4R3/4K3 w - - 0 1", 
            35, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/4p3/4R3/4K3 w - - 0 1", 
            35, 
            Color.WHITE, 
            False
        ),
        # Dame
        (
            "4k3/8/8/8/8/8/2Q5/4K3 w - - 0 1", 
            51, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/8/2Q5/4K3 w - - 0 1", 
            35, 
            Color.WHITE, 
            True
        ), 
        # Pion blanc
        (
            "4k3/8/8/8/8/4P3/8/4K3 w - - 0 1", 
            34, 
            Color.WHITE, 
            True
        ), 
        (
            "4k3/8/8/8/8/4P3/8/4K3 w - - 0 1", 
            36, 
            Color.WHITE, 
            True
        ), 
        # Pion noir
        (
            "4k3/8/8/8/8/8/3p4/4K3 b - - 0 1", 
            59, 
            Color.BLACK, 
            True
        ), 
        (
            "4k3/8/8/8/8/8/3p4/4K3 b - - 0 1", 
            61, 
            Color.BLACK, 
            True
        ),
        # Mauvaise couleur
        (
            "4k3/8/8/8/8/8/3N4/4K3 w - - 0 1", 
            42, 
            Color.BLACK, 
            False
        ),
        # Case non attaquée
        (
            INITIAL_FEN, 
            35, 
            Color.WHITE, 
            False
        ), 
        (
            INITIAL_FEN, 
            35, 
            Color.BLACK, 
            False
        ),
    ]
)
def test_is_square_attacked(
    attack_generator: AttackGenerator,
    fen: str,
    square: int,
    by_color: Color,
    expected: bool,
) -> None:
    """Vérifie la détection des cases attaquées."""
    position = Position(fen)

    assert attack_generator.is_square_attacked(
        position,
        square,
        by_color,
    ) is expected, (
        f"Résultat incorrect pour la case {square}, "
        f"la couleur {by_color.name} et le FEN '{fen}'."
    )