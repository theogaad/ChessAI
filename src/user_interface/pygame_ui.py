import pygame

from src.chess_engine.constants import BOARD_SIZE, CASE_SIZE
from src.chess_engine.game import Game
from src.chess_engine.types import Color, PieceType, EventType
from src.user_interface.ui import UI


class PygameUI(UI):
    """Interface utilisateur graphique basée sur Pygame."""

    def __init__(self) -> None:
        """Initialise Pygame, la fenêtre et les images des pièces."""
        super().__init__()
        pygame.init()
        self._screen: pygame.Surface = pygame.display.set_mode((BOARD_SIZE * CASE_SIZE, BOARD_SIZE * CASE_SIZE))
        self._images: dict[tuple[Color, PieceType], pygame.Surface] = {}

        for color in Color:
            for piece_type in PieceType:
                self._images[(color, piece_type)] = pygame.image.load(
                    self.piece_to_image_filename(color, piece_type)
                )
                self._images[(color, piece_type)] = pygame.transform.scale(
                    self._images[(color, piece_type)], 
                    (CASE_SIZE, CASE_SIZE)
                )

    def exit(self) -> None:
        pygame.quit()

    def display_position(self, game: Game) -> None:
        """Affiche la position actuelle de la partie.

        Args:
            game: Partie dont la position doit être affichée.
        """
        self.display_board()

        for rank in range(BOARD_SIZE):
            for file in range(BOARD_SIZE):
                square: int = rank * BOARD_SIZE + file
                square_content: tuple[Color, PieceType] | None = game.position.piece_bitboards.get_piece_at(square)

                if square_content is not None:
                    self.display_piece(square_content, square)

        pygame.display.flip()

    def update_event(self) -> int | None:
        """Met à jour l'attribut event."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.event = EventType.QUIT
                return None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.event = EventType.CLICK
                clicked_square: int = self.pygame_coordinate_to_square(event.pos)
                return clicked_square

        self.event = EventType.NONE
        return None

    def display_board(self) -> None:
        """Affiche le plateau de jeu."""
        for rank in range(BOARD_SIZE):
            for file in range(BOARD_SIZE):
                square: int = rank * BOARD_SIZE + file
                pygame_color: tuple[int, int, int] = (100, 100, 100) if (rank + file) % 2 == 0 else (255, 255, 255)
                case_x, case_y = self.square_to_pygame_coordinate(square)
                pygame.draw.rect(
                    self._screen, 
                    pygame_color, 
                    (case_x, case_y, CASE_SIZE, CASE_SIZE)
                )

    def display_piece(self, piece: tuple[Color, PieceType], square: int) -> None:
        """Affiche une pièce sur une case du plateau.
        
        Args:
            piece: Couleur et type de la pièce à afficher.
            square: Indice de la case sur laquelle afficher la pièce.
        """
        self._screen.blit(self._images[piece], self.square_to_pygame_coordinate(square))

    def square_to_pygame_coordinate(self, square: int) -> tuple[int, int]:
        """Convertit un indice de case en coordonnées Pygame.
        
        Args:
            square: Indice de la case selon la convention du moteur.
        
        Returns:
            Coordonnées ``(x, y)`` correspondant au coin supérieur gauche 
            de la case dans la fenêtre Pygame.
        """
        return (
            (BOARD_SIZE - (square % BOARD_SIZE) - 1) * CASE_SIZE, 
            (square // BOARD_SIZE) * CASE_SIZE
        )

    def pygame_coordinate_to_square(self, pygame_position: tuple[int, int]) -> int:
        """Convertit des coordonnées Pygame en indice de case.
        
        Args:
            pygame_position: Coordonnées Pygame à convertir.
        
        Returns:
            Indice de la case correspondant aux coordonnées Pygame reçues.
        """
        file, rank = pygame_position
        file = BOARD_SIZE - (file // CASE_SIZE) - 1
        rank = rank // CASE_SIZE

        return rank * BOARD_SIZE + file