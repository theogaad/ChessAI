from random import choice
from src.chess.board import Board
from src.chess.case import Case
from src.chess.game import Game
from src.chess.move import Move
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.player import Player
from src.chess.position import Position
from src.chess.utils import PieceColor, MoveType, GameStatus, INF, CHECKMATE, PROMOTION_VALUE, CAPTURE_VALUE, NORMAL_VALUE, verify_type, get_opposite_color



class Ai:
    def __init__(self) -> None:
        pass


    def minimax_recursive(
        self, 
        depth: int, 
        game: Game, 
        color: PieceColor,
        alpha: int,
        beta: int
    ):
        if game.status != GameStatus.ONGOING:
            checkmate_player: None | Player = game.is_checkmate()[1]
            if (isinstance(checkmate_player, Player) and 
                checkmate_player.is_color(color)):
                return -CHECKMATE

            elif (isinstance(checkmate_player, Player) and 
                checkmate_player.is_color(get_opposite_color(color))):
                return CHECKMATE

            elif game.is_check(color):
                return -1

            elif game.is_check(get_opposite_color(color)):
                return 1

            else:
                return 0

        elif depth == 0:
            return (
                game.board.get_board_value_of_color(color) - 
                game.board.get_board_value_of_color(get_opposite_color(color))
                )

        elif game.current_player.is_color(color):
            best_board_value: int = -INF

            for ai_move in self.move_ordering(self.generate_moves_of_color(color, game), reverse_values=True):
                ancient_has_moved: bool = game.board.apply_move(ai_move)
                game.switch_current_player()

                game.update_game_status_and_end_the_game()
                new_ai_board_value: int = self.minimax_recursive(depth - 1, game, color, alpha, beta)

                best_board_value = max(new_ai_board_value, best_board_value)

                alpha = max(best_board_value, alpha)

                game.board.unapply_move(ai_move, ancient_has_moved)
                game.switch_current_player()
                game.update_game_status_and_end_the_game()

                if alpha >= beta:
                    break

            return best_board_value 

        else:
            worst_board_value: int = INF

            for enemy_move in self.move_ordering(self.generate_moves_of_color(get_opposite_color(color), game)):
                ancient_has_moved = game.board.apply_move(enemy_move)
                game.switch_current_player()

                game.update_game_status_and_end_the_game()
                new_enemy_board_value: int = self.minimax_recursive(depth - 1, game, color, alpha, beta)

                worst_board_value = min(new_enemy_board_value, worst_board_value)

                beta = min(worst_board_value, beta)

                game.board.unapply_move(enemy_move, ancient_has_moved)
                game.switch_current_player()
                game.update_game_status_and_end_the_game()

                if alpha < beta:
                    break

            return worst_board_value 


    def minimax(self, depth: int, game: Game, color: PieceColor) -> list[Move]:
        alpha: int = -INF
        beta: int = INF
        best_value: int = -INF
        values_moves: list[tuple[int, Move]] = []
        best_moves: list[Move] = []

        for move in self.move_ordering(self.generate_moves_of_color(color, game,), reverse_values=True):
            ancient_has_moved: bool = game.board.apply_move(move)
            game.switch_current_player()

            game.update_game_status_and_end_the_game()
            new_board_value: int = self.minimax_recursive(depth - 1, game, color, alpha, beta)

            game.board.unapply_move(move, ancient_has_moved)
            game.switch_current_player()
            game.update_game_status_and_end_the_game()

            if new_board_value > best_value:
                best_value = new_board_value

            alpha = max(best_value, alpha)

            values_moves.append((new_board_value, move))

            if alpha >= beta:
                break

        for value_move in values_moves:
            if value_move[0] == best_value:
                best_moves.append(value_move[1])

        return best_moves


    def generate_moves_of_color(
        self, 
        color: PieceColor, 
        game: Game
    ) -> list[Move]:
        move_list: list[Move] = []
        pieces_cases: list[Case] = game.board.get_cases_of_piece_type_and_color((Bishop, King, Knight, Pawn, Queen, Rook), color)

        for piece_case in pieces_cases:
            piece_reachable_cases: list[Case] = game.get_legally_reachable_cases_from_position(piece_case.position)

            for piece_reachable_case in piece_reachable_cases:
                move: Move = Move(piece_case, piece_reachable_case)

                if game.is_promotion(move):
                    for piece_type in (Bishop, Knight, Queen, Rook):
                        promotion_move: Move = Move(piece_case, piece_reachable_case, MoveType.PROMOTION, piece_type)
                        move_list.append(promotion_move)

                else:
                    game.update_move_type_and_properties(move)
                    move_list.append(move)

        return move_list

    
    def move_ordering(
        self, 
        move_list: list[Move], 
        reverse_values: bool = False
    ) -> list[Move]:
        value_move_list: list[tuple[int, Move]] = []

        for move in move_list:
            move_value: int = 0

            if move.promotion_piece_type:
                move_value += PROMOTION_VALUE

                if move.captured_piece:
                    move_value += CAPTURE_VALUE

            elif move.captured_piece:
                move_value += CAPTURE_VALUE

            else:
                move_value += NORMAL_VALUE

            value_move_list.append((move_value, move))

        value_move_list.sort(key=lambda x: x[0], reverse=reverse_values)

        return [ordered_move[1] for ordered_move in value_move_list]