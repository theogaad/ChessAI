from src.chess.profile import Profile
from src.chess.player import Player
from src.chess.board import Board
from src.chess.move import Move
from src.chess.case import Case
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.exceptions.illegal_move_error import IllegalMoveError
from src.chess.constants import BOARD_SIZE
from random import randint
from copy import deepcopy

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

    def switch_players(self):
        self.current_player = self.players[1] if self.current_player.color == PieceColor.WHITE else self.players[0]

    def get_legal_moves(self, line: int, column: int) -> list[Case]:
        legal_moves: list[Case] = []
        possible_moves: list[Case] = self.board.get_possible_moves(line, column)
        for case in possible_moves:
            board_after_move: Board = deepcopy(self.board)
            board_after_move.apply_move(Move(board_after_move.grid[line][column], board_after_move.grid[case.line][case.column]))
            if board_after_move.is_checked(self.current_player):
                continue
            legal_moves.append(case)
        return legal_moves

    def get_color_every_legal_moves(self, color: PieceColor) -> list[Case]:
        every_legal_moves: list[Case] = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                case: Case = self.board.grid[i][j]
                if isinstance(case.content, Piece) and case.content.piece_color == color:
                    piece_legal_moves: list[Case] = self.get_legal_moves(i, j)
                    for legal_move in piece_legal_moves:
                        every_legal_moves.append(legal_move)
        return every_legal_moves

    def play_move(self, move: Move) -> None:
        if not isinstance(move.start.content, Piece):
            raise IllegalMoveError("L'attribut start d'un move doit être une case contenant une pièce.")
        
        piece: Piece = move.start.content
        if not piece.piece_color == self.current_player.color:
            raise IllegalMoveError("La couleur de la pièce jouée doit être la même que celle du joueur actuel.")
        
        piece_legal_moves: list[Case] = self.get_legal_moves(move.start.line, move.start.column)
        if not move.end in piece_legal_moves:
            raise IllegalMoveError("L'attribut end d'un move doit être une case atteignable par la pièce contenue dans l'attribut start.")

        self.board.apply_move(move)
        self.moves.append(move)
        self.switch_players()