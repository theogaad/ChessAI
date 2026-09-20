"""Package contenant l'initialisation et le comportement basique de toutes les pièces d'échecs.

Piece -- Classe abstraite définissant une pièce. Contient l'Enum des couleurs, l'initialisation, les getters/setters, 
la représentation en chaîne de caractère, l'égalité et la méthode get_reachable_sliding_positions_from_position.
Bishop -- Classe héritière de la classe Piece, définissant un Fou. Contient la méthode abstraite 
get_reachable_positions_from_position héritée de la classe Piece
King -- Classe héritière de la classe Piece, définissant un Roi. Contient la méthode abstraite 
get_reachable_positions_from_position héritée de la classe Piece
Knight -- Classe héritière de la classe Piece, définissant un Cavalier. Contient la méthode abstraite 
get_reachable_positions_from_position héritée de la classe Piece
Pawn -- Classe héritière de la classe Piece, définissant un Pion. Contient la méthode abstraite 
get_reachable_positions_from_position héritée de la classe Piece
Queen -- Classe héritière de la classe Piece, définissant une Reine. Contient la méthode abstraite 
get_reachable_positions_from_position héritée de la classe Piece
Rook -- Classe héritière de la classe Piece, définissant une Tour. Contient la méthode abstraite 
get_reachable_positions_from_position héritée de la classe Piece
"""