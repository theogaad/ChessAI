from src.chess_engine.history import History
from src.chess_engine.move import Move
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.move_generator import MoveGenerator
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType, MoveType, GameStatus, DrawReason
from src.chess_engine.undo_info import UndoInfo
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
        legal_moves: Liste des coups légaux de la position actuelle.
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
        self.position: Position = Position(fen)
        zobrist_hash: int = zobrist.hash_position(self.position)
        self.position.zobrist_hash = zobrist_hash
        self.white_player: Player = white_player
        self.black_player: Player = black_player
        self.history: History = History(zobrist_hash)
        self.status: GameStatus = GameStatus.ONGOING
        self.draw_reason: DrawReason | None = None
        self._move_generator: MoveGenerator = move_generator
        self._move_executor: MoveExecutor = move_executor
        self.legal_moves: list[Move] = self.get_legal_moves()
        self.update_status()

    def current_player(self) -> Player:
        """Retourne le joueur dont c'est le tour.

        Returns:
            Le joueur correspondant à la couleur indiquée par
            ``position.side_to_move``.
        """
        if self.position.side_to_move is Color.WHITE:
            return self.white_player
        return self.black_player

    def get_legal_moves(self) -> list[Move]:
        """Retourne les coups légaux de la position actuelle.

        Returns:
            Liste des coups légaux disponibles pour le joueur actif.
        """
        return self._move_generator.generate_legal_moves(self.position)

    def make_move(self, move: Move) -> None:
        """Joue un coup et met à jour l'état de la partie.

        Le coup est appliqué à la position actuelle, les informations
        nécessaires à son annulation sont ajoutées à l'historique et le hash
        Zobrist obtenu est enregistré.

        Le statut de la partie est ensuite mis à jour.

        Args:
            move: Coup à jouer.
        
        Raises:
            ValueError: Si le mouvement n'est pas légal.
        """
        if move not in self.legal_moves:
            raise ValueError("Le mouvement n'est pas légal.")
        
        undo_info: UndoInfo = self._move_executor.make_move(self.position, move)
        self.history.add(
            move, 
            undo_info, 
            self.position.zobrist_hash
        )
        self.legal_moves = self.get_legal_moves()
        self.update_status()

    def undo_move(self) -> None:
        """Annule le dernier coup joué.

        La position, l'historique et les informations associées à la partie
        sont restaurés à leur état précédent.

        Raises:
            IndexError: Si aucun coup n'a été joué dans la partie.
        """
        self._move_executor.undo_move(
            self.position, 
            self.history.get_last_move(), 
            self.history.get_last_undo_info()
        )
        self.history.remove_last()
        self.legal_moves = self.get_legal_moves()
        self.update_status()

    def update_move_type(self, move: Move) -> Move:
        """Retourne le move donné en mettant à jour son attribut MoveType.
        
        Args:
            move: Move dont l'attribut est mis à jour.

        Returns:
            Le move avec l'attribut MoveType mis à jour.
        """
        updated_move: Move = move
        
        for move_type in MoveType:
            updated_move.move_type = move_type

            if updated_move in self.legal_moves:
                return updated_move

        return move


    def update_status(self) -> None:
        """Met à jour le statut de la partie.

        Le statut est déterminé à partir des coups légaux disponibles et
        des différentes conditions de fin de partie, notamment l'échec et
        mat, le pat et les conditions de nulle.
        """
        self.status = GameStatus.ONGOING
        self.draw_reason = None

        if len(self.legal_moves) == 0:
            if self._move_generator.is_king_in_check(self.position, self.position.side_to_move):
                self.status = GameStatus.CHECKMATE

            else:
                self.status = GameStatus.STALEMATE

        elif self.history.count_position(self.position.zobrist_hash) >= 3:
            self.status = GameStatus.DRAW
            self.draw_reason = DrawReason.REPETITION

        elif self.position.halfmove_clock >= 100:
            self.status = GameStatus.DRAW
            self.draw_reason = DrawReason.FIFTY_MOVES

        elif self.is_insufficient_material():
            self.status = GameStatus.DRAW
            self.draw_reason = DrawReason.INSUFFICIENT_MATERIAL

    def is_insufficient_material(self) -> bool:
        """Indique si la position contient un matériel insuffisant pour mater.
        
        Une position est considérée comme ayant un matériel insuffisant lorsque 
        aucun des joueurs ne possède de pion, de tour ou de dame et que la 
        configuration restante ne permet pas de réaliser un échec et mat.
        
        Les configurations prises en compte comprennent notamment les positions 
        roi contre roi, roi et cavalier contre roi, roi et fou contre roi, ainsi 
        que les positions où chaque joueur ne possède qu'un fou et que les deux 
        fous évoluent sur des cases de même couleur.
        
        Returns: 
            ``True`` si le matériel est insuffisant pour réaliser un échec et mat, 
            sinon ``False``.
        """
        for color in Color:
            for piece_type in [
                PieceType.QUEEN, 
                PieceType.ROOK, 
                PieceType.PAWN
            ]:
                if self.position.piece_bitboards.get_bitboard(color, piece_type) != 0:
                    return False

        pieces_count: int = self.position.piece_bitboards.occupied.bit_count()
        if pieces_count <= 3:
            return True

        white_knights_count: int = self.position.piece_bitboards.get_bitboard(Color.WHITE, PieceType.KNIGHT).bit_count()
        black_knights_count: int = self.position.piece_bitboards.get_bitboard(Color.BLACK, PieceType.KNIGHT).bit_count()
        white_bishops_count: int = self.position.piece_bitboards.get_bitboard(Color.WHITE, PieceType.BISHOP).bit_count()
        black_bishops_count: int = self.position.piece_bitboards.get_bitboard(Color.BLACK, PieceType.BISHOP).bit_count()
        knights_count: int = white_knights_count + black_knights_count
        
        white_bishop_square: int = self.position.piece_bitboards.get_bitboard(Color.WHITE, PieceType.BISHOP).bit_length() - 1
        black_bishop_square: int = self.position.piece_bitboards.get_bitboard(Color.BLACK, PieceType.BISHOP).bit_length() - 1
        if (knights_count == 0 and white_bishops_count == 1 and black_bishops_count == 1 and
            abs(white_bishop_square - black_bishop_square) % 2 == 0):
            return True

        return False