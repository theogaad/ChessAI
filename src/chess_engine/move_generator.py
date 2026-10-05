from math import log2

from src.chess_engine.constants import BOARD_SIZE, NUMBER_OF_SQUARES
from src.chess_engine.types import Color, PieceType, CastlingRights, MoveType
from src.chess_engine.position import Position
from src.chess_engine.move import Move
from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.undo_info import UndoInfo


class MoveGenerator:
    """Génère les coups légaux d'une position d'échecs.

    Cette classe génère les coups pseudo-légaux des pièces présentes sur une
    position, puis élimine les coups qui laissent le roi du joueur actif en
    échec.

    Elle s'appuie sur ``AttackGenerator`` pour déterminer les cases
    contrôlées par les pièces et sur ``MoveExecutor`` pour appliquer
    temporairement les coups et vérifier la sécurité du roi.

    La classe gère notamment les déplacements normaux, les captures, les
    déplacements de pions, les promotions, les captures en passant et les
    roques.

    Attributes:
        _attack_generator: Générateur utilisé pour déterminer les cases
            attaquées par les pièces.
        _move_executor: Exécuteur utilisé pour appliquer et annuler les coups
            lors de la vérification de leur légalité.
    """

    def __init__(
        self,
        attack_generator: AttackGenerator,
        move_executor: MoveExecutor,
    ) -> None:
        """Initialise le générateur de coups.

        Args:
            attack_generator: Générateur utilisé pour calculer les attaques.
            move_executor: Exécuteur utilisé pour appliquer et annuler les
                coups.
        """
        self._attack_generator = attack_generator
        self._move_executor = move_executor

    def generate_legal_moves(self, position: Position) -> list[Move]:
        """Génère tous les coups légaux d'une position.

        Les coups pseudo-légaux sont générés puis vérifiés afin de s'assurer
        qu'ils ne laissent pas le roi du joueur actif en échec.

        Args:
            position: Position pour laquelle les coups doivent être générés.

        Returns:
            Liste des coups légaux disponibles dans la position.
        """
        legal_moves: list[Move] = []

        pseudo_legal_moves: list[Move] = self.generate_pseudo_legal_moves(position)

        for move in pseudo_legal_moves:
            undo_info: UndoInfo = self._move_executor.make_move(position, move)

            if not self._attack_generator.is_square_attacked(
                position, 
                position.piece_bitboards.get_bitboard(position.side_to_move.opposite, PieceType.KING).bit_length() - 1, 
                position.side_to_move
            ):
                legal_moves.append(move)

            self._move_executor.undo_move(position, move, undo_info)

        return legal_moves

    def generate_pseudo_legal_moves(self, position: Position) -> list[Move]:
        """Génère les coups pseudo-légaux d'une position.
        
        Les coups pseudo-légaux respectent les mouvements propres à chaque pièce 
        ainsi que les contraintes liées à l'occupation du plateau, mais ne 
        vérifient pas si le roi du joueur actif est laissé en échec.
        
        Args: 
            position: Position pour laquelle les coups doivent être générés.
        
        Returns:
            Liste des coups pseudo-légaux disponibles dans la position.
        """
        pseudo_legal_moves: list[Move] = []
        
        for square in range(NUMBER_OF_SQUARES):
            square_content: tuple[Color, PieceType] | None = position.piece_bitboards.get_piece_at(square)

            if square_content is None:
                continue

            color, piece_type = square_content

            if color is not position.side_to_move:
                continue

            pseudo_legal_squares: int = 0

            match piece_type:
                case PieceType.KING:
                    pseudo_legal_squares = self._attack_generator.king_attacks(square)
                    pseudo_legal_moves.extend(self.generate_castling_moves(
                        position, 
                        color, 
                        piece_type, 
                        square
                    ))
                case PieceType.QUEEN:
                    pseudo_legal_squares = self._attack_generator.queen_attacks(square, position.piece_bitboards.occupied)
                case PieceType.ROOK:
                    pseudo_legal_squares = self._attack_generator.rook_attacks(square, position.piece_bitboards.occupied)
                case PieceType.BISHOP:
                    pseudo_legal_squares = self._attack_generator.bishop_attacks(square, position.piece_bitboards.occupied)
                case PieceType.KNIGHT:
                    pseudo_legal_squares = self._attack_generator.knight_attacks(square)
                case PieceType.PAWN:
                    pseudo_legal_squares = self._attack_generator.pawn_attacks(square, color)

                    if color is Color.WHITE:
                        pseudo_legal_squares &= position.piece_bitboards.black_pieces
                        coeff: int = -1

                    else:
                        pseudo_legal_squares &= position.piece_bitboards.white_pieces
                        coeff: int = 1

                    forward: int = (1 << (square + coeff * BOARD_SIZE)) & ~position.piece_bitboards.occupied
                    pseudo_legal_squares |= forward

                    if (forward != 0 and 
                        ((color is Color.WHITE and square // BOARD_SIZE == BOARD_SIZE - 2) or 
                        (color is Color.BLACK and square // BOARD_SIZE == 1))):
                        pseudo_legal_squares |= ((1 << (square + 2 * coeff * BOARD_SIZE)) & 
                                                        ~position.piece_bitboards.occupied)

                    if (position.en_passant_square is not None and 
                        (1 << square) & self._attack_generator.pawn_attacks(
                            position.en_passant_square, 
                            color.opposite
                        ) != 0):
                        pseudo_legal_moves.append(Move(
                            square, 
                            position.en_passant_square, 
                            MoveType.EN_PASSANT
                        ))

            if color is Color.WHITE:
                pseudo_legal_squares &= ~position.piece_bitboards.white_pieces

            else:
                pseudo_legal_squares &= ~position.piece_bitboards.black_pieces

            while pseudo_legal_squares != 0:
                pseudo_legal_square: int = pseudo_legal_squares.bit_length() - 1

                if (piece_type is PieceType.PAWN and (
                    (color is Color.WHITE and pseudo_legal_square // BOARD_SIZE == 0) or
                    (color is Color.BLACK and pseudo_legal_square // BOARD_SIZE == BOARD_SIZE - 1)
                )):
                    for promotion_type in (PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT):
                        pseudo_legal_moves.append(Move(
                            square, 
                            pseudo_legal_square, 
                            MoveType.NORMAL, 
                            promotion_type
                        ))

                else:
                    pseudo_legal_moves.append(Move(
                        square, 
                        pseudo_legal_square, 
                        MoveType.NORMAL
                    ))

                pseudo_legal_squares &= ~(1 << pseudo_legal_square)
    
        return pseudo_legal_moves

    def generate_castling_moves(
        self, 
        position: Position, 
        color: Color,  
        square: int
    ) -> list[Move]:
        """Génère les coups de roque pseudo-légaux d'un roi.
        
        Vérifie les droits de roque, les cases situées entre le roi et la tour, 
        ainsi que les cases traversées ou occupées par le roi. La légalité 
        complète du coup reste vérifiée par ``generate_legal_moves``.

        Les tours sont supposées être bien placée.
        
        Args:
            position: Position actuelle.
            color: Couleur du roi dont les coups de roque sont recherchés.
            square: Case occupée par le roi.
        
        Returns:
            Liste contenant les coups de petit et de grand roque disponibles.
        """
        castling_moves: list[Move] = []

        if color is Color.WHITE:
            kingside_right: CastlingRights = CastlingRights.WHITE_KINGSIDE
            queenside_right: CastlingRights = CastlingRights.WHITE_QUEENSIDE
        else:
            kingside_right: CastlingRights = CastlingRights.BLACK_KINGSIDE
            queenside_right: CastlingRights = CastlingRights.BLACK_QUEENSIDE

        opponent: Color = color.opposite

        if not self._attack_generator.is_square_attacked(position, square, opponent):

            if (
                position.castling_rights & kingside_right
                and (1 << (square - 1) | 1 << (square - 2))
                    & position.piece_bitboards.occupied == 0
                and not self._attack_generator.is_square_attacked(position, square - 1, opponent)
                and not self._attack_generator.is_square_attacked(position, square - 2, opponent)
            ):
                castling_moves.append(
                    Move(square, square - 2, MoveType.CASTLING)
                )

            if (
                position.castling_rights & queenside_right
                and (1 << (square + 1) | 1 << (square + 2) | 1 << (square + 3))
                    & position.piece_bitboards.occupied == 0
                and not self._attack_generator.is_square_attacked(position, square + 1, opponent)
                and not self._attack_generator.is_square_attacked(position, square + 2, opponent)
            ):
                castling_moves.append(
                    Move(square, square + 2, MoveType.CASTLING)
                )

        return castling_moves