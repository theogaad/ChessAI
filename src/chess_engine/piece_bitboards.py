from src.chess_engine.constants import PIECE_TYPE_NUMBER, DIFFERENT_PIECES_NUMBER
from src.chess_engine.types import Color, PieceType
from typing import TypeAlias

TupleBitboards: TypeAlias = tuple[
    int, int, int, int, int, int,
    int, int, int, int, int, int
]

class PieceBitboards:
    """Représente la position des pièces d'une partie sous forme de bitboards.

    La classe maintient un bitboard pour chaque combinaison de couleur et de
    type de pièce, ainsi que les bitboards d'occupation des pièces blanches,
    des pièces noires et de l'ensemble des pièces.

    Les douze bitboards sont ordonnés comme suit :
        0 : roi blanc
        1 : dame blanche
        2 : tour blanche
        3 : fou blanc
        4 : cavalier blanc
        5 : pion blanc
        6 : roi noir
        7 : dame noire
        8 : tour noire
        9 : fou noir
        10 : cavalier noir
        11 : pion noir

    Les opérations de modification supposent que les préconditions sont
    respectées par l'appelant. Aucune vérification de cohérence n'est
    effectuée par cette classe afin de limiter le coût des opérations
    fréquentes utilisées notamment lors de la recherche de coups.

    Attributes:
        _bitboards: Bitboards des combinaisons de couleur et de type
            de pièce.
        _white_pieces: Bitboard contenant toutes les pièces blanches.
        _black_pieces: Bitboard contenant toutes les pièces noires.
        _occupied: Bitboard contenant toutes les pièces.
    """

    def __init__(self, bitboards: TupleBitboards) -> None:
        """Initialise la représentation des pièces à partir de bitboards.

        Les bitboards sont fournis dans l'ordre correspondant aux combinaisons
        de couleur et de type de pièce défini par la classe.

        Args:
            bitboards: Tuple contenant tous les bitboards des pièces.
        """
        self._bitboards: list[int] = list(bitboards)
        self._white_pieces: int = 0
        self._black_pieces: int = 0

        for i in range(PIECE_TYPE_NUMBER):
            self._white_pieces |= bitboards[i]
            self._black_pieces |= bitboards[PIECE_TYPE_NUMBER + i]

        self._occupied: int = self._white_pieces | self._black_pieces

    @property
    def bitboards(self) -> TupleBitboards:
        """Retourne les bitboards de toutes les combinaisons de pièces.

        Returns:
            Un tuple contenant tous les bitboards.
        """
        return tuple([self._bitboards[i] for i in range(DIFFERENT_PIECES_NUMBER)])

    @property
    def white_pieces(self) -> int:
        """Retourne le bitboard contenant toutes les pièces blanches.

        Returns:
            Le bitboard d'occupation des pièces blanches.
        """
        return self._white_pieces

    @property
    def black_pieces(self) -> int:
        """Retourne le bitboard contenant toutes les pièces noires.

        Returns:
            Le bitboard d'occupation des pièces noires.
        """
        return self._black_pieces

    @property
    def occupied(self) -> int:
        """Retourne le bitboard contenant toutes les pièces.

        Returns:
            Le bitboard d'occupation de l'ensemble des pièces.
        """
        return self._occupied

    def add_piece(
        self,
        color: Color,
        piece_type: PieceType,
        square: int
    ) -> None:
        """Ajoute une pièce sur une case.

        Met à jour le bitboard correspondant ainsi que les bitboards
        d'occupation associés à la couleur et à l'ensemble des pièces.

        Args:
            color: Couleur de la pièce à ajouter.
            piece_type: Type de la pièce à ajouter.
            square: Indice de la case où ajouter la pièce.

        """
        square_mask: int = 1 << square
        bitboard_index: int = color.value * PIECE_TYPE_NUMBER + piece_type.value
        self._bitboards[bitboard_index] |= square_mask

        if color is Color.WHITE:
            self._white_pieces |= square_mask

        else:
            self._black_pieces |= square_mask
        
        self._occupied |= square_mask

    def remove_piece(
        self,
        color: Color,
        piece_type: PieceType,
        square: int
    ) -> None:
        """Retire une pièce d'une case.

        Met à jour le bitboard correspondant ainsi que les bitboards
        d'occupation associés à la couleur et à l'ensemble des pièces.

        Args:
            color: Couleur de la pièce à retirer.
            piece_type: Type de la pièce à retirer.
            square: Indice de la case sur laquelle retirer la pièce.

        """
        square_mask: int = 1 << square
        bitboard_index: int = color.value * PIECE_TYPE_NUMBER + piece_type.value
        self._bitboards[bitboard_index] &= ~square_mask

        if color is Color.WHITE:
            self._white_pieces &= ~square_mask

        else:
            self._black_pieces &= ~square_mask

        self._occupied &= ~square_mask

    def move_piece(
        self,
        color: Color,
        piece_type: PieceType,
        start_square: int,
        end_square: int
    ) -> None:
        """Déplace une pièce d'une case à une autre.

        Le bit correspondant à la case de départ est retiré et celui correspondant
        à la case d'arrivée est ajouté.

        Args:
            color: Couleur de la pièce à déplacer.
            piece_type: Type de la pièce à déplacer.
            start_square: Indice de la case de départ.
            end_square: Indice de la case d'arrivée.
        """
        self.remove_piece(color, piece_type, start_square)
        self.add_piece(color, piece_type, end_square)

    def clear(self) -> None:
        """Retire toutes les pièces des bitboards."""
        for i in range(DIFFERENT_PIECES_NUMBER):
            self._bitboards[i] = 0

        self._white_pieces = 0
        self._black_pieces = 0
        self._occupied = 0

    def get_piece_at(
        self,
        square: int
    ) -> tuple[Color, PieceType] | None:
        """Retourne la pièce présente sur une case.

        Args:
            square: Indice de la case à examiner.

        Returns:
            Un tuple contenant la couleur et le type de la pièce présente,
            ou None si la case est vide.
        """
        square_mask: int = 1 << square
        for color in Color:
            for piece_type in PieceType:
                if square_mask & self.get_bitboard(color, piece_type):
                    return (color, piece_type)

        return None

    def get_bitboard(
        self,
        color: Color,
        piece_type: PieceType
    ) -> int:
        """Retourne le bitboard correspondant à une pièce.

        Args:
            color: Couleur des pièces recherchées.
            piece_type: Type des pièces recherchées.

        Returns:
            Le bitboard correspondant à la combinaison de couleur et de
            type de pièce demandée.
        """
        bitboard_index: int = color.value * PIECE_TYPE_NUMBER + piece_type.value
        return self._bitboards[bitboard_index]