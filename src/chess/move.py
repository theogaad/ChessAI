from dataclasses import dataclass
from src.chess.case import Case
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.knight import Knight
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.utils import MoveType, verify_type



@dataclass
class Move:
    """Représente un mouvement aux échecs.
    
    Attributes:
        start_case: Case de départ de la pièce qui effectue le mouvement.
        end_case: Case d'arrivée de la pièce qui effectue le mouvement.
        move_type: Type de mouvement effectué.
        promotion_piece_type: Nouveau type de la pièce dans l'evantualité d'une promotion.
        captured_piece: Pièce éventuellement capturée lors du mouvement.
        moving_piece: Pièce effectuant le mouvement.

    Les propriétés ``captured_piece`` et ``moving_piece`` sont déterminées à partir des autres propriétés.
    """
    __start_case: Case
    __end_case: Case
    __move_type: MoveType = MoveType.NORMAL
    __promotion_piece_type: None | type[Bishop | Knight | Queen | Rook] = None


    def __post_init__(self) -> None:
        """Vérifie le type de tous les propriétés et initialise les propriétés ``captured_piece`` et ``moving_piece``.
        
        Raises:
            TypeError: Si une des propriétés n'est pas du type attendu ou si la case de départ de contient pas de pièce.
        """
        verify_type(self.start_case, Case, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "start_case")
        verify_type(self.end_case, Case, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "end_case")
        verify_type(self.move_type, MoveType, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "move_type")
        verify_type(self.promotion_piece_type, (Bishop, Knight, Queen, Rook), "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "promotion_piece_type", or_none=True)
        verify_type(self.end_case.content, Piece, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "end_case.content")

        # Obligé de garder cette vérification sous la forme if isinstance() 
        # pour pouvoir initialiser moving_piece en satisfaisant mypy.
        if not isinstance(self.start_case.content, Piece):
            raise TypeError("Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None) Le paramètre start_case.content doit être du type Piece.")

        self.captured_piece: None | Piece = self.end_case.content
        self.moving_piece: Piece = self.start_case.content


    def __repr__(self) -> str:
        """Retourne la représentation textuelle d'un mouvement."""
        return f"Move[{self.start_case.position} -> {self.end_case.position}, {self.moving_piece}, capture: {self.captured_piece}, type: {self.move_type}, promotion: {self.promotion_piece_type}]"


    @property
    def start_case(self) -> Case:
        """Retourne la case de départ."""
        return self.__start_case

    @start_case.setter
    def start_case(self, new_start_case: Case) -> None:
        """Modifie la case de départ.
        
        Args:
            new_start_case: Nouvelle case de départ.
        
        Raises:
            TypeError: Si ``new_start_case`` n'est pas une instance de ``Case``.
        """
        verify_type(new_start_case, Case, "start_case(new_start_case)", "new_start_case")

        self.start_case = new_start_case

    @property
    def end_case(self) -> Case:
        """Retourne la case d'arrivée."""
        return self.__end_case

    @end_case.setter
    def end_case(self, new_end_case: Case) -> None:
        """Modifie la case d'arrivée.

        Args:
            new_end_case: Nouvelle case d'arrivée.
        
        Raises:
            TypeError: Si ``new_end_case`` n'est pas une instance de ``Case``.
        """
        verify_type(new_end_case, Case, "end_case(new_end_case)", "new_end_case")

        self.__end_case = new_end_case

    @property
    def move_type(self) -> MoveType:
        """Retourne le type du mouvement."""
        return self.__move_type

    @move_type.setter
    def move_type(self, new_move_type: MoveType) -> None:
        """Modifie le type du mouvement.
        
        Args:
            new_move_type: Nouveau type du mouvement.
        
        Raises:
            TypeError: Si ``new_move_type`` n'est pas une instance de ``MoveType``.
        """
        verify_type(new_move_type, MoveType, "move_type(new_move_type)", "new_move_type")

        self.__move_type = new_move_type

    @property
    def promotion_piece_type(self) -> None | type[Bishop | Knight | Queen | Rook]:
        """Retourne le type de la pièce effectuant le mouvement après une éventuelle promotion ou 'None'."""
        return self.__promotion_piece_type

    @promotion_piece_type.setter
    def promotion_piece_type(self, new_promotion_piece_type: None | type[Bishop | Knight | Queen | Rook]) -> None:
        """Modifie le type de la pièce effectuant le mouvement après une éventuelle promotion.
        
        Args:
            new_promotion_piece_type: Nouveau type de la pièce effectuant le mouvement après une éventuelle promotion.

        Raises:
            TypeError: Si new_promotion_piece_type n'est pas du type attendu.
        """
        verify_type(new_promotion_piece_type, (Bishop, Knight, Queen, Rook), "promotion_piece_type(new_promotion_piece_type)", "new_promotion_piece_type", or_none=True)

        self.__promotion_piece_type = new_promotion_piece_type

    @property
    def captured_piece(self) -> None | Piece:
        """Retourne une éventuelle pièce capturée ou 'None'."""
        return self.__captured_piece

    @captured_piece.setter
    def captured_piece(self, new_captured_piece) -> None:
        """Modifie l'éventuelle pièce capturée.
        
        Args:
            new_captured_piece: Nouvelle pièce capturée ou 'None'.
        
        Raises:
            TypeError: Si ``new_captured_piece`` n'est ni de type ``None`` ni une instance de ``Piece``. 
        """
        verify_type(new_captured_piece, Piece, "capture_piece(new_captured_piece)", "new_captured_piece", or_none=True)

        self.__captured_piece = new_captured_piece

    @property
    def moving_piece(self) -> Piece:
        """Retourne la pièce qui effectue le mouvement."""
        return self.__moving_piece

    @moving_piece.setter
    def moving_piece(self, new_moving_piece: Piece):
        """Modifie la pièce qui effectue le mouvement.
        
        Args:
            new_moving_piece: Nouvelle pièce effectuant le mouvement.
        
        Raises:
            TypeError: Si ``new_moving_piece`` n'est pas une instance de ``Piece``.
        """
        verify_type(new_moving_piece, Piece, "moving_piece(new_moving_piece)", "new_move_piece")

        self.__moving_piece = new_moving_piece