from threading import Event

from src.chess_engine.move import Move
from src.chess_engine.player import Player
from src.chess_engine.position import Position
from src.chess_engine.types import Color


class Human(Player):
    """Représente un joueur humain. 
    
    Cette classe implémente l'interface ``Player`` pour un joueur dont le 
    choix des coups est effectué par une couche externe, telle qu'une 
    interface utilisateur. 
    
    La méthode ``choose_move`` est bloquante : elle attend qu'un coup soit 
    fourni par la couche externe via ``set_move``. Cette conception permet 
    au moteur de rester indépendant de toute bibliothèque d'interface 
    utilisateur. 
    
    Attributes: 
        color: Couleur des pièces contrôlées par le joueur.
    """

    def __init__(self, color: Color) -> None:
        """Initialise un joueur humain.

        Args:
            color: Couleur des pièces contrôlées par le joueur.
        """
        super().__init__(color)
        self._event: Event = Event()
        self._move: Move | None = None

    def choose_move(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> Move:
        """Attend et retourne le coup sélectionné par l'utilisateur.
        
        Cette méthode bloque son exécution jusqu'à ce qu'un coup soit fourni 
        via ``set_move``. La vérification de la légalité du coup relève de la 
        responsabilité de la partie.
        
        Args:
            position: Position actuelle de la partie.
            legal_moves: Liste des coups légaux disponibles.
            
        Returns:
            Le coup sélectionné par l'utilisateur.
        """
        self._event.wait()
        self._event.clear()

        assert self._move is not None

        move: Move = self._move
        self._move = None

        return move

    def set_move(self, move: Move) -> None:
        """Fournit le coup sélectionné par l'utilisateur.
        
        Cette méthode est destinée à être appelée par la couche externe 
        responsable de l'interaction avec l'utilisateur. Elle transmet le 
        coup à ``choose_move`` et permet à cette dernière de poursuivre son 
        exécution.
        
        Args:
            move: Coup sélectionné par l'utilisateur.
        """
        self._move = move
        self._event.set()