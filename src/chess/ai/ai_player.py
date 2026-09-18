from random import choice, randint
from src.chess.case import Case
from src.chess.game import Game
from src.chess.move import Move
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.knight import Knight
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook

class AIPlayer():
    def __init__(self):
        pass

    def play_random_move(self, game: Game):
        list_of_pieces: list[Piece] = game.board.get_color_all_pieces(game.current_player.color)
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