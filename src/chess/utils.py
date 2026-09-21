from enum import Enum



# Enums
class PieceColor(Enum):
    """Enum représentant les deux couleurs possibles au échecs."""
    WHITE = "White"
    BLACK = "Black"

class MoveType(Enum):
    """Enum représentant les différents type de Move possibles."""
    NORMAL = "Normal"
    CASTLING = "Castling"
    PROMOTION = "Promotion"
    EN_PASSANT = "En passant"

class DrawType(Enum):
    """Enum représentant les différents type de draw possibles."""
    STALEMATE = "Stalemate"
    REPETITION = "Repetition"
    INSUFFICIENT_MATERIAL = "Insufficient material"

# Fonctions
def verify_type(obj_to_verify: object, type: type, function_name: str, variable_name: str) -> None:
    """Fonction vérifiant le type d'un object et invoquant une erreur si le type ne correspond pas.
    
    obj_to_verify -- object quelconque dont on va vérifier le type
    type -- type que obj_to_verify doit avoir
    function_name -- nom de la fonction/méthode appelant cette fonction, apparaît dans le message d'erreur
    variable_name -- nom de la variable que l'on vérifie, apparaît dans le message d'erreur
    """
    if not isinstance(obj_to_verify, type):
        raise TypeError(f"{function_name} Le paramètre {variable_name} doit être du type {type}.")