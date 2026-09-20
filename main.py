from src.chess.game import Game
from src.chess.profile import Profile
from src.chess.ui.pygame_chess_game_ui import pygame_main

pygame_main(Game([Profile(), Profile()]))