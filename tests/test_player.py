from src.chess.player import Player
from src.chess.pieces.piece import PieceColor
from src.chess.profile import Profile
import pytest

@pytest.fixture
def player_white() -> Player:
    return Player(Profile(), PieceColor.WHITE)

@pytest.fixture
def player_black() -> Player:
    return Player(Profile(), PieceColor.BLACK)

def test_player_white(player_white: Player) -> None:
    assert player_white.color == PieceColor.WHITE

def test_player_black(player_black: Player) -> None:
    assert player_black.color == PieceColor.BLACK