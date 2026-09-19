from abc import ABC
from src.chess.pieces.piece import PieceColor
from src.chess.profile import Profile



class Player(ABC):
    def __init__(self, profile: Profile, color: PieceColor) -> None:
        if not isinstance(profile, Profile):
            raise TypeError("Player(self, profile, color) L'attribut profile doit être du type Profile.")
        
        if not isinstance(color, PieceColor):
            raise TypeError("Player(self, profile, color) L'attribut color doit être du type PieceColor.")
        
        self.profile: Profile = profile
        self.color: PieceColor = color