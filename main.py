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
from src.chess.position import Position
from src.chess.profile import Profile
from src.chess.utils import WHITE, BLACK, PieceColor, GameStatus


def random_moves() -> None:
    game: Game = Game((Profile(), Profile()))
    while game.status == GameStatus.ONGOING:
        available_pieces: list[Case] = game.board.get_cases_of_piece_type_and_color(
            (Bishop, King, Knight, Pawn, Queen, Rook), game.current_player.color
        )
        start_case: Case = choice(available_pieces)

        while not game.get_legally_reachable_cases_from_position(start_case.position) and available_pieces:
            available_pieces.remove(start_case)
            start_case = choice(available_pieces)

        if available_pieces:
            end_case: Case = choice(game.get_legally_reachable_cases_from_position(start_case.position))
            move: Move = Move(start_case, end_case)

            game.apply_move(move)
    print(game.status)

no_error = True
while no_error:
    try:
        random_moves()
    except:
        no_error = False