from queue import Queue
from threading import Thread, Event

from src.chess_ai.ai_worker import AIWorker
from src.chess_engine.ai import AI
from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.constants import INITIAL_FEN
from src.chess_engine.game import Game
from src.chess_engine.human import Human
from src.chess_engine.move import Move
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.move_generator import MoveGenerator
from src.chess_engine.player import Player
from src.chess_engine.types import Color, MoveType, GameStatus, EventType
from src.chess_engine.zobrist import Zobrist
from src.user_interface.pygame_ui import PygameUI
from src.user_interface.ui import UI


class ChessApp:
    """Orchestre l'interface utilisateur et le moteur d'échecs.
    
    L'application exécute l'interface utilisateur et la partie dans des 
    threads distincts. Une file permet de transmettre les coups de l'interface 
    vers les joueurs humains du moteur.
    
    Attributes:
        _game_thread: Thread exécutant la boucle principale de la partie.
        _ui_to_game_queue: File utilisée pour transmettre les coups et les 
            signaux d'arrêt de l'interface vers le moteur.
        _game_initialisation: Événement indiquant que la partie a été 
            initialisée et peut être utilisée par l'interface.
        _ui_initialisation: Événement indiquant que l'interface a été 
            initialisée et peut être utilisée par le moteur.
        _stop_running: Événement indiquant que l'application doit arrêter 
            son exécution.
        _game: Partie d'échecs actuellement exécutée par l'application.
        _ui: Interface utilisateur utilisée par l'application.
    """

    def __init__(self) -> None:
        """Initialise les threads, la communication et les événements de l'application."""
        self._game_thread: Thread = Thread(target=self.run_game)
        self._ai_thread: Thread = Thread(target=self.run_ai)

        self._ui_to_game_queue: Queue = Queue()
        self._ai_request_queue: Queue = Queue()
        self._ai_respond_queue: Queue = Queue()

        self._game_initialisation: Event = Event()
        self._ui_initialisation: Event = Event()
        self._ai_initialisation: Event = Event()
        self._human_turn: Event = Event()
        self._ai_turn: Event = Event()
        self._stop_running: Event = Event()

    def run(self) -> None:
        """Lance l'interface utilisateur et la partie.
        
        Les deux composants sont exécutés dans des threads distincts. 
        La méthode attend ensuite leur terminaison.
        
        Une fois les deux threads terminés, l'application se termine.
        """
        self._game_thread.start()
        self._ai_thread.start()
        self.run_ui()

        self._game_thread.join()
        self._ai_thread.join()

        print("Partie finie :)")

    def stop(self) -> None:
        self._stop_running.set()
        self._ai_request_queue.put(None)
        self._ui_to_game_queue.put(None)
        self._ui.exit()

    def run_ui(self) -> None:
        """Exécute la boucle principale de l'interface utilisateur.
        
        Initialise l'interface, attend l'initialisation du moteur, puis 
        affiche continuellement la position actuelle et traite les 
        interactions de l'utilisateur.
        
        La boucle est interrompue lorsque l'utilisateur demande à quitter 
        l'application.
        """
        self.init_ui()
        self._game_initialisation.wait()
        self._ai_initialisation.wait()
        first_clicked_square: int | None = None
        second_clicked_square: int | None = None

        while not self._stop_running.is_set():
            event: int | None = self._ui.update_event()

            match self._ui.event:
                case EventType.QUIT:
                    self.stop()

                case EventType.CLICK:
                    if self._human_turn.is_set() :
                        second_clicked_square = event

                        if first_clicked_square is None:
                            first_clicked_square = second_clicked_square
                            second_clicked_square = None

                        if first_clicked_square is not None and second_clicked_square is not None:
                            move = Move(
                                first_clicked_square, 
                                second_clicked_square, 
                                MoveType.NORMAL
                            )

                            self._ui_to_game_queue.put(move)
                            first_clicked_square = second_clicked_square
                            second_clicked_square = None
                    self._ui.display_position(self._game)

                case _:
                    self._ui.display_position(self._game)

    def run_game(self) -> None:
        """Exécute la boucle principale de la partie.
        
        Initialise le moteur, attend l'initialisation de l'interface, puis 
        demande à chaque joueur de choisir un coup jusqu'à la fin de la 
        partie ou l'arrêt de l'application.
        
        Un joueur humain peut bloquer en attendant qu'un coup soit transmis 
        par l'interface utilisateur.
        """
        self.init_game()
        self._ui_initialisation.wait()
        self._ai_initialisation.wait()

        while self._game.status == GameStatus.ONGOING and not self._stop_running.is_set():
            current_player: Player = self._game.current_player()

            move: Move = current_player.choose_move(self._game.position, self._game.legal_moves)

            if move is not None:
                if self._human_turn.is_set():
                    move = self._game.update_move_type(move)

                try:
                    self._game.make_move(move)

                    self.update_player_turn()

                except ValueError:
                    pass

        print(self._game.status.name)

        if self._game.status is GameStatus.CHECKMATE:
            print(f"winner : {self._game.position.side_to_move.opposite.name}")

        elif self._game.status is GameStatus.DRAW and self._game.draw_reason is not None:
            print(self._game.draw_reason.name)

    def run_ai(self) -> None:
        self.init_ai()
        self._game_initialisation.wait()
        self._ui_initialisation.wait()

        while not self._stop_running.is_set():
            self._ai.analyse_request()

    def init_ui(self) -> None:
        """Initialise l'interface utilisateur de l'application."""
        self._ui: UI = PygameUI()

        self._ui_initialisation.set()

    def init_game(self) -> None:
        """Initialise les composants nécessaires au fonctionnement de la partie.
        
        Crée le générateur d'attaques, le générateur de coups, l'exécuteur 
        de coups, le système Zobrist et la partie initiale.
        """
        fen: str = INITIAL_FEN
        #fen: str = "rnbqkbnr/ppppppPp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        zobrist: Zobrist = Zobrist(42)
        move_executor: MoveExecutor = MoveExecutor(zobrist)
        move_generator: MoveGenerator = MoveGenerator(AttackGenerator(), move_executor)
        
        self._game: Game = Game(
            fen, 
            #Human(Color.WHITE, self._ui_to_game_queue),
            AI(Color.WHITE, self._ai_request_queue, self._ai_respond_queue, 1),  
            #Human(Color.BLACK, self._ui_to_game_queue), 
            AI(Color.BLACK, self._ai_request_queue, self._ai_respond_queue, 1), 
            move_generator, 
            move_executor, 
            zobrist
        )

        self.update_player_turn()

        self._game_initialisation.set()

    def init_ai(self) -> None:
        self._ai: AIWorker = AIWorker(
            self._ai_request_queue, 
            self._ai_respond_queue, 
        )

        self._ai_initialisation.set()

    def update_player_turn(self) -> None:
        if isinstance(self._game.current_player(), Human):
            self._human_turn.set()
            self._ai_turn.clear()

        elif isinstance(self._game.current_player(), AI):
            self._ai_turn.set()
            self._human_turn.clear()