from random import choice

from src.chess_engine.move import Move
from src.chess_engine.player import Player
from src.chess_engine.position import Position


class AI(Player):
    def __init__(self, color):
        super().__init__(color)

    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move | None:
        """Choisit un coup parmi les coups légaux disponibles.

        Args:
            position: Position actuelle de la partie.
            legal_moves: Liste des coups légaux disponibles.

        Returns:
            Le coup choisi par l'ia.
        """
        if len(legal_moves) > 0:
            return choice(legal_moves)

        return None