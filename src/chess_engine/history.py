from dataclasses import dataclass, field

from src.chess_engine.move import Move
from src.chess_engine.undo_info import UndoInfo


@dataclass
class History:
    """Représente l'historique des coups et des positions d'une partie.

    L'historique conserve les coups joués, les informations nécessaires à
    leur annulation ainsi que les hashes Zobrist des positions obtenues après
    chaque coup.

    Le hash de la position initiale est conservé séparément afin d'éviter
    d'ajouter une entrée artificielle aux listes ``moves`` et ``undo_infos``.

    Les listes ``moves``, ``undo_infos`` et ``zobrist_hashes`` restent
    synchronisées : pour un même indice, chaque élément correspond au même
    coup joué et à la position obtenue après ce coup.

    Attributes:
        initial_zobrist_hash: Hash Zobrist de la position initiale de la
            partie.
        moves: Liste des coups joués dans l'ordre chronologique.
        undo_infos: Liste des informations nécessaires pour annuler les
            coups correspondants.
        zobrist_hashes: Liste des hashes Zobrist des positions obtenues
            après chaque coup.
    """

    initial_zobrist_hash: int
    moves: list[Move] = field(default_factory=list)
    undo_infos: list[UndoInfo] = field(default_factory=list)
    zobrist_hashes: list[int] = field(default_factory=list)

    def add(
        self,
        move: Move,
        undo_info: UndoInfo,
        zobrist_hash: int
    ) -> None:
        """Ajoute un coup à l'historique.

        Enregistre simultanément le coup joué, les informations nécessaires
        à son annulation et le hash Zobrist de la position obtenue après
        ce coup.

        Args:
            move: Coup joué.
            undo_info: Informations permettant d'annuler le coup.
            zobrist_hash: Hash Zobrist de la position après le coup.
        """
        self.moves.append(move)
        self.undo_infos.append(undo_info)
        self.zobrist_hashes.append(zobrist_hash)

    def remove_last(self) -> None:
        """Supprime le dernier coup de l'historique.

        Supprime simultanément le dernier coup, les informations nécessaires
        à son annulation et le hash Zobrist correspondant.

        Raises:
            IndexError: Si l'historique est vide.
        """
        if (len(self.moves) == 0 or 
            len(self.undo_infos) == 0 or 
            len(self.zobrist_hashes) == 0):
            raise IndexError("Un des historique est vide.")
        
        self.moves.pop()
        self.undo_infos.pop()
        self.zobrist_hashes.pop()

    def count_position(self, zobrist_hash: int) -> int:
        """Compte le nombre d'occurrences d'une position dans l'historique.

        Le comptage inclut la position initiale ainsi que toutes les positions
        obtenues après les coups joués.

        Args:
            zobrist_hash: Hash Zobrist de la position à rechercher.

        Returns:
            Nombre d'occurrences du hash dans l'historique.
        """
        position_count: int = 0

        for position_hash in [self.initial_zobrist_hash] + self.zobrist_hashes:
            if position_hash == zobrist_hash:
                position_count += 1

        return position_count

    def get_last_move(self) -> Move:
        """Retourne le dernier coup joué.

        Returns:
            Dernier coup enregistré dans l'historique.

        Raises:
            IndexError: Si l'historique est vide.
        """
        return self.moves[-1]

    def get_last_undo_info(self) -> UndoInfo:
        """Retourne les informations d'annulation du dernier coup.

        Returns:
            Informations nécessaires pour annuler le dernier coup joué.

        Raises:
            IndexError: Si l'historique est vide.
        """
        return self.undo_infos[-1]

    def get_last_zobrist_hash(self) -> int:
        """Retourne le hash Zobrist de la dernière position.

        Il s'agit du hash de la position obtenue après le dernier coup joué.

        Returns:
            Hash Zobrist de la dernière position enregistrée.

        Raises:
            IndexError: Si aucun coup n'a encore été joué.
        """
        return self.zobrist_hashes[-1]