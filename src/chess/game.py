from copy import deepcopy
from enum import Enum
from random import randint
from src.chess.board import Board
from src.chess.case import Case
from src.chess.constants import BOARD_SIZE
from src.chess.exceptions.chess_error import ChessError
from src.chess.exceptions.illegal_move_error import IllegalMoveError
from src.chess.move import Move, SpecialMove
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.player import Player
from src.chess.position import Position
from src.chess.profile import Profile



class GameStatus(Enum):
    IN_PROGRESS = "in_progress"
    CHECK = "check"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW_50_MOVES = "draw_50_moves"
    DRAW_INSUFFICIENT_MATERIAL = "draw_insufficient_material"



class Game:
    def __init__(self, profiles: list[Profile]) -> None:
        if not all(isinstance(profile, Profile) for profile in profiles) or len(profiles) != 2:
            raise TypeError("Game(self, profiles) L'attribut profile doit être une liste d'exactement 2 objets de type Profile.")
        
        # Initialisation des joueurs : blanc/noir
        random_index = randint(0,1)
        self.players: list[Player] = [
            Player(profiles[random_index], PieceColor.WHITE), 
            Player(profiles[(random_index + 1) % 2], PieceColor.BLACK)
        ]
        self.current_player: Player = self.players[0]
        self.board: Board = Board()
        self.board.set_to_initial_board()
        self.moves: list[Move] = []
        self.winner: None|Player = None
        self.status: GameStatus = GameStatus.IN_PROGRESS