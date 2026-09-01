from src.chess.board import Board
from src.chess.case import Case
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.constants import BOARD_SIZE
import pytest

@pytest.fixture
def empty_board() -> Board:
    return Board()

@pytest.fixture
def initial_board_configuration() -> Board:
    board = Board()
    board.create_initial_board()
    return board

@pytest.fixture
def board_without_pawn() -> Board:
    board = Board()
    initial_configuration: list[list[Piece|None]] = \
        [[Rook(PieceColor.WHITE), Knight(PieceColor.WHITE), Bishop(PieceColor.WHITE), Queen(PieceColor.WHITE), King(PieceColor.WHITE), Bishop(PieceColor.WHITE), Knight(PieceColor.WHITE), Rook(PieceColor.WHITE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [Rook(PieceColor.BLACK), Knight(PieceColor.BLACK), Bishop(PieceColor.BLACK), Queen(PieceColor.BLACK), King(PieceColor.BLACK), Bishop(PieceColor.BLACK), Knight(PieceColor.BLACK), Rook(PieceColor.BLACK)]]
    board.fill(initial_configuration)
    return board

def test_board_creation(empty_board: Board):
    assert len(empty_board.grid) == BOARD_SIZE, f"Le plateau doit avoir {BOARD_SIZE} lignes."
    for row in empty_board.grid:
        assert len(row) == BOARD_SIZE, f"Chaque ligne du plateau doit avoir {BOARD_SIZE} colonnes."
        for case in row:
            assert isinstance(case, Case), "Chaque élément du plateau doit être une instance de Case."
            assert case.content is None, "Chaque case doit être initialement vide (content = None)."

def test_board_fill(empty_board: Board):
    pieces: list[list[Piece | None]] = [[Rook(PieceColor.WHITE) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    empty_board.fill(pieces)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            piece = empty_board.grid[i][j].content
            assert isinstance(piece, Piece), "Chaque élément du plateau doit être une instance de Piece."
            assert piece.piece_color == PieceColor.WHITE, "La pièce doit être blanche."

def test_board_fill_invalid_size(empty_board: Board):
    invalid_pieces: list[list[Piece | None]] = [[Rook(PieceColor.WHITE) for _ in range(BOARD_SIZE - 1)] for _ in range(BOARD_SIZE)]
    with pytest.raises(ValueError):
        empty_board.fill(invalid_pieces)

    invalid_pieces = [[Rook(PieceColor.WHITE) for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE - 1)]
    with pytest.raises(ValueError):
        empty_board.fill(invalid_pieces)

def test_board_fill_with_none(empty_board: Board):
    pieces: list[list[Piece | None]] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    empty_board.fill(pieces)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            assert empty_board.grid[i][j].content is None

def test_board_fill_initial_configuration_count(initial_board_configuration: Board):
    count_pieces = sum(1 for row in initial_board_configuration.grid for case in row if isinstance(case.content, Piece))
    count_none = sum(1 for row in initial_board_configuration.grid for case in row if case.content is None)
    count_white_pieces = sum(1 for row in initial_board_configuration.grid for case in row if isinstance(case.content, Piece) and case.content.piece_color == PieceColor.WHITE)
    count_black_pieces = sum(1 for row in initial_board_configuration.grid for case in row if isinstance(case.content, Piece) and case.content.piece_color == PieceColor.BLACK)
    assert count_pieces == 32, "Il doit y avoir 32 pièces sur le plateau."
    assert count_none == 32, "Il doit y avoir 32 cases vides sur le plateau."
    assert count_white_pieces == 16, "Il doit y avoir 16 pièces blanches sur le plateau."
    assert count_black_pieces == 16, "Il doit y avoir 16 pièces noires sur le plateau."

@pytest.mark.parametrize("line, column, expected_piece_type, expected_piece_color", [
    (0, 0, Rook, PieceColor.WHITE),
    (0, 4, King, PieceColor.WHITE),
    (1, 3, Pawn, PieceColor.WHITE),
    (6, 5, Pawn, PieceColor.BLACK),
    (7, 4, King, PieceColor.BLACK),
    (7, 0, Rook, PieceColor.BLACK)
])
def test_board_fill_initial_configuration_content(initial_board_configuration: Board, line: int, column: int, expected_piece_type: type[Piece], expected_piece_color: PieceColor):
    piece = initial_board_configuration.grid[line][column].content
    assert isinstance(piece, expected_piece_type), "Le type de la pièce est incorrect."
    assert piece.piece_color == expected_piece_color, "La couleur de la pièce est incorrecte."

@pytest.mark.parametrize("line, column, expected_type", [
    (0, 0, type(None)),
    (0, 4, type(None)),
    (1, 3, Piece),
    (6, 5, Piece),
    (7, 4, type(None)),
    (7, 0, type(None))
])
def test_board_fill_overwrite_existing_content(initial_board_configuration: Board, line: int, column: int, expected_type: type):
    new_board_configuration: list[list[Piece | None]] = \
        [[None for _ in range(BOARD_SIZE)],
        [Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)],
        [Pawn(PieceColor.WHITE) for _ in range(BOARD_SIZE)],
        [None for _ in range(BOARD_SIZE)]]
    initial_board_configuration.fill(new_board_configuration)
    assert isinstance(initial_board_configuration.grid[line][column].content, expected_type), "Le type de contenu de la case est incorrect après l'écrasement des pièces existantes."


@pytest.mark.parametrize("line, column, expected_moves", [
    (0, 1, [(1, 3), (2, 2), (2, 0)]),
    (7, 1, [(6, 3), (5, 2), (5, 0)])
])
def test_board_get_possible_moves_knight(board_without_pawn: Board, line: int, column: int, expected_moves: list[tuple[int, int]]):
    possible_moves: list[Case] = board_without_pawn.get_possible_moves(line, column)
    expected_moves_case: list[Case] = [board_without_pawn.grid[move[0]][move[1]] for move in expected_moves]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le cavalier sont incorrects."

def test_board_get_possible_moves_knight_ennemy_piece(empty_board: Board):
    empty_board.grid[4][4].content = Knight(PieceColor.WHITE)
    empty_board.grid[5][6].content = Pawn(PieceColor.BLACK)
    possible_moves: list[Case] = empty_board.get_possible_moves(4, 4)
    expected_moves_case: list[Case] = [empty_board.grid[5][6], empty_board.grid[6][5], empty_board.grid[3][6], empty_board.grid[2][5], empty_board.grid[5][2], empty_board.grid[6][3], empty_board.grid[3][2], empty_board.grid[2][3]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le cavalier avec une pièce ennemie sont incorrects."

def test_board_get_possible_moves_knight_friendly_piece(empty_board: Board):
    empty_board.grid[4][4].content = Knight(PieceColor.WHITE)
    empty_board.grid[5][6].content = Pawn(PieceColor.WHITE)
    possible_moves: list[Case] = empty_board.get_possible_moves(4, 4)
    expected_moves_case: list[Case] = [empty_board.grid[6][5], empty_board.grid[3][6], empty_board.grid[2][5], empty_board.grid[5][2], empty_board.grid[6][3], empty_board.grid[3][2], empty_board.grid[2][3]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le cavalier avec une pièce amie sont incorrects."

@pytest.mark.parametrize("line, column, expected_moves", [
    (0, 0, [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]),
    (7, 0, [(6, 0), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0), (0, 0)])
])
def test_board_get_possible_moves_rook(board_without_pawn: Board, line: int, column: int, expected_moves: list[tuple[int, int]]):
    # Test possible moves for a white rook at (0, 0)
    possible_moves = board_without_pawn.get_possible_moves(line, column)
    expected_moves_case = [board_without_pawn.grid[move[0]][move[1]] for move in expected_moves]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour la tour sont incorrects."

def test_board_get_possible_moves_rook_ennemy_piece(empty_board: Board):
    empty_board.grid[0][0].content = Rook(PieceColor.WHITE)
    empty_board.grid[0][3].content = Pawn(PieceColor.BLACK)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 0)
    expected_moves_case: list[Case] = [empty_board.grid[1][0], empty_board.grid[2][0], empty_board.grid[3][0], empty_board.grid[4][0], empty_board.grid[5][0], empty_board.grid[6][0], empty_board.grid[7][0], empty_board.grid[0][1], empty_board.grid[0][2], empty_board.grid[0][3]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour la tour avec une pièce ennemie sont incorrects."

def test_board_get_possible_moves_rook_friendly_piece(empty_board: Board):
    empty_board.grid[0][0].content = Rook(PieceColor.WHITE)
    empty_board.grid[0][3].content = Pawn(PieceColor.WHITE)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 0)
    expected_moves_case: list[Case] = [empty_board.grid[1][0], empty_board.grid[2][0], empty_board.grid[3][0], empty_board.grid[4][0], empty_board.grid[5][0], empty_board.grid[6][0], empty_board.grid[7][0], empty_board.grid[0][1], empty_board.grid[0][2]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour la tour avec une pièce amie sont incorrects."

@pytest.mark.parametrize("line, column, expected_moves", [
    (0, 2, [(1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (1, 1), (2, 0)]),
    (7, 2, [(6, 3), (5, 4), (4, 5), (3, 6), (2, 7), (6, 1), (5, 0)])
])
def test_board_get_possible_moves_bishop(board_without_pawn: Board, line: int, column: int, expected_moves: list[tuple[int, int]]):
    # Test possible moves for a white bishop at (0, 2)
    possible_moves = board_without_pawn.get_possible_moves(line, column)
    expected_moves_case = [board_without_pawn.grid[move[0]][move[1]] for move in expected_moves]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le fou sont incorrects."

def test_board_get_possible_moves_bishop_ennemy_piece(empty_board: Board):
    empty_board.grid[0][2].content = Bishop(PieceColor.WHITE)
    empty_board.grid[3][5].content = Pawn(PieceColor.BLACK)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 2)
    expected_moves_case: list[Case] = [empty_board.grid[1][3], empty_board.grid[2][4], empty_board.grid[3][5], empty_board.grid[1][1], empty_board.grid[2][0]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le fou avec une pièce ennemie sont incorrects."

def test_board_get_possible_moves_bishop_friendly_piece(empty_board: Board):
    empty_board.grid[0][2].content = Bishop(PieceColor.WHITE)
    empty_board.grid[3][5].content = Pawn(PieceColor.WHITE)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 2)
    expected_moves_case: list[Case] = [empty_board.grid[1][3], empty_board.grid[2][4], empty_board.grid[1][1], empty_board.grid[2][0]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le fou avec une pièce amie sont incorrects."

@pytest.mark.parametrize("line, column, expected_moves", [
    (0, 3, [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (1, 4), (2, 5), (3, 6), (4, 7), (1, 2), (2, 1), (3, 0)]),
    (7, 3, [(6, 3), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (0, 3), (6, 4), (5, 5), (4, 6), (3, 7), (6, 2), (5, 1), (4, 0)])
])
def test_board_get_possible_moves_queen(board_without_pawn: Board, line: int, column: int, expected_moves: list[tuple[int, int]]):
    # Test possible moves for a white queen at (0, 3)
    possible_moves = board_without_pawn.get_possible_moves(line, column)
    expected_moves_case = [board_without_pawn.grid[move[0]][move[1]] for move in expected_moves]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour la reine sont incorrects."

def test_board_get_possible_moves_queen_ennemy_piece(empty_board: Board):
    empty_board.grid[0][3].content = Queen(PieceColor.WHITE)
    empty_board.grid[3][6].content = Pawn(PieceColor.BLACK)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 3)
    expected_moves_case: list[Case] = [empty_board.grid[1][3], empty_board.grid[2][3], empty_board.grid[3][3], empty_board.grid[4][3], empty_board.grid[5][3], empty_board.grid[6][3], empty_board.grid[7][3], empty_board.grid[0][4], empty_board.grid[0][5], empty_board.grid[0][6], empty_board.grid[0][7], empty_board.grid[0][2], empty_board.grid[0][1], empty_board.grid[0][0], empty_board.grid[1][4], empty_board.grid[2][5], empty_board.grid[3][6], empty_board.grid[1][2], empty_board.grid[2][1], empty_board.grid[3][0]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour la reine avec une pièce ennemie sont incorrects."

def test_board_get_possible_moves_queen_friendly_piece(empty_board: Board):
    empty_board.grid[0][3].content = Queen(PieceColor.WHITE)
    empty_board.grid[3][6].content = Pawn(PieceColor.WHITE)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 3)
    expected_moves_case: list[Case] = [empty_board.grid[1][3], empty_board.grid[2][3], empty_board.grid[3][3], empty_board.grid[4][3], empty_board.grid[5][3], empty_board.grid[6][3], empty_board.grid[7][3], empty_board.grid[0][4], empty_board.grid[0][5], empty_board.grid[0][6], empty_board.grid[0][7], empty_board.grid[0][2], empty_board.grid[0][1], empty_board.grid[0][0], empty_board.grid[1][4], empty_board.grid[2][5], empty_board.grid[1][2], empty_board.grid[2][1], empty_board.grid[3][0]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour la reine avec une pièce amie sont incorrects."

@pytest.mark.parametrize("line, column, expected_moves", [
    (0, 4, [(1, 4), (1, 5), (1, 3)]),
    (7, 4, [(6, 5), (6, 4), (6, 3)])
])
def test_board_get_possible_moves_king(board_without_pawn: Board, line: int, column: int, expected_moves: list[tuple[int, int]]):
    # Test possible moves for a white king at (0, 4)
    possible_moves = board_without_pawn.get_possible_moves(line, column)
    expected_moves_case = [board_without_pawn.grid[move[0]][move[1]] for move in expected_moves]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le roi sont incorrects."

def test_board_get_possible_moves_king_ennemy_piece(empty_board: Board):
    empty_board.grid[0][4].content = King(PieceColor.WHITE)
    empty_board.grid[1][5].content = Pawn(PieceColor.BLACK)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 4)
    expected_moves_case: list[Case] = [empty_board.grid[1][4], empty_board.grid[1][5], empty_board.grid[0][5], empty_board.grid[0][3], empty_board.grid[1][3]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le roi avec une pièce ennemie sont incorrects."

def test_board_get_possible_moves_king_friendly_piece(empty_board: Board):
    empty_board.grid[0][4].content = King(PieceColor.WHITE)
    empty_board.grid[1][5].content = Pawn(PieceColor.WHITE)
    possible_moves: list[Case] = empty_board.get_possible_moves(0, 4)
    expected_moves_case: list[Case] = [empty_board.grid[1][4], empty_board.grid[0][5], empty_board.grid[0][3], empty_board.grid[1][3]]
    assert possible_moves == expected_moves_case, "Les mouvements possibles pour le roi avec une pièce amie sont incorrects."

@pytest.mark.parametrize("line, column, expected_moves", [
    (1, 0, [(2, 0), (3, 0)]),
    (1, 4, [(2, 4), (3, 4)]),
    (6, 2, [(5, 2), (4, 2)]),
    (6, 7, [(5, 7), (4, 7)])
])
def test_board_get_possible_moves_pawn(initial_board_configuration: Board, line: int, column: int, expected_moves: list[tuple[int, int]]):
    possible_moves: list[Case] = initial_board_configuration.get_possible_moves(line, column)
    expected_move_cases: list[Case] = [initial_board_configuration.grid[move[0]][move[1]] for move in expected_moves]
    assert possible_moves == expected_move_cases, "Les mouvements possibles pour le pion sont incorrects"

def test_board_get_possible_moves_pawn_ennemy_blocking(empty_board: Board):
    white_pawn: Pawn = Pawn(PieceColor.WHITE)
    black_pawn: Pawn = Pawn(PieceColor.BLACK)
    empty_board.grid[3][4].content = white_pawn
    empty_board.grid[4][4].content = black_pawn
    white_pawn_possible_moves: list[Case] = empty_board.get_possible_moves(3, 4)
    black_pawn_possible_moves: list[Case] = empty_board.get_possible_moves(4, 4)
    assert white_pawn_possible_moves == []
    assert black_pawn_possible_moves == []

def test_board_get_possible_moves_pawn_ennemy_capture(empty_board: Board):
    white_pawn: Pawn = Pawn(PieceColor.WHITE)
    black_pawn: Pawn = Pawn(PieceColor.BLACK)
    white_pawn.has_moved = True
    black_pawn.has_moved = True
    empty_board.grid[3][4].content = white_pawn
    empty_board.grid[4][3].content = black_pawn
    white_pawn_possible_moves: list[Case] = empty_board.get_possible_moves(3, 4)
    black_pawn_possible_moves: list[Case] = empty_board.get_possible_moves(4, 3)
    assert white_pawn_possible_moves == [empty_board.grid[4][4], empty_board.grid[4][3]]
    assert black_pawn_possible_moves == [empty_board.grid[3][3], empty_board.grid[3][4]]

def test_board_get_possible_moves_pawn_ally_blocking(empty_board: Board):
    white_pawn: Pawn = Pawn(PieceColor.WHITE)
    second_white_pawn: Pawn = Pawn(PieceColor.WHITE)
    second_white_pawn.has_moved = True
    empty_board.grid[3][4].content = white_pawn
    empty_board.grid[4][4].content = second_white_pawn
    white_pawn_possible_moves: list[Case] = empty_board.get_possible_moves(3, 4)
    second_white_pawn_possible_moves: list[Case] = empty_board.get_possible_moves(4, 4)
    assert white_pawn_possible_moves == []
    assert second_white_pawn_possible_moves == [empty_board.grid[5][4]]

@pytest.mark.parametrize("line, column", [(3, 3), (4, 4), (5, 5)])
def test_board_get_possible_moves_empty_case(board_without_pawn: Board, line: int, column: int):
    assert board_without_pawn.get_possible_moves(line, column) == []
