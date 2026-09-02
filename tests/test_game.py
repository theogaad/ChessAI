from src.chess.game import Game
from src.chess.board import Board
from src.chess.profile import Profile
from src.chess.pieces.piece import PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
import pytest

@pytest.fixture
def normal_game() -> Game:
    profiles: list[Profile] = [Profile(), Profile()]
    return Game(profiles)

@pytest.fixture
def game_with_empty_board() -> Game:
    profiles: list[Profile] = [Profile(), Profile()]
    game = Game(profiles)
    game.board = Board()
    return game

def test_game_correct_number_of_players(normal_game: Game):
    assert len(normal_game.players) == 2

@pytest.mark.parametrize("profiles", [
    ([]),
    ([Profile()]),
    ([Profile(), Profile(), Profile()])
])
def test_game_incorrect_number_of_players(profiles: list[Profile]):
    with pytest.raises(ValueError):
        Game(profiles)

def test_game_player_color(normal_game: Game):
    colors = [player.color for player in normal_game.players]
    assert colors.count(PieceColor.WHITE) == 1
    assert colors.count(PieceColor.BLACK) == 1

def test_game_current_player_is_one_of_the_players(normal_game: Game):
    assert normal_game.current_player in normal_game.players

def test_game_current_player_is_white(normal_game: Game):
    assert normal_game.current_player.color == PieceColor.WHITE

def test_game_winner_is_none(normal_game: Game):
    assert normal_game.winner is None

def test_game_moves_is_empty(normal_game: Game):
    assert normal_game.moves == []

@pytest.mark.parametrize("line, column, expected_legal_moves", [
    (0, 4, [(1, 5), (0, 5), (0, 3), (1, 3)]),
    (4, 7, [(7, 4), (1, 4)]),
    (4, 1, [(4, 4), (7, 4), (1, 4)])
])
def test_game_get_legal_moves(game_with_empty_board: Game, line: int, column: int, expected_legal_moves: list[tuple[int, int]]):
    game_with_empty_board.board.grid[0][4].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[4][7].content = Bishop(PieceColor.WHITE)
    game_with_empty_board.board.grid[4][1].content = Queen(PieceColor.WHITE)
    game_with_empty_board.board.grid[7][4].content = Rook(PieceColor.BLACK)

    assert game_with_empty_board.get_legal_moves(line, column) == [game_with_empty_board.board.grid[move[0]][move[1]] for move in expected_legal_moves]

