from src.chess.profile import Profile
from src.chess.player import Player
from src.chess.board import Board
from src.chess.move import Move
from src.chess.pieces.piece import PieceColor
from random import randint

class Game:
    def __init__(self, profiles: list[Profile]):
        if len(profiles) != 2:
            raise ValueError("Une partie d'échec se crée avec exactement 2 joueurs.")
        
        # Initialisation des joueurs : blanc/noir
        random_index = randint(0,1)
        self.players: list[Player] = [
            Player(profiles[random_index], PieceColor.WHITE), 
            Player(profiles[(random_index + 1) % 2], PieceColor.BLACK)
        ]
        self.current_player: Player = self.players[0]

        self.board: Board = Board()
        self.moves: list[Move] = []
        self.winner: None|Player = None