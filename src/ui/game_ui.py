from src.chess.game import Game
from src.chess.mapping import chess_line_to_pygame_line, chess_position_to_pygame_position, pygame_line_to_chess_line, pygame_position_to_chess_position, piece_type_to_image_name
from src.chess.pieces.piece import Piece
from src.chess.position import Position
from src.chess.utils import BOARD_SIZE, CASE_SIZE
import pygame



class GameUi:
    def __init__(self, game: Game):
        pygame.init()
        self.game: Game = game
        self.game_screen = pygame.display.set_mode((BOARD_SIZE * CASE_SIZE - 1, BOARD_SIZE * CASE_SIZE - 1))
        

    def display_game(self) -> None:
        self.display_empty_cases()
        self.display_pieces()
        pygame.display.flip()


    def display_empty_cases(self) -> None:
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i + j) % 2 == 0:
                    color = (50, 50, 50)

                else:
                    color = (255, 255, 255)

                pygame.draw.rect(self.game_screen, color, (i * CASE_SIZE, chess_line_to_pygame_line(j), CASE_SIZE, CASE_SIZE))


    def display_pieces(self) -> None:
        for row in self.game.board.grid:
            for case in row:
                if case.contains_a_piece():
                    self.display_piece(case.position)


    def display_piece(self, position: Position) -> None:
        piece: Piece = self.game.board.get_piece(position)
        piece_image: pygame.Surface = pygame.image.load(f"images/pieces/{piece_type_to_image_name(piece)}.png")
        piece_image = pygame.transform.scale(piece_image, (CASE_SIZE, CASE_SIZE))

        pygame_position: tuple[int, int] = chess_position_to_pygame_position(position)
        self.game_screen.blit(piece_image, (pygame_position[0], pygame_position[1]))


    def freeze(self) -> None:
        running: bool = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()