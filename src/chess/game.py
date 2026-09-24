from copy import deepcopy
from random import shuffle
from src.chess.board import Board
from src.chess.case import Case
from src.chess.exceptions.chess_error import ChessError
from src.chess.exceptions.illegal_move_error import IllegalMoveError
from src.chess.game_info import GameInfo
from src.chess.mapping import str_to_promotion_piece_type
from src.chess.move import Move
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.player import Player
from src.chess.position import Position
from src.chess.profile import Profile
from src.chess.utils import PieceColor, MoveType, GameStatus, BOARD_SIZE, WHITE, BLACK, verify_type, get_opposite_color

# TODO: Implémenter la méthode get_reachable_cases_by_catsling_from_position(self, position: Position)
# TODO: Implémenter la méthode get_reachable_cases_by_en_passant_from_position(self, position: Position)
# TODO: Implémenter la méthode get_legally_reachable_cases_of_color(self, color: PieceColor)
# TODO: Implémenter la méthode apply_move(self, move: Move)
# TODO: Implémenter la méthode unapply_move(self, move: Move)
# TODO: Implémenter la méthode unapply_last_move(self)
# TODO: Implémenter la méthode get_legally_attacked_cases_by_color(self, color: PieceColor)
# TODO: Implémenter la méthode update_move_type(self, move: Move)
# TODO: Implémenter la méthode is_castling(self, move: Move)
# TODO: Implémenter la méthode is_en_passant(self, move: Move)
# TODO: Implémenter la méthode is_promotion(self, move: Move)
# TODO: Implémenter la méthode ask_for_promotion_piece_type(self)
# TODO: Implémenter la méthode is_stalemate(self)
# TODO: Implémenter la méthode is_repetition(self)
# TODO: Implémenter la méthode is_insufficient_material(self)
# TODO: Implémenter la méthode is_fifty_moves(self)
# TODO: Implémenter la méthode is_checkmate(self)
# TODO: Implémenter la méthode update_game_status(self)
# TODO: Implémenter la méthode end_the_game(self)

