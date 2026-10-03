from src.chess_engine.history import History
from src.chess_engine.move import Move
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.move_generator import MoveGenerator
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import Color, DrawReason, GameStatus
from src.chess_engine.zobrist import Zobrist

class Game:
    """Représente une partie d'échecs.

    Cette classe orchestre les différents composants du moteur afin de gérer
    le déroulement d'une partie. Elle maintient la position actuelle, les
    joueurs, l'historique des coups et le statut de la partie.

    La génération et l'exécution des coups sont déléguées respectivement à
    ``MoveGenerator`` et ``MoveExecutor``. La classe ne contient donc pas
    directement la logique détaillée des règles de déplacement.

    La partie peut être initialisée à partir de n'importe quelle position
    FEN, ce qui permet notamment de démarrer une partie depuis une position
    personnalisée.

    Attributes:
        position: Position actuelle de la partie.
        white_player: Joueur contrôlant les pièces blanches.
        black_player: Joueur contrôlant les pièces noires.
        history: Historique des coups joués et des positions obtenues.
        status: Statut actuel de la partie.
        draw_reason: Raison de la nulle si la partie est terminée par une
            nulle, sinon None.
        _move_generator: Générateur utilisé pour produire les coups légaux.
        _move_executor: Composant utilisé pour appliquer et annuler les
            coups.
        _zobrist: Instance utilisée pour gérer les hashes des positions.
    """

    def __init__(
        self,
        fen: str,
        white_player: Player,
        black_player: Player,
        move_generator: MoveGenerator,
        move_executor: MoveExecutor,
        zobrist: Zobrist,
    ) -> None:
        """Initialise une partie.

        La position initiale est construite à partir de la chaîne FEN fournie.
        Le hash Zobrist de cette position est calculé et utilisé pour
        initialiser l'historique de la partie.

        Args:
            fen: Chaîne représentant la position initiale au format FEN.
            white_player: Joueur contrôlant les pièces blanches.
            black_player: Joueur contrôlant les pièces noires.
            move_generator: Générateur utilisé pour produire les coups
                légaux.
            move_executor: Composant utilisé pour appliquer et annuler les
                coups.
            zobrist: Instance utilisée pour calculer les hashes Zobrist.
        """
        # TODO

    def current_player(self) -> Player:
        """Retourne le joueur dont c'est le tour.

        Returns:
            Le joueur correspondant à la couleur indiquée par
            ``position.side_to_move``.
        """
        # TODO

    def legal_moves(self) -> list[Move]:
        """Retourne les coups légaux de la position actuelle.

        Returns:
            Liste des coups légaux disponibles pour le joueur actif.
        """
        # TODO

    def make_move(self, move: Move) -> None:
        """Joue un coup et met à jour l'état de la partie.

        Le coup est appliqué à la position actuelle, les informations
        nécessaires à son annulation sont ajoutées à l'historique et le hash
        Zobrist obtenu est enregistré.

        Le statut de la partie est ensuite mis à jour.

        Args:
            move: Coup à jouer.
        """
        # TODO

    def undo_move(self) -> None:
        """Annule le dernier coup joué.

        La position, l'historique et les informations associées à la partie
        sont restaurés à leur état précédent.

        Raises:
            IndexError: Si aucun coup n'a été joué dans la partie.
        """
        # TODO

    def update_status(self) -> None:
        """Met à jour le statut de la partie.

        Le statut est déterminé à partir des coups légaux disponibles et
        des différentes conditions de fin de partie, notamment l'échec et
        mat, le pat et les conditions de nulle.
        """
        # TODO