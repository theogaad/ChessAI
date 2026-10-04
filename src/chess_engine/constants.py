from src.chess_engine.types import Color, PieceType

BOARD_SIZE: int = 8
NUMBER_OF_SQUARES: int = 64

COLOR_NUMBER: int = len(Color)
PIECE_TYPE_NUMBER: int = len(PieceType)
DIFFERENT_PIECES_NUMBER: int = COLOR_NUMBER * PIECE_TYPE_NUMBER

BOARD_MASK: int = 0xFFFFFFFFFFFFFFFF

FILE_A: int = 0x8080808080808080
FILE_B: int = 0x4040404040404040
FILE_C: int = 0x2020202020202020
FILE_D: int = 0x1010101010101010
FILE_E: int = 0x0808080808080808
FILE_F: int = 0x0404040404040404
FILE_G: int = 0x0202020202020202
FILE_H: int = 0x0101010101010101

RANK_1: int = 0xFF00000000000000
RANK_2: int = 0x00FF000000000000
RANK_3: int = 0x0000FF0000000000
RANK_4: int = 0x000000FF00000000
RANK_5: int = 0x00000000FF000000
RANK_6: int = 0x0000000000FF0000
RANK_7: int = 0x000000000000FF00
RANK_8: int = 0x00000000000000FF

INITIAL_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

ASCII_VALUE: int = 97

KNIGHT_DIRECTIONS: tuple[tuple[int, int], ...] = (
    (2, 1), 
    (2, -1), 
    (-2, 1), 
    (-2, -1), 
    (1, 2), 
    (1, -2), 
    (-1, 2), 
    (-1, -2)
)

BISHOP_DIRECTIONS: tuple[tuple[int, int], ...] = (
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
)

ROOK_DIRECTIONS: tuple[tuple[int, int], ...] = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
)