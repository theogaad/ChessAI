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
    """Dataclass représentant un coup aux échecs.
    
    start_case (private) -- case de départ
    end_case (private) -- case d'arrivée
    move_type (private) -- type du coup (par défault MoveType.NORMAL)
    promotion_piece_type (private) -- type de piece pour une éventuelle promotion (par défault None)
    captured_piece (private) -- piece éventuellement capturée lors du coup (défini dans __post_init__)
    moving_piece (private) -- piece qui effectue le coup (défini dans __post_init__)
    """
    __start_case: Case
    __end_case: Case
    __move_type: MoveType = MoveType.NORMAL
    __promotion_piece_type: None | type[Bishop | Knight | Queen | Rook] = None


    def __post_init__(self) -> None:
        """Vérifie le type de tous les attributs et initialise les attributs captured_piece et moving_piece."""
        verify_type(self.start_case, Case, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "start_case")
        verify_type(self.end_case, Case, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "end_case")
        verify_type(self.move_type, MoveType, "Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None)", "move_type")

        if not (self.promotion_piece_type is None or 
                self.promotion_piece_type in (Bishop, Knight, Queen, Rook)):
            raise TypeError("Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None) Le paramètre promotion_piece_type doit être du type None, Bishop, Knight, Queen ou Rook.")

        if not (self.end_case.content is None or
                isinstance(self.end_case.content, Piece)):
            raise TypeError("Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None) Le paramètre end_case.content doit être du type None ou Piece.")

        if not isinstance(self.start_case.content, Piece):
            raise TypeError("Move(start_case, end_case, move_type=MoveType.NORMAL, promotion_piece_type=None) Le paramètre start_case.content doit être du type Piece.")

        self.captured_piece: None | Piece = self.end_case.content
        self.moving_piece: Piece = self.start_case.content


    def __repr__(self) -> str:
        """Définis la représentation en chaîne de caractères d'un Move."""
        return f"Move[{self.start_case.position} -> {self.end_case.position}, {self.moving_piece}, capture: {self.captured_piece}, type: {self.move_type}, promotion: {self.promotion_piece_type}]"


    @property
    def start_case(self) -> Case:
        """Renvoie la Case de départ."""
        return self.__start_case

    @start_case.setter
    def start_case(self, new_start_case: Case) -> None:
        """Modifie la Case de départ."""
        verify_type(new_start_case, Case, "start_case(new_start_case)", "new_start_case")

        self.start_case = new_start_case

    @property
    def end_case(self) -> Case:
        """Renvoie la Case d'arrivée."""
        return self.__end_case

    @end_case.setter
    def end_case(self, new_end_case: Case) -> None:
        """Modifie la Case d'arrivée."""
        verify_type(new_end_case, Case, "end_case(new_end_case)", "new_end_case")

        self.__end_case = new_end_case

    @property
    def move_type(self) -> MoveType:
        """Renvoie le type du Move."""
        return self.__move_type

    @move_type.setter
    def move_type(self, new_move_type: MoveType) -> None:
        """Modifie le type du Move."""
        verify_type(new_move_type, MoveType, "move_type(new_move_type)", "new_move_type")

        self.__move_type = new_move_type

    @property
    def promotion_piece_type(self) -> None | type[Bishop | Knight | Queen | Rook]:
        """Renvoie le type de Piece d'une eventuelle promotion."""
        return self.__promotion_piece_type

    @promotion_piece_type.setter
    def promotion_piece_type(self, new_promotion_piece_type: None | type[Bishop | Knight | Queen | Rook]) -> None:
        """Modifie le type de Piece d'une éventuelle promotion."""
        if not (new_promotion_piece_type in (Bishop, Knight, Queen, Rook) or 
                new_promotion_piece_type is None):
            raise TypeError("promotion_piece_type(new_promotion_piece_type) Le paramètre new_promotion_piece_type doit être du type None, Bishop, Knight, Queen ou Rook.")

        self.__promotion_piece_type = new_promotion_piece_type

    @property
    def captured_piece(self) -> None | Piece:
        """Renvoie une éventuelle Piece capturée."""
        return self.__captured_piece

    @captured_piece.setter
    def captured_piece(self, new_captured_piece) -> None:
        """Modifie une éventuelle Piece capturée."""
        if not (isinstance(new_captured_piece, Piece) or 
                self.captured_piece is None):
            raise TypeError("capture_piece(new_captured_piece) Le paramètre new_captured_piece doit être du type None ou Piece.")

        self.__captured_piece = new_captured_piece

    @property
    def moving_piece(self) -> Piece:
        """Renvoie la Piece en mouvement."""
        return self.__moving_piece

    @moving_piece.setter
    def moving_piece(self, new_moving_piece: Piece):
        """Modifie la Piece en mouvement."""
        verify_type(new_moving_piece, Piece, "moving_piece(new_moving_piece)", "new_move_piece")

        self.__moving_piece = new_moving_piece