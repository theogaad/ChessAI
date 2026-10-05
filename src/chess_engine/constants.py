from src.chess_engine.types import Color, PieceType

BOARD_SIZE: int = 8 # Nombre de cases d'un côté de l'échiquier.
NUMBER_OF_SQUARES: int = BOARD_SIZE * BOARD_SIZE # Nombre de cases total dans l'échiquier.

COLOR_NUMBER: int = len(Color) # Nombre de couleurs possibles.
PIECE_TYPE_NUMBER: int = len(PieceType) # Nombre de types de pièce possibles.
DIFFERENT_PIECES_NUMBER: int = COLOR_NUMBER * PIECE_TYPE_NUMBER # Nombre de combinaisons (couleur, type) possibles.
CASTLING_RIGHTS_NUMBER: int = 4 # Nombre de droits de roque possibles.

BOARD_MASK: int = 0xFFFFFFFFFFFFFFFF # Masque dont les 64 bits sont à 1

FILE_A: int = 0x8080808080808080 # Masque dont les bits sur la colonne A sont à 1.
FILE_B: int = 0x4040404040404040 # Masque dont les bits sur la colonne B sont à 1.
FILE_C: int = 0x2020202020202020 # Masque dont les bits sur la colonne C sont à 1.
FILE_D: int = 0x1010101010101010 # Masque dont les bits sur la colonne D sont à 1.
FILE_E: int = 0x0808080808080808 # Masque dont les bits sur la colonne E sont à 1.
FILE_F: int = 0x0404040404040404 # Masque dont les bits sur la colonne F sont à 1.
FILE_G: int = 0x0202020202020202 # Masque dont les bits sur la colonne G sont à 1.
FILE_H: int = 0x0101010101010101 # Masque dont les bits sur la colonne H sont à 1.

RANK_1: int = 0xFF00000000000000 # Masque dont les bits sur la ligne 1 sont à 1.
RANK_2: int = 0x00FF000000000000 # Masque dont les bits sur la ligne 2 sont à 1.
RANK_3: int = 0x0000FF0000000000 # Masque dont les bits sur la ligne 3 sont à 1.
RANK_4: int = 0x000000FF00000000 # Masque dont les bits sur la ligne 4 sont à 1.
RANK_5: int = 0x00000000FF000000 # Masque dont les bits sur la ligne 5 sont à 1.
RANK_6: int = 0x0000000000FF0000 # Masque dont les bits sur la ligne 6 sont à 1.
RANK_7: int = 0x000000000000FF00 # Masque dont les bits sur la ligne 7 sont à 1.
RANK_8: int = 0x00000000000000FF # Masque dont les bits sur la ligne 8 sont à 1.

INITIAL_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" # FEN de la position initiale.

ASCII_VALUE: int = 97 # Valeur ASCII de la première lettre des colonnes (a).

KNIGHT_DIRECTIONS: tuple[tuple[int, int], ...] = ( # Directions possibles pour un cavalier.
    (2, 1), 
    (2, -1), 
    (-2, 1), 
    (-2, -1), 
    (1, 2), 
    (1, -2), 
    (-1, 2), 
    (-1, -2)
)

BISHOP_DIRECTIONS: tuple[tuple[int, int], ...] = ( # Directions possibles pour un fou.
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
)

ROOK_DIRECTIONS: tuple[tuple[int, int], ...] = ( # Directions possibles pour une tour.
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
)