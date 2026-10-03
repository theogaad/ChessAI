from src.chess_engine.position import Position
from src.chess_engine.types import Color, PieceType


class Zobrist:
    """Gère les clés de hachage Zobrist utilisées par le moteur.

    Le hachage Zobrist permet d'associer une valeur entière à une position
    d'échecs afin de pouvoir identifier rapidement une position et détecter
    notamment les répétitions.

    Une clé aléatoire distincte est associée à chaque combinaison de couleur,
    de type de pièce et de case. Des clés supplémentaires sont utilisées pour
    le joueur devant jouer, les droits de roque et la case en passant.

    Les clés sont générées une seule fois lors de l'initialisation et restent
    inchangées pendant toute la durée de vie de l'instance.

    Attributes:
        _piece_keys: Clés Zobrist associées à chaque combinaison de couleur,
            de type de pièce et de case.
        _side_to_move_key: Clé utilisée lorsque les Noirs sont au trait.
        _castling_keys: Clés associées aux différentes combinaisons de droits
            de roque.
        _en_passant_keys: Clés associées aux différentes cases en passant.
    """

    def __init__(self, seed: int | None = None) -> None:
        """Initialise les clés Zobrist.

        Args:
            seed: Graine optionnelle utilisée pour initialiser le générateur
                de nombres aléatoires. Si None, une graine aléatoire est
                utilisée.
        """
        # TODO

    def hash_position(self, position: Position) -> int:
        """Calcule le hash Zobrist complet d'une position.

        Args:
            position: Position dont le hash doit être calculé.

        Returns:
            Valeur entière représentant le hash Zobrist de la position.
        """
        # TODO

    def piece_key(
        self,
        color: Color,
        piece_type: PieceType,
        square: int,
    ) -> int:
        """Retourne la clé Zobrist associée à une pièce sur une case.

        Args:
            color: Couleur de la pièce.
            piece_type: Type de la pièce.
            square: Indice de la case occupée.

        Returns:
            Clé Zobrist correspondante.
        """
        # TODO

    def side_to_move_key(self) -> int:
        """Retourne la clé Zobrist associée au trait des Noirs.

        Returns:
            Clé Zobrist utilisée lorsque les Noirs doivent jouer.
        """
        # TODO

    def castling_key(self, castling_rights: int) -> int:
        """Retourne la clé Zobrist associée aux droits de roque.

        Args:
            castling_rights: Combinaison des droits de roque disponibles.

        Returns:
            Clé Zobrist correspondante.
        """
        # TODO

    def en_passant_key(self, square: int) -> int:
        """Retourne la clé Zobrist associée à une case en passant.

        Args:
            square: Indice de la case en passant.

        Returns:
            Clé Zobrist correspondante.
        """
        # TODO