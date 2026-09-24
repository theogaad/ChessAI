from dataclasses import dataclass
from src.chess.board import Board
from src.chess.move import Move
from src.chess.player import Player
from src.chess.utils import verify_type



@dataclass(frozen=True)
class GameInfo:
    """Contient les informations essentielles de l'état d'une partie à un moment précis.
    
    Attributes:
        board: État de l'échiquier de la partie.
        current_player: Joueur dont c'est le tour.
        castling_possible_moves: Mouvements possibles du type roque.
        en_passant_possible_moves: Mouvements possibles du type en passant.
    """
    __board: Board
    __current_player: Player
    __castling_possible_moves: list[Move]
    __en_passant_possible_moves: list[Move]


    def __post_init__(self):
        """Vérifie le type de chaque propriété.
        
        Raises:
            TypeError: Si une des propriété n'est pas du type attendu.
        """
        verify_type(self.board, Board, "GameInfo(board, current_player, castling_possible_moves, en_passant_possible_moves)", "board")
        verify_type(self.current_player, Player, "GameInfo(board, current_player, castling_possible_moves, en_passant_possible_moves)", "current_player")
        verify_type(self.castling_possible_moves, list, "GameInfo(board, current_player, castling_possible_moves, en_passant_possible_moves)", "castling_possible_moves")
        verify_type(self.en_passant_possible_moves, list, "GameInfo(board, current_player, castling_possible_moves, en_passant_possible_moves)", "en_passant_possible_moves")

        for move in self.castling_possible_moves:
            verify_type(move, Move, "GameInfo(board, current_player, castling_possible_moves, en_passant_possible_moves)", "castling_possible_moves[x]")

        for move in self.en_passant_possible_moves:
            verify_type(move, Move, "GameInfo(board, current_player, castling_possible_moves, en_passant_possible_moves)", "en_passant_possible_moves[x]")


    @property
    def board(self) -> Board:
        """Retourne l'état de l'échiquier de la partie."""
        return self.__board

    @property
    def current_player(self) -> Player:
        """Retourne le joueur dont c'est le tour."""
        return self.__current_player

    @property
    def castling_possible_moves(self) -> list[Move]:
        """Retourne les mouvements possibles du type roque."""
        return self.__castling_possible_moves

    @property
    def en_passant_possible_moves(self) -> list[Move]:
        """Retourne les mouvements possibles du type en passant."""
        return self.__en_passant_possible_moves