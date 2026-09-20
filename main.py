from src.chess.game import Game
from src.chess.profile import Profile
from src.chess.ui.pygame_chess_game_ui import pygame_main
from src.chess.utils import verify_type

#pygame_main(Game([Profile(), Profile()]))
def test(a: int):
    verify_type(a, int, "test(a)")

test(1)
