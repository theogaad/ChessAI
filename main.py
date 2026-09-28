from random import choice
from src.ai.ai import Ai
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
from src.ui.game_ui import GameUi

def random_moves(number: int, game: Game, game_ui: GameUi) -> None:
    for _ in range(number):
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

        if game.status != GameStatus.ONGOING:
            break

        game_ui.display_game()

    print(game.status)

def ai_vs_ai() -> GameUi:
    game: Game = Game((Profile(), Profile()))
    ai = Ai()
    ui: GameUi = GameUi(game)
    ui.display_game()

    while game.status == GameStatus.ONGOING:
        white_move: Move = choice(ai.minimax(2, game, WHITE))
        game.apply_move(white_move)
        ui.display_game()
        black_move: Move = choice(ai.minimax(1, game, BLACK))
        game.apply_move(black_move)
        ui.display_game()
    print(game.status)
    return ui

#no_repetition = True
#while no_repetition:
    #no_repetition = random_moves() != GameStatus.DRAW_REPETITION
def test() -> None:
    test_game = Game((Profile(), Profile()))
    test_ui: GameUi = GameUi(test_game)
    random_moves(100, test_game, test_ui)
    test_ai = Ai()
    #test_game.apply_move(Move(test_game.board.get_case(Position(0, 1)), test_game.board.get_case(Position(2, 2))))
    test_move: Move = choice(test_ai.minimax(2, test_game, WHITE))
    print(test_move)
    test_ui.freeze()

#ai_vs_ai().display_game()
#test()

def special_board() -> None:
    game: Game = Game((Profile(), Profile()))
    game.board.empty_the_board()

for i in range(24000000):
    print(i)
print("ok")