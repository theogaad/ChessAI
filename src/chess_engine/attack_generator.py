from src.chess_engine.constants import BOARD_SIZE, NUMBER_OF_SQUARES, KNIGHT_DIRECTIONS, BISHOP_DIRECTIONS, ROOK_DIRECTIONS
from src.chess_engine.piece_bitboards import PieceBitboards
from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType


class AttackGenerator:
    """Génère les cases attaquées par les différentes pièces d'échecs.

    Les attaques des pions, cavaliers et rois sont pré-calculées lors de
    l'initialisation de l'instance, car elles ne dépendent pas de
    l'occupation du plateau.

    Les attaques des pièces glissantes (fous, tours et dames) sont calculées
    dynamiquement en fonction de l'occupation du plateau.

    La classe ne génère pas de coups et ne vérifie pas leur légalité. Une
    attaque représente uniquement les cases contrôlées par une pièce selon
    ses règles de déplacement.

    Attributes:
        _white_pawn_attacks: Table pré-calculée des attaques des pions blancs,
            indexée par case.
        _black_pawn_attacks: Table pré-calculée des attaques des pions noirs,
            indexée par case.
        _knight_attacks: Table pré-calculée des attaques des cavaliers,
            indexée par case.
        _king_attacks: Table pré-calculée des attaques des rois, indexée par
            case.
    """

    def __init__(self) -> None:
        """Initialise le générateur d'attaques.

        Les tables d'attaques des pions, cavaliers et rois sont calculées
        lors de l'initialisation.
        """
        self._white_pawn_attacks: list[int] = [0 for _ in range(NUMBER_OF_SQUARES)]
        self._black_pawn_attacks: list[int] = [0 for _ in range(NUMBER_OF_SQUARES)]
        self._knight_attacks: list[int] = [0 for _ in range(NUMBER_OF_SQUARES)]
        self._king_attacks: list[int] = [0 for _ in range(NUMBER_OF_SQUARES)]

        for square in range(NUMBER_OF_SQUARES):
            if square > (BOARD_SIZE - 1):
                self._king_attacks[square] |= (1 << square) >> BOARD_SIZE
                
                if square % BOARD_SIZE != 0:
                    self._white_pawn_attacks[square] |= (1 << square) >> (BOARD_SIZE + 1)
                    self._king_attacks[square] |= (1 << square) >> 1 | (1 << square) >> (BOARD_SIZE + 1)
                    
                if square % BOARD_SIZE != (BOARD_SIZE - 1):
                    self._white_pawn_attacks[square] |= (1 << square) >> (BOARD_SIZE - 1)
                    self._king_attacks[square] |= (1 << square) << 1 | (1 << square) >> (BOARD_SIZE - 1)

            if square < NUMBER_OF_SQUARES - BOARD_SIZE:
                self._king_attacks[square] |= (1 << square) << BOARD_SIZE
                
                if square % BOARD_SIZE != 0:
                    self._black_pawn_attacks[square] |= (1 << square) << (BOARD_SIZE - 1)
                    self._king_attacks[square] |= (1 << square) >> 1 | (1 << square) << (BOARD_SIZE - 1)

                if square % BOARD_SIZE != (BOARD_SIZE - 1):
                    self._black_pawn_attacks[square] |= (1 << square) << (BOARD_SIZE + 1)
                    self._king_attacks[square] |= (1 << square) << 1 | (1 << square) << (BOARD_SIZE + 1)

            rank: int = square // BOARD_SIZE
            file: int = square % BOARD_SIZE

            for rank_offset, file_offset in KNIGHT_DIRECTIONS:
                target_rank: int = rank + rank_offset
                target_file: int = file + file_offset

                if 0 <= target_rank < BOARD_SIZE and 0 <= target_file < BOARD_SIZE:
                    target_square: int = target_rank * BOARD_SIZE + target_file
                    self._knight_attacks[square] |= 1 << target_square

    def is_king_in_check(
        self, 
        position: Position
    ) -> bool:
        return self.is_square_attacked(
            position, 
            position.piece_bitboards.get_bitboard(
                position.side_to_move, 
                PieceType.KING
            ).bit_length() - 1, 
            position.side_to_move.opposite
        )

    def pawn_attacks(self, square: int, color: Color) -> int:
        """Retourne les cases attaquées par un pion.

        Args:
            square: Indice de la case occupée par le pion.
            color: Couleur du pion.

        Returns:
            Bitboard des cases attaquées par le pion.
        """
        if color is Color.WHITE:
            return self._white_pawn_attacks[square]
        
        return self._black_pawn_attacks[square]

    def knight_attacks(self, square: int) -> int:
        """Retourne les cases attaquées par un cavalier.

        Args:
            square: Indice de la case occupée par le cavalier.

        Returns:
            Bitboard des cases attaquées par le cavalier.
        """
        return self._knight_attacks[square]

    def king_attacks(self, square: int) -> int:
        """Retourne les cases attaquées par un roi.

        Args:
            square: Indice de la case occupée par le roi.

        Returns:
            Bitboard des cases attaquées par le roi.
        """
        return self._king_attacks[square]

    def bishop_attacks(self, square: int, occupied: int) -> int:
        """Retourne les cases attaquées par un fou.

        Les cases attaquées sont déterminées en fonction de l'occupation
        actuelle du plateau. Le calcul s'arrête lorsqu'une pièce bloque
        chaque direction de déplacement.

        Args:
            square: Indice de la case occupée par le fou.
            occupied: Bitboard représentant les cases occupées.

        Returns:
            Bitboard des cases attaquées par le fou.
        """
        attacks: int = 0

        rank: int = square // BOARD_SIZE
        file: int = square % BOARD_SIZE

        for rank_offset, file_offset in BISHOP_DIRECTIONS:
            new_rank: int = rank + rank_offset
            new_file: int = file + file_offset

            while 0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE:
                new_square: int = new_rank * BOARD_SIZE + new_file
                attacks |= 1 << new_square

                if 1 << new_square & occupied:
                    break

                new_rank += rank_offset
                new_file += file_offset

        return attacks

    def rook_attacks(self, square: int, occupied: int) -> int:
        """Retourne les cases attaquées par une tour.

        Les cases attaquées sont déterminées en fonction de l'occupation
        actuelle du plateau. Le calcul s'arrête lorsqu'une pièce bloque
        chaque direction de déplacement.

        Args:
            square: Indice de la case occupée par la tour.
            occupied: Bitboard représentant les cases occupées.

        Returns:
            Bitboard des cases attaquées par la tour.
        """
        attacks: int = 0
        
        rank: int = square // BOARD_SIZE
        file: int = square % BOARD_SIZE

        for rank_offset, file_offset in ROOK_DIRECTIONS:
            new_rank: int = rank + rank_offset
            new_file: int = file + file_offset

            while 0 <= new_rank < BOARD_SIZE and 0 <= new_file < BOARD_SIZE:
                new_square: int = new_rank * BOARD_SIZE + new_file
                attacks |= 1 << new_square

                if 1 << new_square & occupied:
                    break

                new_rank += rank_offset
                new_file += file_offset

        return attacks

    def queen_attacks(self, square: int, occupied: int) -> int:
        """Retourne les cases attaquées par une dame.

        Les attaques d'une dame correspondent à l'union de ses attaques
        diagonales et orthogonales.

        Args:
            square: Indice de la case occupée par la dame.
            occupied: Bitboard représentant les cases occupées.

        Returns:
            Bitboard des cases attaquées par la dame.
        """
        return self.bishop_attacks(square, occupied) | self.rook_attacks(square, occupied)

    def is_square_attacked(
        self,
        position: Position,
        square: int,
        by_color: Color,
    ) -> bool:
        """Détermine si une case est attaquée par une couleur donnée.

        Cette méthode considère les attaques de toutes les pièces de la
        couleur spécifiée présentes sur la position.

        Args:
            position: Position dans laquelle vérifier l'attaque.
            square: Indice de la case à vérifier.
            by_color: Couleur dont les pièces doivent être prises en compte.

        Returns:
            True si la case est attaquée par au moins une pièce de la couleur
            spécifiée, sinon False.
        """
        bitboards: PieceBitboards = position.piece_bitboards
        occupied: int = bitboards.occupied

        king: int = bitboards.get_bitboard(by_color, PieceType.KING)
        queen: int = bitboards.get_bitboard(by_color, PieceType.QUEEN)
        rook: int = bitboards.get_bitboard(by_color, PieceType.ROOK)
        bishop: int = bitboards.get_bitboard(by_color, PieceType.BISHOP)
        knight: int = bitboards.get_bitboard(by_color, PieceType.KNIGHT)
        pawn: int = bitboards.get_bitboard(by_color, PieceType.PAWN)

        if self.king_attacks(square) & king:
            return True

        if self.rook_attacks(square, occupied) & (rook | queen):
            return True

        if self.bishop_attacks(square, occupied) & (bishop | queen):
            return True

        if self.knight_attacks(square) & knight:
            return True

        if self.pawn_attacks(square, by_color.opposite) & pawn:
            return True

        return False