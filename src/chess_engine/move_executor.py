from src.chess_engine.position import Position
from src.chess_engine.move import Move
from src.chess_engine.undo_info import UndoInfo
from src.chess_engine.zobrist import Zobrist


class MoveExecutor:
    """Applique et annule les coups sur une position.

    Cette classe est responsable de modifier une position lors de
    l'application d'un coup et de restaurer son état précédent lors de
    l'annulation du coup.

    Elle gère notamment les déplacements normaux, les captures, les
    promotions, les roques et les captures en passant, ainsi que la mise à
    jour des informations associées à la position.

    Le hash Zobrist est également mis à jour lors de l'application d'un coup
    et restauré lors de son annulation.

    La classe ne vérifie pas si un coup est légal. Les préconditions
    nécessaires à l'exécution d'un coup sont supposées être respectées par
    l'appelant.

    Attributes:
        _zobrist: Instance utilisée pour calculer et mettre à jour le hash
            Zobrist des positions.
    """

    def __init__(self, zobrist: Zobrist) -> None:
        """Initialise l'exécuteur de coups.

        Args:
            zobrist: Instance utilisée pour gérer le hash Zobrist.
        """
        # TODO

    def make_move(self, position: Position, move: Move) -> UndoInfo:
        """Applique un coup à une position.

        L'état nécessaire à l'annulation du coup est sauvegardé avant toute
        modification de la position.

        Args:
            position: Position sur laquelle appliquer le coup.
            move: Coup à appliquer.

        Returns:
            Informations permettant d'annuler le coup avec ``undo_move``.
        """
        # TODO

    def undo_move(
        self,
        position: Position,
        move: Move,
        undo_info: UndoInfo,
    ) -> None:
        """Annule un coup précédemment appliqué à une position.

        La position est restaurée à l'état qu'elle avait avant l'application
        du coup.

        Args:
            position: Position ayant subi le coup.
            move: Coup à annuler.
            undo_info: Informations sauvegardées lors de l'application du
                coup.
        """
        # TODO