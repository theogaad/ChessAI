from src.chess.game import Game, GameStatus
from src.chess.case import Case
from src.chess.move import Move
from src.chess.pieces.piece import Piece
from src.chess.profile import Profile
from src.chess.utils import is_valid_position



Theo: Profile = Profile()
Ia: Profile = Profile()

# Simulation d'une partie (Mat du berger)
game: Game = Game([Theo, Ia])
while game.status == GameStatus.IN_PROGRESS or game.status == GameStatus.CHECK:
    print("Couleur : " + game.current_player.color.value)
    print("Choisissez une pièce parmis ces coordonnées : ")
    for piece in game.board.get_color_all_pieces(game.current_player.color):
        position: None | tuple[int, int] = game.board.get_piece_position(piece)
        if position is not None:
            print("(" + str(position[0]) + ", " + str(position[1]) + ")")

    number_of_legal_moves: int = 0
    print()

    while number_of_legal_moves == 0:
        chosen_piece_line: int = int(input("Ligne : "))
        chosen_piece_column: int = int(input("Colonne : "))

        is_valid_position(chosen_piece_line, chosen_piece_column, "main (chosen_piece_line, chosen_piece_column)")

        chosen_case: Case = game.board.grid[chosen_piece_line][chosen_piece_column]
        assert chosen_case.content is not None, "La Case choisie doit contenir une Piece."
        chosen_piece: Piece = chosen_case.content

        number_of_legal_moves = len(game.get_legal_moves(chosen_piece_line, chosen_piece_column))
        if number_of_legal_moves == 0:
            print("Cette pièce ne peut pas effectuer de coup légal, veuillez choisir une autre pièce.")
        print()

    print("Choisissez un coup à jouer : ")
    print("Coups possibles par cette pièce :")

    piece_legal_moves: list[Case] = game.get_legal_moves(chosen_piece_line, chosen_piece_column)
    for moves in piece_legal_moves:
        print("(" + str(moves.line) + ", " + str(moves.column) + ")")
    print()

    move_line: int = int(input("Ligne : "))
    move_column: int = int(input("Colonne : "))
    is_valid_position(move_line, move_column, "main (move_line, move_column)")

    move_end_case: Case = game.board.grid[move_line][move_column]

    while move_end_case not in piece_legal_moves:
        print("Ce coup n'est pas légal, veuillez choisir un coup légal.")

        move_line = int(input("Ligne : "))
        move_column = int(input("Colonne : "))
        is_valid_position(move_line, move_column, "main (move_line, move_column)")

        move_end_case = game.board.grid[move_line][move_column]

    move: Move = Move(chosen_case, move_end_case)
    game.play_move(move)
    print(game.moves[-1])

# Ajouter gestion promotion