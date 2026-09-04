from src.chess.profile import Profile
from src.chess.player import Player
from src.chess.board import Board
from src.chess.move import Move, SpecialMove
from src.chess.case import Case
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.king import King
from src.chess.pieces.rook import Rook
from src.chess.exceptions.illegal_move_error import IllegalMoveError
from src.chess.constants import BOARD_SIZE
from random import randint
from copy import deepcopy

class Game:
    def __init__(self, profiles: list[Profile]) -> None:
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

    def switch_players(self) -> None:
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def get_legal_moves(self, line: int, column: int) -> list[Case]:
        case_content = self.board.grid[line][column].content
        if case_content is None:
            return []
        legal_moves: list[Case] = []
        possible_moves: list[Case] = self.board.get_possible_moves(line, column)
        for case in possible_moves:
            board_after_move: Board = deepcopy(self.board)
            board_after_move.apply_move(Move(board_after_move.grid[line][column], board_after_move.grid[case.line][case.column]))
            if board_after_move.is_checked(case_content.piece_color):
                continue
            legal_moves.append(case)
            legal_moves.extend(self.get_castling_moves(line, column))
        return legal_moves

    def get_castling_moves(self, line: int, column: int) -> list[Case]:
        castling_moves: list[Case] = []
        actual_case: Case = self.board.grid[line][column]
        if isinstance(actual_case.content, King) and not actual_case.content.has_moved and not self.board.is_checked(actual_case.content.piece_color):
            king: King = actual_case.content
            for possible_rook in [self.board.grid[line][0], self.board.grid[line][7]]: # Tableau des deux cases censées contenir les tours
                if isinstance(possible_rook.content, Rook) and not possible_rook.content.has_moved:
                    rook_case: Case = possible_rook
                    rook_column: int = rook_case.column
                    direction: int = 1 if rook_column > column else -1
                    case_between_king_and_rook_is_empty: bool = True
                    case_between_king_and_rook_is_not_checked: bool = True
                    for i in range(min(rook_column, column) + 1, max(rook_column, column)):
                        temp_case = self.board.grid[line][i]
                        if temp_case.content is not None:
                            case_between_king_and_rook_is_empty = False
                            break
                    for i in range(2):
                        temp_board = deepcopy(self.board)
                        temp_board.apply_move(Move(temp_board.grid[line][column], temp_board.grid[line][column + (i + 1) * direction]))
                        if temp_board.is_checked(king.piece_color):
                            case_between_king_and_rook_is_not_checked = False
                            break
                    if case_between_king_and_rook_is_empty and case_between_king_and_rook_is_not_checked:
                        castling_moves.append(self.board.grid[line][column + 2 * direction])
        return castling_moves

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

        # Roque
        if move.special_move == SpecialMove.CASTLING:
            rook_case: Case = self.board.grid[move.start.line][7 if move.start.column < move.end.column else 0]
            rook_move: Move = Move(rook_case, self.board.grid[move.start.line][5 if move.start.column < move.end.column else 3])
            self.board.apply_move(rook_move)
        self.board.apply_move(move)
        self.moves.append(move)
        self.switch_players()

    def is_stalemate(self, color: PieceColor) -> bool:
            is_checked: bool = self.board.is_checked(color)
            every_legal_moves: list[Case] = self.get_color_every_legal_moves(color)
            return not is_checked and not every_legal_moves

    def is_checkmate(self, color: PieceColor) -> bool:
        is_checked: bool = self.board.is_checked(color)
        every_legal_moves: list[Case] = self.get_color_every_legal_moves(color)
        return is_checked and not every_legal_moves

    def is_game_over(self, player: Player) -> bool:
        return self.is_stalemate(player.color) or self.is_checkmate(player.color)