from src.chess.game import Game
from src.chess.profile import Profile
from src.chess.pieces.piece import PieceColor
import pytest

@pytest.fixture
def normal_game() -> Game:
    profiles: list[Profile] = [Profile(), Profile()]
    return Game(profiles)

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