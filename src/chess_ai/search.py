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
from src.chess_engine.types import Color, PieceValue
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

        #minimax_best_moves: list[Move] = self.minimax(search_position, legal_moves, depth)
        negamax_best_moves: list[Move] = self.negamax(search_position, legal_moves, depth)

        best_moves: list[Move] = negamax_best_moves

        if len(best_moves) == 0:
            return None

        return choice(best_moves)

    def minimax(
        self, 
        position: Position, 
        legal_moves: list[Move], 
        depth: int
    ) -> list[Move]:
        best_moves: list[Move] = []
        best_move_value: int = -INF
        alpha: int = -INF
        beta: int = INF

        for move in legal_moves:
            undo_info: UndoInfo = self._move_executor.make_move(position, move)

            move_value: int = self.minimax_recursive(
                position, 
                legal_moves, 
                depth - 1, 
                False, 
                alpha, 
                beta
            )

            self._move_executor.undo_move(position, move, undo_info)

            if move_value > best_move_value:
                best_moves.clear()
                best_move_value = move_value
                best_moves.append(move)

            elif move_value == best_move_value:
                best_moves.append(move)

            alpha = max(alpha, best_move_value)

            if alpha >= beta:
                break

        return best_moves

    def minimax_recursive(
        self, 
        position: Position,
        legal_moves: list[Move], 
        depth: int, 
        maximizing: bool, 
        alpha: int, 
        beta: int
    ) -> int:
        legal_moves = self._move_generator.generate_legal_moves(position)
        if len(legal_moves) == 0:
            if self._move_generator._attack_generator.is_king_in_check(position, position.side_to_move):
                coeff: int = -1 if maximizing else 1

                return coeff * INF

            return 0

        elif depth == 0:
            coeff = 1 if maximizing else -1
            return coeff * self._evaluation.evaluate_position(position)

        elif maximizing:
            best_value = -INF

            for move in legal_moves:
                undo_info: UndoInfo = self._move_executor.make_move(position, move)
                
                move_value: int = self.minimax_recursive(
                    position, 
                    legal_moves, 
                    depth - 1, 
                    False, 
                    alpha, 
                    beta
                )
    
                self._move_executor.undo_move(position, move, undo_info)
    
                best_value = max(best_value, move_value)
                alpha = max(alpha, best_value)

                if alpha >= beta:
                    break

            return best_value

        else:
            worst_value = INF

            for move in legal_moves:
                undo_info = self._move_executor.make_move(position, move)
                
                move_value = self.minimax_recursive(
                    position, 
                    legal_moves, 
                    depth - 1, 
                    True, 
                    alpha, 
                    beta
                )
    
                self._move_executor.undo_move(position, move, undo_info)
    
                worst_value = min(worst_value, move_value)
                beta = min(beta, worst_value)

                if alpha >= beta:
                    break

            return worst_value

    def negamax(
        self, 
        position: Position, 
        legal_moves: list[Move], 
        depth: int
    ) -> list[Move]:
        best_moves: list[Move] = []
        best_move_value: int = -INF
        alpha: int = -INF
        beta: int = INF

        for move in legal_moves:
            undo_info: UndoInfo = self._move_executor.make_move(position, move)

            move_value: int = - self.negamax_recursive(
                position, 
                legal_moves, 
                depth - 1, 
                -alpha, 
                -beta
            )

            self._move_executor.undo_move(position, move, undo_info)

            if move_value > best_move_value:
                best_moves.clear()
                best_move_value = move_value
                best_moves.append(move)

            elif move_value == best_move_value:
                best_moves.append(move)

            alpha = max(alpha, best_move_value)

            if alpha >= beta:
                break

        return best_moves

    def negamax_recursive(
        self, 
        position: Position, 
        legal_moves: list[Move], 
        depth: int, 
        alpha: int, 
        beta: int
    ) -> int:
        legal_moves = self._move_generator.generate_legal_moves(position)
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
                    legal_moves, 
                    depth - 1, 
                    -alpha, 
                    -beta
                )
    
                self._move_executor.undo_move(position, move, undo_info)

                best_value = max(best_value, move_value)
                alpha = max(alpha, best_value)

                if alpha >= beta:
                    break

            return best_value

    def order_moves(
        self,
        position: Position,
        legal_moves: list[Move],
    ) -> list[Move]:
        ordered_moves = legal_moves

        return ordered_moves