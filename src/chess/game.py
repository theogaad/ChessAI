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


    def switch_players(self) -> None:
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]


    def get_legal_moves(self, position: Position) -> list[Case]:
        case_content: None | Piece = self.board.grid[position.line][position.column].content

        if case_content is None:
            return []
        
        legal_moves: list[Case] = []
        possible_moves: list[Case] = self.board.get_reachable_cases_from_position(position)

        for case in possible_moves:
            board_after_move: Board = deepcopy(self.board)
            board_after_move.apply_move(Move(board_after_move.grid[position.line][position.column], 
                                             board_after_move.grid[case.position.line][case.position.column]))

            if board_after_move.is_checked(case_content.piece_color):
                continue

            legal_moves.append(case)
            legal_moves.extend(self.get_castling_moves(position))
            legal_moves.extend(self.get_en_passant_moves(position))

        return legal_moves


    def get_castling_moves(self, position: Position) -> list[Case]:
        castling_moves: list[Case] = []
        actual_case: Case = self.board.grid[position.line][position.column]

        if isinstance(actual_case.content, King) and not actual_case.content.has_moved and not self.board.is_checked(actual_case.content.piece_color):
            king: King = actual_case.content

            for possible_rook in [self.board.grid[position.line][0], self.board.grid[position.line][7]]: # Tableau des deux cases censées contenir les tours
                if isinstance(possible_rook.content, Rook) and not possible_rook.content.has_moved:
                    rook_case: Case = possible_rook
                    rook_column: int = rook_case.position.column
                    direction: int = 1 if rook_column > position.column else -1
                    case_between_king_and_rook_is_empty: bool = True
                    case_between_king_and_rook_is_not_checked: bool = True

                    for i in range(min(rook_column, position.column) + 1, max(rook_column, position.column)):
                        temp_case = self.board.grid[position.line][i]

                        if temp_case.content is not None:
                            case_between_king_and_rook_is_empty = False
                            break

                    for i in range(2):
                        temp_board = deepcopy(self.board)
                        temp_board.apply_move(Move(temp_board.grid[position.line][position.column], 
                                                   temp_board.grid[position.line][position.column + (i + 1) * direction]))

                        if temp_board.is_checked(king.piece_color):
                            case_between_king_and_rook_is_not_checked = False
                            break

                    if case_between_king_and_rook_is_empty and case_between_king_and_rook_is_not_checked:
                        castling_moves.append(self.board.grid[position.line][position.column + 2 * direction])

        return castling_moves

    def get_en_passant_moves(self, position: Position) -> list[Case]:
        en_passant_moves: list[Case] = []
        actual_case: Case = self.board.grid[position.line][position.column]

        if isinstance(actual_case.content, Pawn) and self.moves:
            last_move: Move = self.moves[-1]
            last_move_end_case: Case = self.board.grid[last_move.end_case.position.line][last_move.end_case.position.column]

            if (isinstance(last_move_end_case.content, Pawn) and
            last_move_end_case.content.piece_color != actual_case.content.piece_color and
            abs(last_move.start_case.position.line - last_move.end_case.position.line) == 2 and
            last_move.end.line == line and abs(last_move.end.column - column) == 1):
                end_case: Case = self.board.grid[line + (1 if actual_case.content.piece_color == PieceColor.WHITE else -1)][last_move.end.column]

                if end_case.content is None:
                    en_passant_moves.append(end_case)

        return en_passant_moves


    def get_color_every_legal_moves(self, color: PieceColor) -> list[Case]:
        if not isinstance(color, PieceColor):
            raise TypeError("get_color_every_legal_moves(self, color) Le paramètre color doit être du type PieceColor.")
        
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
        if not isinstance(move, Move):
            raise TypeError("play_move(self, move) Le paramètre move doit être du type Move.")

        if not isinstance(move.start.content, Piece):
            raise IllegalMoveError("L'attribut start d'un move doit être une case contenant une pièce.")
        
        piece: Piece = move.start.content

        if not piece.piece_color == self.current_player.color:
            raise IllegalMoveError("La couleur de la pièce jouée doit être la même que celle du joueur actuel.")
        
        piece_legal_moves: list[Case] = self.get_legal_moves(move.start.line, move.start.column)

        if not move.end in piece_legal_moves:
            raise IllegalMoveError("L'attribut end d'un move doit être une case atteignable par la pièce contenue dans l'attribut start.")

        self.change_move_type(move)

        if move.special_move != SpecialMove.PROMOTION and move.promotion_piece_type is not None:
            raise ChessError("L'attribut promotion_piece_type du move devrait être None.")
        
        if move.special_move == SpecialMove.PROMOTION and move.promotion_piece_type is None:
            raise ChessError("Aucune type de pièce choisi pour la promotion")

        move.captured_piece = move.end.content

        # En passant
        if move.special_move == SpecialMove.EN_PASSANT:
            move.captured_piece = self.board.grid[move.start.line][move.end.column].content
        
        # Roque
        if move.special_move == SpecialMove.CASTLING:
            rook_case: Case = self.board.grid[move.start.line][7 if move.start.column < move.end.column else 0]
            rook_move: Move = Move(rook_case, self.board.grid[move.start.line][5 if move.start.column < move.end.column else 3])
            self.board.apply_move(rook_move)
            
        self.board.apply_move(move)
        self.moves.append(move)

        # Promotion
        if move.special_move == SpecialMove.PROMOTION and move.promotion_piece_type is not None:
            self.promotion(move.end.line, move.end.column, move.promotion_piece_type)

        self.switch_players()
        self.update_game_status()


    def change_move_type(self, move: Move) -> None:
        if not isinstance(move, Move):
            raise TypeError("change_move_type(self, move) Le paramètre move doit être du type Move.")
        
        if isinstance(move.start.content, King) and abs(move.start.column - move.end.column) == 2:
            move.special_move = SpecialMove.CASTLING

        elif self.is_promotion(move):
            move.special_move = SpecialMove.PROMOTION

        elif move.end in self.get_en_passant_moves(move.start.line, move.start.column):
            move.special_move = SpecialMove.EN_PASSANT

        else:
            move.special_move = SpecialMove.NONE


    def is_promotion(self, move: Move) -> bool:
        return isinstance(move.start.content, Pawn) and (
        (move.start.content.piece_color == PieceColor.WHITE and move.end.line == 7) or
        (move.start.content.piece_color == PieceColor.BLACK and move.end.line == 0))


    def promotion(self, line: int, column: int, new_type: type[Bishop|Knight|Queen|Rook]) -> None:
        is_valid_position(line, column, "promotion(self, line, column, new_type)")

        if new_type not in (Bishop, Knight, Queen, Rook):
            raise ChessError("Promotion : Type de pièce invalide.")
        
        case_content: Piece|None = self.board.grid[line][column].content

        if not isinstance(case_content, Pawn):
            raise ChessError("Promotion : La pièce à promouvoir doit être un pion.")
        
        self.board.grid[line][column].content = new_type(case_content.piece_color)


    def is_50_moves(self) -> bool:
        count: int = 0

        for move in reversed(self.moves):
            if not isinstance(move.moving_piece, Pawn) and move.captured_piece is None:
                count += 1

            else:
                break

        return count >= 100


    def is_insufficient_material(self) -> bool:
        white_pieces: list[Piece] = self.board.get_color_all_pieces(PieceColor.WHITE)
        black_pieces: list[Piece] = self.board.get_color_all_pieces(PieceColor.BLACK)
        white_bishop: None | Bishop = None
        black_bishop: None | Bishop = None

        if len(white_pieces) > 2 or len(black_pieces) > 2:
            return False

        for list_of_pieces in [white_pieces, black_pieces]:
            for piece in list_of_pieces:
                if isinstance(piece, (Pawn, Queen, Rook)):
                    return False

                elif isinstance(piece, Bishop): 
                    if piece.piece_color == PieceColor.WHITE:
                        white_bishop = piece

                    else:
                        black_bishop = piece

        if len(white_pieces) == 2 and len(black_pieces) == 2:
            if white_bishop and black_bishop:
                white_bishop_position: tuple[int, int] | None = self.board.get_piece_position(white_bishop)
                black_bishop_position: tuple[int, int] | None = self.board.get_piece_position(black_bishop)

                if (white_bishop_position and black_bishop_position and
                    (((white_bishop_position[0] + white_bishop_position[1]) % 2 == (black_bishop_position[0] + black_bishop_position[1]) % 2) or
                    ((white_bishop_position[0] + white_bishop_position[1]) % 2 == (black_bishop_position[0] + black_bishop_position[1]) % 2))):
                    return True

            return False

        return True


    def is_stalemate(self, color: PieceColor) -> bool:
        if not isinstance(color, PieceColor):
            raise TypeError("is_stalemate(self, color) Le paramètre color doit être du type PieceColor.")
        
        is_checked: bool = self.board.is_checked(color)
        every_legal_moves: list[Case] = self.get_color_every_legal_moves(color)

        return not is_checked and not every_legal_moves


    def is_checkmate(self, color: PieceColor) -> bool:
        if not isinstance(color, PieceColor):
            raise TypeError("is_checkmate(self, color) Le paramètre color doit être du type PieceColor.")
        
        is_checked: bool = self.board.is_checked(color)
        every_legal_moves: list[Case] = self.get_color_every_legal_moves(color)

        return is_checked and not every_legal_moves


    def update_game_status(self):
        if self.is_checkmate(self.current_player.color):
            self.status = GameStatus.CHECKMATE
            self.switch_players()
            self.game_issue(self.current_player)
            self.end_the_game()

        elif self.board.is_checked(self.current_player.color):
            self.status = GameStatus.CHECK

        elif self.is_stalemate(self.current_player.color):
            self.status = GameStatus.STALEMATE
            self.game_issue(None)
            self.end_the_game()

        elif self.is_insufficient_material():
            self.status = GameStatus.DRAW_INSUFFICIENT_MATERIAL
            self.game_issue(None)
            self.end_the_game()

        elif self.is_50_moves():
            self.status = GameStatus.DRAW_50_MOVES
            self.game_issue(None)
            self.end_the_game()

        else:
            self.status = GameStatus.IN_PROGRESS


    def game_issue(self, winner: Player | None) -> None:
        if not (isinstance(winner, Player) or winner is None):
            raise TypeError("end_the_game(self, winner) Le paramètre winner doit être du type Player.")
        
        self.winner = winner

    
    def end_the_game(self):
        pass