class Game:
    """Représente une partie d'échec."""
    def __init__(
        self, 
        profiles: tuple[Profile, Profile]
    ) -> None:
        self.init_players(profiles)
        self.__board: Board = Board()
        self.__status: GameStatus = GameStatus.ONGOING
        self.__move_history: list[Move] = []
        self.__game_info_history: list[GameInfo] = []


    def get_legally_reachable_cases_from_position(
        self, 
        position: Position
    ) -> list[Case]:
        """Retourne toutes les case légalement accessibles par la pièce située à la position donnée.
        
        Args:
            position: Position de départ de la pièce.
            
        Returns:
            Liste de toutes les case légalement accessibles par la pièce située à la position donnée.
            
        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_legally_reachable_cases_from_position(position)", "position")
        legally_reachable_cases: list[Case] = []

        piece: Piece = self.board.get_piece(position)

        for reachable_case in self.board.get_reachable_cases_from_position(position):
            test_move: Move = Move(self.board.get_case(position), reachable_case)
            self.board.apply_move(test_move)

            if not self.is_check(piece.piece_color):
                legally_reachable_cases.append(reachable_case)

            self.board.unapply_move(test_move)
            self.update_has_moved(test_move.moving_piece)

        legally_reachable_cases.extend(self.get_legally_reachable_cases_by_castling_from_position(position))
        legally_reachable_cases.extend(self.get_legally_reachable_cases_by_en_passant_from_position(position))

        return legally_reachable_cases


    def get_legally_reachable_cases_by_castling_from_position(
        self, 
        position: Position
    ) -> list[Case]:
        """Retourne les cases légalements accessibles par la pièce à la position donnée en faisant un roque.
        
        Args:
            position: Position de départ.
            
        Returns:
            Liste de toutes les cases légalements accessibles par la pièce à la position donnée en faisant un roque.
            
        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_legally_reachable_cases_by_castling_from_position(position)", "position")

        legally_reachable_cases_by_castling: list[Case] = []
        actual_case: Case = self.board.get_case(position)

        if (isinstance(actual_case.content, King) and
            not actual_case.content.has_moved):

            for direction in [-1, 1]:
                can_castle: bool = True

                for i in range(1, 3):
                    end_case: Case = self.board.get_case(Position(actual_case.position.line, 
                                                                  actual_case.position.column + (i * direction)))

                    if (end_case.content or 
                        end_case in self.board.get_attacked_cases_by_color(actual_case.content.piece_color)):
                        can_castle = False
                        break

                if can_castle:
                    legally_reachable_cases_by_castling.append(end_case)

        return legally_reachable_cases_by_castling


    def get_legally_reachable_cases_by_en_passant_from_position(
        self, 
        position: Position
    ) -> list[Case]:
        """Retourne les cases légalements accessibles par la pièce à la position donnée en faisant un en_passant.
                
        Args:
            position: Position de départ.
            
        Returns:
            Liste de toutes les cases légalements accessibles par la pièce à la position donnée en faisant un en_passant.
            
        Raises:
            TypeError: Si ``position`` n'est pas une instance de ``Position``.
        """
        verify_type(position, Position, "get_legally_reachable_cases_by_en_passant_from_position(position)", "position")
        
        legally_reachable_cases_by_en_passant: list[Case] = []
        actual_case: Case = self.board.get_case(position)
        piece: Piece = self.board.get_piece(position)

        if isinstance(actual_case.content, Pawn):
            for direction in [-1, 1]:
                if 0 <= (actual_case.position.column + direction) < BOARD_SIZE:
                    adjacent_case: Case = self.board.get_case(Position(actual_case.position.line, 
                                                                   actual_case.position.column + direction))

                    # Si la case adjacente contient un pion d'une couleur différente que la pièce positionnée à ``position`` et
                    # si le pion adjacent vient de faire le dernier coup enregistré dans la partie en avancant de 2 cases.
                    if (isinstance(adjacent_case.content, Pawn) and 
                        not actual_case.content.is_color(adjacent_case.content.piece_color) and
                        self.move_history and
                        self.move_history[-1].moving_piece == adjacent_case.content and 
                        abs(self.move_history[-1].start_case.position.line - 
                            self.move_history[-1].end_case.position.line) == 2):
                        reachable_case: Case = self.board.get_case(Position(
                            actual_case.position.line + (1 if actual_case.content.is_color(WHITE) else -1),
                            actual_case.position.column + direction
                        ))
                        test_move: Move = Move(actual_case, reachable_case)
                        self.board.apply_move(test_move)

                        if not self.is_check(piece.piece_color):
                            legally_reachable_cases_by_en_passant.append(reachable_case)

                        self.board.unapply_move(test_move)
                        self.update_has_moved(test_move.moving_piece)
        
        return legally_reachable_cases_by_en_passant


    def get_legally_reachable_cases_of_color(
        self, 
        color: PieceColor
    ) -> list[Case]:
        """Retourne toutes les case légalement accessibles par toutes les pièces de la couleur donnée.
                
        Args:
            color: Couleur des pièces dont on veut récupérer les cases accessibles.
            
        Returns:
            Liste de toutes les case légalement accessibles par toutes les pièces de la couleur donnée.
            
        Raises:
            TypeError: Si ``color`` n'est pas une instance de ``PieceColor``.
        """
        verify_type(color, PieceColor, "get_legally_reachable_cases_of_color(color)", "color")

        legally_reachable_cases: list[Case] = []

        for case in self.board.get_cases_of_piece_type_and_color((Bishop, King, Knight, Pawn, Queen, Rook), color):
            legally_reachable_cases.extend(self.get_legally_reachable_cases_from_position(case.position))

        return legally_reachable_cases


    def get_legally_attacked_cases_by_color(
        self, 
        color: PieceColor
    ) -> list[Case]:
        """Retourne toutes les cases menacées par toutes les pièces de la couleur donnée.
        
        Args:
            color: Couleur des pièces dont on veut récupérer les cases menacées.
            
        Returns:
            Liste de toutes les cases menacées par toutes les pièces de la couleur donnée.
        
        Raises:
            TypeError: Si ``color`` n'est pas une instance de ``PieceColor``.
        """
        verify_type(color, PieceColor, "get_legally_attacked_cases_by_color(color)", "color")

        legally_attacked_cases: list[Case] = []

        for case in self.board.get_cases_of_piece_type_and_color((Bishop, King, Knight, Pawn, Queen, Rook), color):
            if isinstance(case.content, Pawn):
                for position in case.content.get_reachable_positions_from_position(case.position):
                    if case.position.get_direction(position)[1] != 0:
                        test_move: Move = Move(case, self.board.get_case(position))
                        self.board.apply_move(test_move)
                        
                        if self.is_check(color):
                            legally_attacked_cases.append(self.board.get_case(position))

                        self.board.unapply_move(test_move)
                        self.update_has_moved(test_move.moving_piece)

            else:
                legally_attacked_cases.extend(self.get_legally_reachable_cases_from_position(case.position))

        return legally_attacked_cases


    def is_check(
        self, 
        color: PieceColor
    ) -> bool:
        """Indique si le roi de la couleur donnée est en échec.
        
        Raises:
            TypeError: Si ``color`` n'est pas une instance de ``PieceColor``.
        """
        verify_type(color, PieceColor, "is_check(color)", "color")

        king_case: Case = self.board.get_cases_of_piece_type_and_color((King,), color)[0]

        if king_case in self.board.get_attacked_cases_by_color(get_opposite_color(color)):
            return True

        return False


    def get_game_info(self) -> GameInfo:
        """Retourne les informations principales concernant l'état actuel de la partie."""
        castling_possible_moves: list[Move] = []
        en_passant_possible_moves: list[Move] = []

        for color in [WHITE, BLACK]:
            for king_case in self.board.get_cases_of_piece_type_and_color((King,), color):
                castling_cases: list[Case] = self.get_legally_reachable_cases_by_castling_from_position(king_case.position)
                for castling_case in castling_cases:
                    castling_possible_moves.append(Move(king_case, castling_case))

            for pawn_case in self.board.get_cases_of_piece_type_and_color((Pawn,), color):
                en_passant_cases: list[Case] = self.get_legally_reachable_cases_by_en_passant_from_position(pawn_case.position)
                for en_passant_case in en_passant_cases:
                    en_passant_possible_moves.append(Move(pawn_case, en_passant_case))
        
        return GameInfo(deepcopy(self.board), self.current_player, castling_possible_moves, en_passant_possible_moves)


    def apply_move(
        self, 
        move: Move
    ) -> None:
        """Applique le mouvement donné à cette partie.
        
        Args:
            move: Mouvement à appliquer.
        
        Raises:
            TypeError: Si ``move`` n'est pas une instance de ``Move``.
        """
        verify_type(move, Move, "apply_move(move)", "move")

        if not move.end_case in self.get_legally_reachable_cases_from_position(move.start_case.position):
            raise IllegalMoveError("apply_move(move) La case ``move.end_case`` doit être une case légalement atteignale par la pièce contenue dans ``move.start_case``.")

        if not move.moving_piece.is_color(self.current_player.color):
            raise IllegalMoveError("apply_move(move) La couleur de la pièce contenue dans ``move.start_case`` doit être la même que celle du joueur actuel.")

        self.update_move_type_and_properties(move)
        self.board.apply_move(move)
        self.move_history.append(move)
        self.game_info_history.append(self.get_game_info())
        self.update_game_status_and_end_the_game()
        self.switch_current_player()


    def unapply_move(
        self, 
        move: Move
    ) -> None:
        """Annule le mouvement donné sur cette partie.
                
        Args:
            move: Mouvement à annuler.
        
        Raises:
            TypeError: Si ``move`` n'est pas une instance de ``Move``.
            ChessError: Si le mouvement n'est pas présent dans l'historique des mouvements de cette partie.
        """
        # TODO: Possiblement supprimer.
        verify_type(move, Move, "unapply_move(move)", "move")

        if not move in self.move_history:
            raise ChessError("Ce mouvement n'est pas présent dans l'historique des mouvements.")

        self.board.unapply_move(move)
        # On supprime la dernière occurence du mouvement dans l'historique.
        self.move_history.reverse()
        self.move_history.remove(move)
        self.move_history.reverse()
        self.update_game_status_and_end_the_game()

        if not move.moving_piece.is_color(self.current_player.color):
            self.switch_current_player()


    def update_has_moved(self, piece: Piece) -> None:
        """Actualise la propriété ``has_moved`` de la pièce en s'appuyant sur l'historique des mouvements.
        
        Args:
            piece: Pièce dont on actualise la propriété ``has_moved``.
        
        Raises:
            TypeError: Si ``piece`` n'est pas une instance de ``Piece``.
        """
        verify_type(piece, Piece, "update_has_moved(piece)", "piece")

        piece_has_moved: bool = False

        for ancient_move in self.move_history:
            if ancient_move.moving_piece is piece:
                piece_has_moved = True
            
        piece.has_moved = piece_has_moved

    
    def unapply_last_move(self) -> None:
        """Annule le dernier coup enregistré dans l'historique de cette partie."""
        # TODO: Possiblement supprimer.
        self.unapply_move(self.move_history[-1])


    def update_move_type_and_properties(
        self, 
        move: Move
    ) -> None:
        """Actualise les propriétés du mouvement donné.
        
        Args:
            move: Mouvement dont on actualise les propriété.
            
        Raises:
            TypeError: Si ``move`` n'est pas une instance de ``Move``.
        """
        verify_type(move, Move, "update_move_type(move)", "move")

        if self.is_castling(move):
            move.move_type = MoveType.CASTLING

        elif self.is_en_passant(move):
            move.move_type = MoveType.EN_PASSANT
            move.captured_piece = self.board.get_piece(Position(move.start_case.position.line, move.end_case.position.column))

        elif self.is_promotion(move):
            move.move_type = MoveType.PROMOTION
            move.promotion_piece_type = self.ask_for_promotion_piece_type()

        else:
            move.move_type = MoveType.NORMAL


    def is_castling(
        self, 
        move: Move
    ) -> bool:
        """Indique si le mouvement est un roque.
        
        Raises:
            TypeError: Si move n'est pas une instance de Move.
        """
        verify_type(move, Move, "is_castling(move)", "move")

        is_castling = (isinstance(move.start_case.content, King) and
                       abs(move.start_case.position.column - move.end_case.position.column) == 2)

        return is_castling


    def is_en_passant(
        self, 
        move: Move
    ) -> bool:
        """Indique si le mouvement est un en passant.
                
        Raises:
            TypeError: Si move n'est pas une instance de Move.
        """
        verify_type(move, Move, "is_en_passant(move)", "move")

        is_en_passant = (isinstance(move.start_case.content, Pawn) and
                         move.end_case.content is None and
                         move.start_case.position.get_direction(move.end_case.position)[1] != 0)

        return is_en_passant


    def is_promotion(
        self, 
        move: Move
    ) -> bool:
        """Indique si le mouvement est une promotion.
                
        Raises:
            TypeError: Si move n'est pas une instance de Move.
        """
        verify_type(move, Move, "is_promotion(move)", "move")

        is_promotion = (isinstance(move.start_case.content, Pawn) and 
                        move.end_case.position.line == (7 if move.start_case.content.is_color(WHITE)
                                                        else 0))

        return is_promotion


    def ask_for_promotion_piece_type(self) -> type[Bishop | Knight | Queen | Rook]:
        """Demande à l'utilisateur de choisir un type de pièce pour une promotion.
        
        La méthode pour faire cette demande n'est pas encore définitive.

        Returns:
            Le type de pièce choisi par l'utilisateur parmi 'Bishop', 'Knight', 'Queen' et 'Rook'.
        """

        # Pour l'instant on utilise ``input`` pour demander le type de pièce.
        #piece_type: type[Bishop | Knight | Queen | Rook] = str_to_promotion_piece_type(input("Veuillez indiquer le nouveau type souhaité de la pièce après la promotion parmi 'Bishop', 'Knight', 'Queen' et 'Rook' : "))

        #return piece_type
        return Queen


    def end_the_game(self, winner: None | Player = None) -> None:
        # TODO: Faire la doc.

        # TODO: Finir la méthode.
        pass


    def update_game_status_and_end_the_game(self) -> None:
        """Actualise le status de la partie et l'arrête si nécessaire."""
        if self.is_checkmate()[0]:
            self.status = GameStatus.CHECKMATE
            self.end_the_game(self.is_checkmate()[1])

        elif self.is_stalemate():
            self.status = GameStatus.DRAW_STALEMATE
            self.end_the_game()
        
        elif self.is_repetition():
            self.status = GameStatus.DRAW_REPETITION
            self.end_the_game()

        elif self.is_insufficient_material():
            self.status = GameStatus.DRAW_INSUFFICIENT_MATERIAL
            self.end_the_game()

        elif self.is_fifty_moves():
            self.status = GameStatus.DRAW_FIFTY_MOVES
            self.end_the_game()

        else:
            self.status = GameStatus.ONGOING


    def is_checkmate(self) -> tuple[bool, None | Player]:
        """Indique si l'un des joueurs est échec et mat.
        
        Returns:
            Un tuple indiquant si il y a échec et mat et si oui le joueur gagnant, sinon ``None``.
        """
        is_checkmate: bool = False
        winner: None | Player = None

        for player in self.players:
            if (not self.get_legally_reachable_cases_of_color(player.color) and
                self.is_check(player.color)):
                is_checkmate = True
                winner = player

        return (is_checkmate, winner)


    def is_stalemate(self) -> bool:
        """Indique si il y a pat."""
        is_stalemate: bool = False

        for player in self.players:
            if (not self.get_legally_reachable_cases_of_color(player.color) and
                not self.board.get_cases_of_piece_type_and_color((King,), player.color) in 
                self.get_legally_attacked_cases_by_color(get_opposite_color(player.color))):
                is_stalemate = True

        return is_stalemate


    def is_repetition(self) -> bool:
        """Indique si la disposition actuelle de l'échiquier est déjà apparu au moins 2 autres fois dans cette partie."""
        same_game_info_count: int = 0

        if self.game_info_history:
            last_game_info: GameInfo = self.game_info_history[-1]

            for game_info in self.game_info_history:
                if game_info == last_game_info:
                    same_game_info_count += 1

        return same_game_info_count >= 3


    def is_insufficient_material(self) -> bool:
        """Indique si la partie est dans une configuration où les joueurs n'ont pas assez de pièces pour finir en échec et mat."""
        piece_dictionary: dict = {}

        for color in [WHITE, BLACK]:
            for piece_type in [Bishop, King, Knight, Pawn, Queen, Rook]:
                piece_dictionary[(color, piece_type)] = len(self.board.get_cases_of_piece_type_and_color((piece_type,), color))

        if (piece_dictionary[(WHITE, Queen)] or
            piece_dictionary[(BLACK, Queen)] or
            piece_dictionary[(WHITE, Rook)] or
            piece_dictionary[(BLACK, Rook)] or
            piece_dictionary[(WHITE, Knight)] == 2 or
            piece_dictionary[(BLACK, Knight)] == 2 or
            piece_dictionary[(WHITE, Bishop)] == 2 or
            piece_dictionary[(BLACK, Bishop)] == 2 or
            (piece_dictionary[(WHITE, Knight)] and 
             piece_dictionary[(BLACK, Knight)]) or
             (piece_dictionary[(WHITE, Bishop)] and 
              piece_dictionary[(BLACK, Knight)]) or
              (piece_dictionary[(WHITE, Knight)] and
               piece_dictionary[(BLACK, Bishop)])):
            return False

        if (piece_dictionary[(WHITE, Bishop)] and
            piece_dictionary[(BLACK, Bishop)]):
            white_bishop_case: Case = self.board.get_cases_of_piece_type_and_color((Bishop,), WHITE)[0]
            black_bishop_case: Case = self.board.get_cases_of_piece_type_and_color((Bishop,), BLACK)[0]

            # Si les deux fous sont des cases de même couleur.
            if ((white_bishop_case.position.line + white_bishop_case.position.column) % 2 !=
                (black_bishop_case.position.line + black_bishop_case.position.column) % 2):
                return False

        return True


    def is_fifty_moves(self) -> bool:
        """Indique si aucun pion n'a été déplacée ou si aucune capture n'a été faite pendant les 100 derniers coups."""
        move_counter: int = 0

        for move in reversed(self.move_history):
            if isinstance(move.moving_piece, Pawn) or move.captured_piece:
                break
            move_counter += 1

        return move_counter >= 100


    def switch_current_player(self) -> None:
        """Passe au joueur suivant en modifiant la propriété ``current_player``"""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]


    def init_players(
        self, 
        profiles: tuple[Profile, Profile]
    ) -> None:
        """Initialise les joueurs à partir des profils donnés et en leur attribuant une couleur aléatoire.

        Initialise aussi le joueur actuel en choisissant le joueur dont la couleur est blanche.
        
        Args:
            profiles: Tuple de profils auquel les joueurs sont associés.
            
        Raises:
            TypeError: Si ``profiles`` n'est pas un tuple ou si ses éléments ne sont pas des instances de ``Profile``."""
        verify_type(profiles, tuple, "init_players(profiles)", "profiles")

        if not len(profiles) == 2:
            raise ChessError("init_players(profiles) L'argument profiles doit être un tuple d'exactement 2 éléments.")

        for profile in profiles:
            verify_type(profile, Profile, "init_players(profiles)", "profiles[x]")

        colors: list[PieceColor] = [WHITE, BLACK]
        shuffle(colors)
        self.__players: tuple[Player, Player] = (Player(profiles[0], colors[0]), Player(profiles[1], colors[1]))
        self.__current_player: Player = self.players[0] if self.players[0].is_color(WHITE) else self.players[1]


    @property
    def players(self) -> tuple[Player, Player]:
        """Retourne un tuple des joueurs de cette partie."""
        return self.__players

    @players.setter
    def players(
        self, 
        new_players: tuple[Player, Player]
    ) -> None:
        """Modifie le tuple des joueurs de cette partie.
        
        Args:
            new_players: Nouveau tuple des joueurs de cette partie.
            
        Raises:
            TypeError: Si ``new_players`` n'est pas un tuple ou si les éléments de ``new_players`` ne sont pas des instance de ``Player``.
            ChessError: Si ``new_players`` n'est pas un tuple d'exactement 2 éléments.    
        """
        verify_type(new_players, tuple, "players(new_players)", "new_players")

        if not len(new_players) == 2:
            raise ChessError("players(new_players) L'argument new_players doit être un tuple contenant exactement 2 éléments.")

        for new_player in new_players:
            verify_type(new_player, Player, "players(new_players)", "new_players[x]")

        self.__players = new_players

    @property
    def current_player(self) -> Player:
        """Retourne le joueur actuel de la partie."""
        return self.__current_player

    @current_player.setter
    def current_player(
        self, 
        new_current_player: Player
    ) -> None:
        """Modifie le joueur actuel de la partie.
        
        Args:
            new_current_player: Nouveau joueur actuel.
            
        Raises:
            TypeError: Si ``new_current_player`` n'est pas une instance de ``Player``.
        """
        verify_type(new_current_player, Player, "current_player(new_current_player)", "new_current_player")

        self.__current_player = new_current_player

    @property
    def board(self) -> Board:
        """Retourne l'échiquier de cette partie."""
        return self.__board

    @board.setter
    def board(
        self, 
        new_board: Board
    ) -> None:
        """Modifie l'échiquier de cette partie.
                
        Args:
            new_board: Nouvel échiquier de cette partie.
            
        Raises:
            TypeError: Si ``new_board`` n'est pas une instance de ``Board``.
        """
        verify_type(new_board, Board, "board(new_board)", "new_board")

        self.__board = new_board

    @property
    def status(self) -> GameStatus:
        """Retourne le status actuel de cette partie."""
        return self.__status

    @status.setter
    def status(
        self, 
        new_status: GameStatus
    ) -> None:
        """Modifie le status actuel de cette partie.
                
        Args:
            new_status: Nouveau status de cette partie.
            
        Raises:
            TypeError: Si ``new_status`` n'est pas une instance de ``GameStatus``.
        """
        verify_type(new_status, GameStatus, "status(new_status)", "new_status")

        self.__status = new_status

    @property
    def move_history(self) -> list[Move]:
        """Retourne l'historique des coups joués de cette partie."""
        return self.__move_history

    @move_history.setter
    def move_history(
        self, 
        new_move_history: list[Move]
    ) -> None:
        """Modifie l'historique des coups joués de cette partie.
                
        Args:
            new_move_history: Nouvel historique de coups joués.
            
        Raises:
            TypeError: Si ``new_move_history`` n'est pas une liste 
                ou si les éléments de ``new_move_history`` ne sont pas des instances de ``Move``.
        """
        verify_type(new_move_history, list, "move_history(new_move_history)", "new_move_history")

        for move in self.move_history:
            verify_type(move, Move, "move_history(new_move_history)", "new_move_history[x]")

        self.__move_history = new_move_history

    @property
    def game_info_history(self) -> list[GameInfo]:
        """Retourne l'historique des états de cette partie."""
        return self.__game_info_history

    @game_info_history.setter
    def game_info_history(self, new_game_info_history: list[GameInfo]) -> None:
        """Modifie l'historique des états de cette partie.
        
        Args:
            new_game_info_history: Nouvelle historique des états de cette partie.
            
        Raises:
            TypeError: Si ``new_game_info_history`` n'est une liste ou si un des éléments de ``new_game_info_history`` n'est pas une instance de ``GameInfo``."""
        verify_type(new_game_info_history, list, "game_info_history(new_game_info_history)", "new_game_info_history")

        for new_game_info in new_game_info_history:
            verify_type(new_game_info, GameInfo, "game_info_history(new_game_info_history)", "new_game_info_history[x]")

        self.__game_info_history = new_game_info_history