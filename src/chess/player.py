from src.chess.profile import Profile
from src.chess.pieces.piece import PieceColor

class Player:
    def __init__(self, profile: Profile, color: PieceColor) -> None:
        self.profile: Profile = profile
        self.color: PieceColor = color