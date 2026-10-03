from src.chess_engine.position import Position
from src.chess_engine.move import Move
from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.move_executor import MoveExecutor


class MoveGenerator:
    """Génère les coups légaux d'une position d'échecs.

    Cette classe génère les coups pseudo-légaux des pièces présentes sur une
    position, puis élimine les coups qui laissent le roi du joueur actif en
    échec.

    Elle s'appuie sur ``AttackGenerator`` pour déterminer les cases
    contrôlées par les pièces et sur ``MoveExecutor`` pour appliquer
    temporairement les coups et vérifier la sécurité du roi.

    La classe gère notamment les déplacements normaux, les captures, les
    déplacements de pions, les promotions, les captures en passant et les
    roques.

    Attributes:
        _attack_generator: Générateur utilisé pour déterminer les cases
            attaquées par les pièces.
        _move_executor: Exécuteur utilisé pour appliquer et annuler les coups
            lors de la vérification de leur légalité.
    """

    def __init__(
        self,
        attack_generator: AttackGenerator,
        move_executor: MoveExecutor,
    ) -> None:
        """Initialise le générateur de coups.

        Args:
            attack_generator: Générateur utilisé pour calculer les attaques.
            move_executor: Exécuteur utilisé pour appliquer et annuler les
                coups.
        """
        # TODO

    def generate_legal_moves(self, position: Position) -> list[Move]:
        """Génère tous les coups légaux d'une position.

        Les coups pseudo-légaux sont générés puis vérifiés afin de s'assurer
        qu'ils ne laissent pas le roi du joueur actif en échec.

        Args:
            position: Position pour laquelle les coups doivent être générés.

        Returns:
            Liste des coups légaux disponibles dans la position.
        """
        # TODO