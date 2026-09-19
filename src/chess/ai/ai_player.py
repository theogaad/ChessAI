from copy import deepcopy
from random import choice, randint
from src.chess.case import Case
from src.chess.constants import BISHOP_VALUE, KNIGHT_VALUE, PAWN_VALUE, QUEEN_VALUE, ROOK_VALUE
from src.chess.game import Game
from src.chess.move import Move
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.player import Player
from src.chess.profile import Profile



class AIPlayer(Player):
    def __init__(self, profile: Profile, color: PieceColor):
        super().__init__(profile, color)


    def play_random_move(self, game: Game) -> None:
        list_of_pieces: list[Piece] = game.board.get_color_all_pieces(self.color)

        while list_of_pieces:
            random_index: int = randint(0, len(list_of_pieces) - 1)
            piece_position: None | tuple[int, int] = game.board.get_piece_position(list_of_pieces[random_index])

            if piece_position is not None:
                piece_possible_moves: list[Case] = game.get_legal_moves(piece_position[0], piece_position[1])

                if piece_possible_moves:
                    move: Move = Move(game.board.grid[piece_position[0]][piece_position[1]], choice(piece_possible_moves))

                    if game.is_promotion(move):
                        possible_promotions: list[type] = [Bishop, Knight, Queen, Rook]
                        move.promotion_piece_type = choice(possible_promotions)

                    game.play_move(move)
                    break

                else:
                    list_of_pieces.pop(random_index)


    def minimax_depth_1(self, game: Game) -> None:
        list_of_move_values: list[tuple[int, Move]] = self.get_list_of_move_values(game, self.color)

        if list_of_move_values:
            list_of_move_values.sort(key=lambda x: x[0], reverse=True)

            if list_of_move_values[0][0] == list_of_move_values[-1][0]:
                game.play_move(list_of_move_values[0][1])

            else:
                game.play_move(list_of_move_values[0][1])


    def minimax_depth_2(self, game: Game) -> None:
        list_of_move_values: list[tuple[int, Move]] = self.get_list_of_move_values(game, self.color)

        for i in range(len(list_of_move_values)):
            list_of_enemy_move_values: list[tuple[int, Move]] = \
            self.get_list_of_move_values(self.apply_move(game, list_of_move_values[i][1]), 
                                         PieceColor.WHITE if self.color == PieceColor.BLACK else PieceColor.BLACK)

            if not list_of_enemy_move_values:
                game.play_move(list_of_move_values[i][1])

            else:
                list_of_enemy_move_values.sort(key=lambda x: x[0])
                list_of_move_values[i] = (list_of_enemy_move_values[0][0], list_of_move_values[i][1])

        if list_of_move_values:
            list_of_move_values.sort(key=lambda x: x[0], reverse=True)

            if list_of_move_values[0][0] == list_of_move_values[-1][0]:
                game.play_move(choice(list_of_move_values)[1])

            else:
                game.play_move(list_of_move_values[0][1])


    def apply_move(self, game: Game, move: Move) -> Game:
        game_copy: Game = deepcopy(game)
        new_move_start: Case = game_copy.board.grid[move.start.line][move.start.column]
        new_move_end: Case = game_copy.board.grid[move.end.line][move.end.column]
        new_move: Move = Move(new_move_start, new_move_end, move.special_move, move.promotion_piece_type, move.captured_piece)

        game_copy.play_move(new_move)

        return game_copy


    def get_pieces_value(self, pieces: list[Piece]) -> int:
        pieces_values: dict[type[Piece], int] = {
            Bishop: BISHOP_VALUE,
            Knight: KNIGHT_VALUE,
            Pawn: PAWN_VALUE,
            Queen: QUEEN_VALUE,
            Rook: ROOK_VALUE,
            King: 0
        }

        value: int = 0

        for piece in pieces:
            value += pieces_values[type(piece)]

        return value


    def get_board_value(self, game: Game) -> int:
        ai_pieces: list[Piece] = game.board.get_color_all_pieces(self.color)
        enemy_pieces: list[Piece] = game.board.get_color_all_pieces(PieceColor.WHITE if self.color == PieceColor.BLACK else PieceColor.BLACK)
        ai_value: int = self.get_pieces_value(ai_pieces)
        enemy_value: int = self.get_pieces_value(enemy_pieces)

        return ai_value - enemy_value


    def get_list_of_move_values(self, game: Game, color: PieceColor) -> list[tuple[int, Move]]:
        list_of_pieces: list[Piece] = game.board.get_color_all_pieces(color)
        list_of_values: list[tuple[int, Move]] = []

        for piece in list_of_pieces:
            piece_position: None | tuple[int, int] = game.board.get_piece_position(piece)

            if piece_position is not None:
                piece_possible_moves: list[Case] = game.get_legal_moves(piece_position[0], piece_position[1])

                for possible_move in piece_possible_moves:
                    move: Move = Move(game.board.grid[piece_position[0]][piece_position[1]], possible_move)

                    if game.is_promotion(move):
                        possible_promotions: list[type] = [Bishop, Knight, Queen, Rook]
                        for promotion in possible_promotions:
                            move.promotion_piece_type = promotion
                            game_after_move: Game = self.apply_move(game, move)
                            list_of_values.append((self.get_board_value(game_after_move), move))

                    else:
                        game_after_move = self.apply_move(game, move)
                        list_of_values.append((self.get_board_value(game_after_move), move))

        return list_of_values