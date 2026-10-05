from src.chess_engine.constants import BOARD_SIZE, NUMBER_OF_SQUARES
from src.chess_engine.move import Move
from src.chess_engine.piece_bitboards import PieceBitboards
from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType, CastlingRights, MoveType
from src.chess_engine.undo_info import UndoInfo
from src.chess_engine.zobrist import Zobrist


class MoveExecutor:
    """Applique et annule les coups sur une position.

    Cette classe est responsable de modifier une position lors de
    l'application d'un coup et de restaurer son état précédent lors de
    l'annulation du coup.

    Elle gère notamment les déplacements normaux, les captures, les
    promotions, les roques et les captures en passant, ainsi que la mise à
    jour des informations associées à la position.

    Le hash Zobrist est également mis à jour lors de l'application d'un coup
    et restauré lors de son annulation.

    La classe ne vérifie pas si un coup est légal. Les préconditions
    nécessaires à l'exécution d'un coup sont supposées être respectées par
    l'appelant.

    Attributes:
        _zobrist: Instance utilisée pour calculer et mettre à jour le hash
            Zobrist des positions.
    """

    def __init__(self, zobrist: Zobrist) -> None:
        """Initialise l'exécuteur de coups.

        Args:
            zobrist: Instance utilisée pour gérer le hash Zobrist.
        """
        self._zobrist = zobrist

    def make_move(self, position: Position, move: Move) -> UndoInfo:
        """Applique un coup à une position.

        L'état nécessaire à l'annulation du coup est sauvegardé avant toute
        modification de la position.

        Args:
            position: Position sur laquelle appliquer le coup.
            move: Coup à appliquer.

        Returns:
            Informations permettant d'annuler le coup avec ``undo_move``.
        """
        bitboards: PieceBitboards = position.piece_bitboards
        color, piece_type = bitboards.get_piece_at(move.start_square)

        # Anciennes infos
        captured_piece: tuple[Color, PieceType] | None = bitboards.get_piece_at(move.end_square)
        previous_castling_rights: CastlingRights = position.castling_rights
        previous_en_passant_square: int | None = position.en_passant_square
        previous_halfmove_clock: int = position.halfmove_clock
        previous_fullmove_number: int = position.fullmove_number
        previous_zobrist_hash: int = position.zobrist_hash

        # Annulation du zobrist
        zobrist_hash: int = previous_zobrist_hash
        zobrist_hash ^= self._zobrist.castling_key(previous_castling_rights)

        if self._zobrist.en_passant_square_is_pertinent(position):
            zobrist_hash ^= self._zobrist.en_passant_key(previous_en_passant_square)

        # Application du move
        if captured_piece is not None:
            position.piece_bitboards.remove_piece(captured_piece[0], captured_piece[1], move.end_square)
            zobrist_hash ^= self._zobrist.piece_key(captured_piece[0], captured_piece[1], move.end_square)

        if move.move_type is MoveType.CASTLING:
            if move.start_square - move.end_square > 0:
                position.piece_bitboards.move_piece(
                    color, 
                    PieceType.ROOK, 
                    move.start_square // BOARD_SIZE * BOARD_SIZE, 
                    move.end_square + 1
                )
                zobrist_hash ^= self._zobrist.piece_key(
                    color, 
                    PieceType.ROOK, 
                    move.start_square // BOARD_SIZE * BOARD_SIZE
                )
                zobrist_hash ^= self._zobrist.piece_key(color, PieceType.ROOK, move.end_square + 1)

            else:
                position.piece_bitboards.move_piece(
                    color, 
                    PieceType.ROOK, 
                    move.start_square // BOARD_SIZE * BOARD_SIZE + (BOARD_SIZE - 1), 
                    move.end_square - 1
                )
                zobrist_hash ^= self._zobrist.piece_key(
                    color, 
                    PieceType.ROOK, 
                    move.start_square // BOARD_SIZE * BOARD_SIZE + (BOARD_SIZE - 1)
                )
                zobrist_hash ^= self._zobrist.piece_key(color, PieceType.ROOK, move.end_square - 1)

        if move.move_type is MoveType.EN_PASSANT:
            coeff: int = -1 if color is Color.BLACK else 1
            captured_piece_square: int = move.end_square + coeff * BOARD_SIZE
            captured_piece = bitboards.get_piece_at(captured_piece_square)
            
            position.piece_bitboards.remove_piece(captured_piece[0], captured_piece[1], captured_piece_square)
            zobrist_hash ^= self._zobrist.piece_key(captured_piece[0], captured_piece[1], captured_piece_square)

        position.piece_bitboards.move_piece(color, piece_type, move.start_square, move.end_square)
        zobrist_hash ^= self._zobrist.piece_key(color, piece_type, move.start_square)
        zobrist_hash ^= self._zobrist.piece_key(color, piece_type, move.end_square)

        if move.promotion_piece_type is not None:
            position.piece_bitboards.remove_piece(color, piece_type, move.end_square)
            position.piece_bitboards.add_piece(color, move.promotion_piece_type, move.end_square)
            zobrist_hash ^= self._zobrist.piece_key(color, piece_type, move.end_square)
            zobrist_hash ^= self._zobrist.piece_key(color, move.promotion_piece_type, move.end_square)

        # Mise à jour de position
        position.en_passant_square = None

        if captured_piece is not None and captured_piece[1] is PieceType.ROOK:
            if move.end_square == 0:
                position.castling_rights &= ~CastlingRights.BLACK_KINGSIDE
            elif move.end_square == BOARD_SIZE - 1:
                position.castling_rights &= ~CastlingRights.BLACK_QUEENSIDE
            elif move.end_square == NUMBER_OF_SQUARES - 1:
                position.castling_rights &= ~CastlingRights.WHITE_QUEENSIDE
            elif move.end_square == NUMBER_OF_SQUARES - BOARD_SIZE:
                position.castling_rights &= ~CastlingRights.WHITE_KINGSIDE

        if piece_type is PieceType.KING:
            if color is Color.WHITE:
                position.castling_rights &= ~(CastlingRights.WHITE_KINGSIDE | CastlingRights.WHITE_QUEENSIDE)

            else:
                position.castling_rights &= ~(CastlingRights.BLACK_KINGSIDE | CastlingRights.BLACK_QUEENSIDE)

        elif piece_type is PieceType.ROOK:
            if move.start_square == 0:
                position.castling_rights &= ~CastlingRights.BLACK_KINGSIDE
            elif move.start_square == BOARD_SIZE - 1:
                position.castling_rights &= ~CastlingRights.BLACK_QUEENSIDE
            elif move.start_square == NUMBER_OF_SQUARES - 1:
                position.castling_rights &= ~CastlingRights.WHITE_QUEENSIDE
            elif move.start_square == NUMBER_OF_SQUARES - BOARD_SIZE:
                position.castling_rights &= ~CastlingRights.WHITE_KINGSIDE

        elif piece_type is PieceType.PAWN and abs(move.end_square - move.start_square) == 2 * BOARD_SIZE:
            coeff: int = 1 if color is Color.WHITE else -1
            position.en_passant_square = move.end_square +  coeff * BOARD_SIZE

            if self._zobrist.en_passant_square_is_pertinent(position):
                zobrist_hash ^= self._zobrist.en_passant_key(position.en_passant_square)

        if captured_piece is not None or piece_type is PieceType.PAWN:
            position.halfmove_clock = 0

        else:
            position.halfmove_clock += 1

        if position.side_to_move is Color.BLACK:
            position.fullmove_number += 1

        position.side_to_move = position.side_to_move.opposite

        # Zobrist
        zobrist_hash ^= self._zobrist.castling_key(position.castling_rights)
        zobrist_hash ^= self._zobrist.side_to_move_key()
        position.zobrist_hash = zobrist_hash

        return UndoInfo(
            captured_piece, 
            previous_castling_rights, 
            previous_en_passant_square, 
            previous_halfmove_clock, 
            previous_fullmove_number, 
            previous_zobrist_hash
        )

    def undo_move(
        self,
        position: Position,
        move: Move,
        undo_info: UndoInfo,
    ) -> None:
        """Annule un coup précédemment appliqué à une position.

        La position est restaurée à l'état qu'elle avait avant l'application
        du coup.

        Args:
            position: Position ayant subi le coup.
            move: Coup à annuler.
            undo_info: Informations sauvegardées lors de l'application du
                coup.
        """
        color, piece_type = position.piece_bitboards.get_piece_at(move.end_square)
        position.piece_bitboards.move_piece(color, piece_type, move.end_square, move.start_square)

        if move.promotion_piece_type is not None:
            position.piece_bitboards.remove_piece(color, piece_type, move.start_square)
            position.piece_bitboards.add_piece(color, PieceType.PAWN, move.start_square)

        if move.move_type is MoveType.CASTLING:
            if move.start_square - move.end_square > 0:
                position.piece_bitboards.move_piece(
                    color, 
                    PieceType.ROOK, 
                    move.end_square + 1, 
                    move.start_square // BOARD_SIZE * BOARD_SIZE
                )

            else:
                position.piece_bitboards.move_piece(
                    color, 
                    PieceType.ROOK, 
                    move.end_square - 1, 
                    move.start_square // BOARD_SIZE * BOARD_SIZE + (BOARD_SIZE - 1)
                )

        elif move.move_type is MoveType.EN_PASSANT:
            coeff: int = -1 if color is Color.BLACK else 1
            position.piece_bitboards.add_piece(
                undo_info.captured_piece[0], 
                undo_info.captured_piece[1], 
                move.end_square + coeff * BOARD_SIZE
            )

        elif undo_info.captured_piece is not None:
            position.piece_bitboards.add_piece(
                undo_info.captured_piece[0], 
                undo_info.captured_piece[1], 
                move.end_square
            )

        position.castling_rights = undo_info.previous_castling_rights
        position.en_passant_square = undo_info.previous_en_passant_square
        position.halfmove_clock = undo_info.previous_halfmove_clock
        position.fullmove_number = undo_info.previous_fullmove_number
        position.zobrist_hash = undo_info.previous_zobrist_hash
        position.side_to_move = position.side_to_move.opposite