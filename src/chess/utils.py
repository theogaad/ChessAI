from enum import Enum



# Enums
class PieceColor(Enum):
    """Représente les différentes couleurs possible d'une pièce."""
    WHITE = "White"
    BLACK = "Black"

class MoveType(Enum):
    """Représente les différents type de coup possibles."""
    NORMAL = "Normal"
    CASTLING = "Castling"
    PROMOTION = "Promotion"
    EN_PASSANT = "En passant"

class DrawType(Enum):
    """Représente les différents type de nulles possibles."""
    STALEMATE = "Stalemate"
    REPETITION = "Repetition"
    INSUFFICIENT_MATERIAL = "Insufficient material"


# Constantes
BOARD_SIZE: int = 8 # Nombre de lignes/colonnes dans un plateau d'échecs

CASE_SIZE: int = 100 # Taille d'une case en pixels dans pygame

# Valeurs des pièces
PAWN_VALUE: int = 1
BISHOP_VALUE: int = 3
KNIGHT_VALUE: int = 3
ROOK_VALUE: int = 5
QUEEN_VALUE: int = 13

# Couleurs
WHITE = PieceColor.WHITE
BLACK = PieceColor.BLACK


# Fonctions
def verify_type(
        obj_to_verify: object, 
        expected_types: type | tuple[type, ...], 
        function_name: str, 
        variable_name: str, 
        or_none: bool = False
    ) -> None:
    """Vérifie le type d'un object et invoque une erreur si le type ne correspond pas.
    
    Args:
        obj_to_verify: Objet dont le type est à vérifier.
        expected_types: Type(s) attendu(s) de ``obj_to_verify``.
        function_name: Nom de la fonction/méthode appelant cette fonction.
        variable_name: Nom de la variable que l'on vérifie.
        or_none: Indique si ``obj_to_verify`` peut être ``None``.

    Raises:
        TypeError: Si l'un des paramètre n'est pas du type attendu, ou si ``obj_to_verify`` n'est pas du type ``expected_types``.
    """
    if not isinstance(obj_to_verify, object):
        raise TypeError("verify_type(obj_to_verify, expected_types, function_name, variable_name, or_none=False) Le paramètre obj_to_verify doit être du type 'object'.")

    if not isinstance(expected_types, (type, tuple)):
        raise TypeError("verify_type(obj_to_verify, expected_types, function_name, variable_name, or_none=False) Le paramètre expected_types doit être du type 'type' ou 'tuple'.")

    if isinstance(expected_types, tuple):
        for expected_type in expected_types:
            if not isinstance(expected_type, type):
                raise TypeError("verify_type(obj_to_verify, expected_types, function_name, variable_name, or_none=False) Le paramètre expected_types[x] doit être du type 'type'.")

    if not isinstance(function_name, str):
        raise TypeError("verify_type(obj_to_verify, expected_types, function_name, variable_name, or_none=False) Le paramètre function_name doit être du type 'str'.")

    if not isinstance(variable_name, str):
        raise TypeError("verify_type(obj_to_verify, expected_types, function_name, variable_name, or_none=False) Le paramètre variable_name doit être du type 'str'.")

    if not isinstance(or_none, bool):
        raise TypeError("verify_type(obj_to_verify, expected_types, function_name, variable_name, or_none=False) Le paramètre or_none doit être du type 'bool'.")

    message: str = ""

    if or_none:
        message += f"du type 'None' ou "

    if isinstance(expected_types, tuple):
        message += "parmi "
        for i in range(len(expected_types)):
            message += "'" + expected_types[i].__name__ + ("'." if i == len(expected_types) - 1 else "', ")

    elif or_none:
        message += f"'{expected_types.__name__}'."

    else:
        message += f"du type '{expected_types.__name__}'."
        
    if not isinstance(obj_to_verify, expected_types) and not (or_none and obj_to_verify is None):
        raise TypeError(f"{function_name} Le paramètre {variable_name} doit être {message}")


def get_opposite_color(color: PieceColor):
    """Retourne la couleur opposée à la couleur donnée.
    
    Raises:
        TypeError: Si color n'est pas une instance de PieceColor.
    """
    verify_type(color, PieceColor, "get_opposite_color(color)", "color")

    if color == PieceColor.WHITE:
        return PieceColor.BLACK

    return PieceColor.BLACK