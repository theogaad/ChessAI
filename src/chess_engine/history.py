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