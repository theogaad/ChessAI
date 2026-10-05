import random

from src.chess_engine.constants import (
    BOARD_SIZE, 
    NUMBER_OF_SQUARES, 
    PIECE_TYPE_NUMBER, 
    DIFFERENT_PIECES_NUMBER, 
    CASTLING_RIGHTS_NUMBER, 
)
from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType, CastlingRights


class Zobrist:
    """Gère les clés de hachage Zobrist utilisées par le moteur.

    Le hachage Zobrist permet d'associer une valeur entière à une position
    d'échecs afin de pouvoir identifier rapidement une position et détecter
    notamment les répétitions.

    Une clé aléatoire distincte est associée à chaque combinaison de couleur,
    de type de pièce et de case. Des clés supplémentaires sont utilisées pour
    le joueur devant jouer, les droits de roque et la case en passant.

    Les clés sont générées une seule fois lors de l'initialisation et restent
    inchangées pendant toute la durée de vie de l'instance.

    Attributes:
        _piece_keys: Clés Zobrist associées à chaque combinaison de couleur,
            de type de pièce et de case.
        _side_to_move_key: Clé utilisée lorsque les Noirs sont au trait.
        _castling_keys: Clés associées aux différentes combinaisons de droits
            de roque.
        _en_passant_keys: Clés associées aux différentes cases en passant.
    """

    def __init__(self, seed: int | None = None) -> None:
        """Initialise les clés Zobrist.

        Args:
            seed: Graine optionnelle utilisée pour initialiser le générateur
                de nombres aléatoires. Si None, une graine aléatoire est
                utilisée.
        """
        random_generator = random.Random(seed)

        self._piece_keys: list[list[int]] = [[random_generator.getrandbits(NUMBER_OF_SQUARES) for _ in range(NUMBER_OF_SQUARES)]
                                             for _ in range(DIFFERENT_PIECES_NUMBER)]
        self._side_to_move_key: int = random_generator.getrandbits(NUMBER_OF_SQUARES)
        self._castling_keys: list[int] = [random_generator.getrandbits(NUMBER_OF_SQUARES) 
                                          for _ in range(CASTLING_RIGHTS_NUMBER)]
        self._en_passant_keys: list[int] = [random_generator.getrandbits(NUMBER_OF_SQUARES) 
                                           for _ in range(BOARD_SIZE * 2)]

    def hash_position(self, position: Position) -> int:
        """Calcule le hash Zobrist complet d'une position.

        Args:
            position: Position dont le hash doit être calculé.

        Returns:
            Valeur entière représentant le hash Zobrist de la position.
        """
        hash: int = 0

        for square in range(NUMBER_OF_SQUARES):
            piece: tuple[Color, PieceType] | None = position.piece_bitboards.get_piece_at(square)

            if piece:
                hash ^= self.piece_key(piece[0], piece[1], square)

        if position.side_to_move is Color.BLACK:
            hash ^= self.side_to_move_key()

        hash ^= self.castling_key(position.castling_rights)

        if position.en_passant_square is not None and self.en_passant_square_is_pertinent(position):
            hash ^= self.en_passant_key(position.en_passant_square)

        return hash

    def piece_key(
        self,
        color: Color,
        piece_type: PieceType,
        square: int,
    ) -> int:
        """Retourne la clé Zobrist associée à une pièce sur une case.

        Args:
            color: Couleur de la pièce.
            piece_type: Type de la pièce.
            square: Indice de la case occupée.

        Returns:
            Clé Zobrist correspondante.
        """
        return self._piece_keys[color.value * PIECE_TYPE_NUMBER + piece_type.value][square]

    def side_to_move_key(self) -> int:
        """Retourne la clé Zobrist associée au trait des Noirs.

        Returns:
            Clé Zobrist utilisée lorsque les Noirs doivent jouer.
        """
        return self._side_to_move_key

    def castling_key(self, castling_rights: CastlingRights) -> int:
        """Retourne la clé Zobrist associée aux droits de roque.

        Args:
            castling_rights: Combinaison des droits de roque disponibles.

        Returns:
            Clé Zobrist correspondante.
        """
        castling_hash: int = 0

        if castling_rights & CastlingRights.WHITE_KINGSIDE:
            castling_hash ^= self._castling_keys[0]
        if castling_rights & CastlingRights.WHITE_QUEENSIDE:
            castling_hash ^= self._castling_keys[1]
        if castling_rights & CastlingRights.BLACK_KINGSIDE:
            castling_hash ^= self._castling_keys[2]
        if castling_rights & CastlingRights.BLACK_QUEENSIDE:
            castling_hash ^= self._castling_keys[3]

        return castling_hash

    def en_passant_key(self, square: int) -> int:
        """Retourne la clé Zobrist associée à une case en passant.

        Args:
            square: Indice de la case en passant.

        Returns:
            Clé Zobrist correspondante.
        """
        if square // BOARD_SIZE == 2:
            return self._en_passant_keys[square - BOARD_SIZE * 2]

        elif square // BOARD_SIZE == 5:
            return self._en_passant_keys[square - BOARD_SIZE * (BOARD_SIZE - 3)]

        else:
            return 0

    def en_passant_square_is_pertinent(self, position: Position) -> bool:
        if position.en_passant_square is None:
            return False
        
        en_passant_square: int = position.en_passant_square
        pawn_squares: int = 0
        pawn_bitboard: int = 0

        if en_passant_square // BOARD_SIZE == 2 and position.side_to_move is Color.WHITE:
            pawn_bitboard = position.piece_bitboards.get_bitboard(Color.WHITE, PieceType.PAWN)

            if en_passant_square % BOARD_SIZE != 0:
                pawn_squares |= (1 << (en_passant_square + (BOARD_SIZE - 1)))

            if en_passant_square % BOARD_SIZE != (BOARD_SIZE - 1):
                pawn_squares |= (1 << (en_passant_square + (BOARD_SIZE + 1)))

        elif en_passant_square // BOARD_SIZE == (BOARD_SIZE - 3) and position.side_to_move is Color.BLACK:
            pawn_bitboard = position.piece_bitboards.get_bitboard(Color.BLACK, PieceType.PAWN)

            if en_passant_square % BOARD_SIZE != 0:
                pawn_squares |= (1 << (en_passant_square - (BOARD_SIZE + 1)))

            if en_passant_square % BOARD_SIZE != (BOARD_SIZE - 1):
                pawn_squares |= (1 << (en_passant_square - (BOARD_SIZE - 1)))

        return pawn_squares & pawn_bitboard != 0