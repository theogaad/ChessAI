from src.chess.case import Case
from src.chess.move import Move, MoveType
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.piece import PieceColor
from src.chess.position import Position

case1: Case = Case(Position(0, 0), Bishop(PieceColor.WHITE))
case2: Case = Case(Position(7, 7), King(PieceColor.BLACK))

move1: Move = Move(case1, case2)
move2: Move = Move(case2, case1)

print(move1)
print(move2)

if case1.content:
    case1.content.get_reachable_positions_from_position(case1.position)