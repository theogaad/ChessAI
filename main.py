from src.chess.case import Case
from src.chess.move import Move, MoveType
from src.chess.pieces.king import King
from src.chess.pieces.piece import PieceColor
from src.chess.position import Position

case1: Case = Case(Position(0, 0), King(PieceColor.WHITE))
case2: Case = Case(Position(7, 7), King(PieceColor.BLACK))

move1: Move = Move(case1, case2)

print(move1)