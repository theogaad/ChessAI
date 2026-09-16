from src.chess.game import Game
from src.chess.move import Move
from src.chess.profile import Profile



Theo: Profile = Profile()
Ia: Profile = Profile()

# Simulation d'une partie (Mat du berger)
game: Game = Game([Profile(), Profile()])
list_of_moves: list[list[tuple[int, int]]] = [
    [(1, 4), (2, 4)], 
    [(6, 4), (5, 4)],
    [(0, 5), (3, 2)],
    [(5, 4), (4, 4)],
    [(0, 3), (2, 5)],
    [(4, 4), (3, 4)],
    [(2, 5), (6, 5)]
]
for moves in list_of_moves:
    print(game.status)
    move: Move = Move(game.board.grid[moves[0][0]][moves[0][1]], game.board.grid[moves[1][0]][moves[1][1]])
    game.play_move(move)
print(game.status)