from copy import deepcopy
from random import choice

from src.chess_ai.ai_request import AIRequest
from src.chess_ai.evaluation import Evaluation
from src.chess_engine.attack_generator import AttackGenerator
from src.chess_engine.constants import INF
from src.chess_engine.move import Move
from src.chess_engine.move_executor import MoveExecutor
from src.chess_engine.move_generator import MoveGenerator
from src.chess_engine.position import Position
from src.chess_engine.types import Color
from src.chess_engine.undo_info import UndoInfo
from src.chess_engine.zobrist import Zobrist


class Search:
    def __init__(self) -> None:
        self._move_executor: MoveExecutor = MoveExecutor(Zobrist())
        self._move_generator: MoveGenerator = MoveGenerator(
            AttackGenerator(), 
            self._move_executor
        )
        self._evaluation: Evaluation = Evaluation()

    def find_best_move(self, ai_request: AIRequest) -> Move | None:
        if len(ai_request.legal_moves) == 0:
            return None

        search_position: Position = deepcopy(ai_request.position)
        legal_moves: list[Move] = ai_request.legal_moves
        depth: int = ai_request.depth

        best_moves: list[Move] = self.negamax(search_position, legal_moves, depth)

        if len(best_moves) == 0:
            return None

        return choice(best_moves)

    def negamax(
        self, 
        position: Position, 
        legal_moves: list[Move], 
        depth: int
    ) -> list[Move]:
        best_moves: list[Move] = []
        best_move_value: int = -INF

        for move in legal_moves:
            undo_info: UndoInfo = self._move_executor.make_move(position, move)

            move_value: int = - self.negamax_recursive(
                position, 
                self._move_generator.generate_legal_moves(position), 
                depth - 1
            )

            self._move_executor.undo_move(position, move, undo_info)

            if move_value > best_move_value:
                best_moves.clear()
                best_move_value = move_value
                best_moves.append(move)

            elif move_value == best_move_value:
                best_moves.append(move)

        return best_moves

    def negamax_recursive(
        self, 
        position: Position, 
        legal_moves: list[Move], 
        depth: int, 
    ) -> int:
        if len(legal_moves) == 0:
            if self._move_generator._attack_generator.is_king_in_check(position, position.side_to_move):
                return -INF
            
            return 0

        elif depth == 0:
            return self._evaluation.evaluate_position(position)

        else:
            best_value: int = -INF

            for move in legal_moves:
                undo_info: UndoInfo = self._move_executor.make_move(position, move)
                
                move_value: int = - self.negamax_recursive(
                    position, 
                    self._move_generator.generate_legal_moves(position), 
                    depth - 1, 
                )
    
                self._move_executor.undo_move(position, move, undo_info)

                best_value = max(best_value, move_value)

            return best_value