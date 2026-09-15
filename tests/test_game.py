from src.chess.case import Case
from src.chess.exceptions.illegal_move_error import IllegalMoveError
from src.chess.game import Game
from src.chess.board import Board
from src.chess.move import Move, SpecialMove
from src.chess.player import Player
from src.chess.profile import Profile
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
import pytest

@pytest.fixture
def normal_game() -> Game:
    profiles: list[Profile] = [Profile(), Profile()]
    return Game(profiles)

@pytest.fixture
def game_with_empty_board() -> Game:
    profiles: list[Profile] = [Profile(), Profile()]
    game = Game(profiles)
    game.board = Board()
    return game

def test_game_correct_number_of_players(normal_game: Game) -> None:
    assert len(normal_game.players) == 2

@pytest.mark.parametrize("profiles", [
    ([]),
    ([Profile()]),
    ([Profile(), Profile(), Profile()])
])
def test_game_incorrect_number_of_players(profiles: list[Profile]) -> None:
    with pytest.raises(ValueError):
        Game(profiles)

def test_game_player_color(normal_game: Game) -> None:
    colors = [player.color for player in normal_game.players]
    assert colors.count(PieceColor.WHITE) == 1
    assert colors.count(PieceColor.BLACK) == 1

def test_game_current_player_is_one_of_the_players(normal_game: Game) -> None:
    assert normal_game.current_player in normal_game.players

def test_game_current_player_is_white(normal_game: Game) -> None:
    assert normal_game.current_player.color == PieceColor.WHITE

def test_game_winner_is_none(normal_game: Game) -> None:
    assert normal_game.winner is None

def test_game_moves_is_empty(normal_game: Game) -> None:
    assert normal_game.moves == []

@pytest.mark.parametrize("line, column, expected_legal_moves", [
    (0, 4, [(1, 5), (0, 5), (0, 3), (1, 3)]),
    (4, 7, [(7, 4), (1, 4)]),
    (4, 1, [(4, 4), (7, 4), (1, 4)])
])
def test_game_get_legal_moves(game_with_empty_board: Game, line: int, column: int, expected_legal_moves: list[tuple[int, int]]) -> None:
    game_with_empty_board.board.grid[0][4].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[4][7].content = Bishop(PieceColor.WHITE)
    game_with_empty_board.board.grid[4][1].content = Queen(PieceColor.WHITE)
    game_with_empty_board.board.grid[7][4].content = Rook(PieceColor.BLACK)

    assert game_with_empty_board.get_legal_moves(line, column) == [game_with_empty_board.board.grid[move[0]][move[1]] for move in expected_legal_moves]

@pytest.mark.parametrize("expected_legal_moves", [
    (0, 3),
    (1, 3),
    (0, 5),
    (1, 5),
    (1, 4),
    (7, 4),
    (4, 4),
    (7, 4),
    (1, 4)
])
def test_game_get_color_every_legal_moves(game_with_empty_board: Game, expected_legal_moves: tuple[int, int]) -> None:
    game_with_empty_board.board.grid[0][4].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[4][7].content = Bishop(PieceColor.WHITE)
    game_with_empty_board.board.grid[4][1].content = Queen(PieceColor.WHITE)
    game_with_empty_board.board.grid[7][4].content = Rook(PieceColor.BLACK)

    legal_moves: list[Case] = game_with_empty_board.get_color_every_legal_moves(PieceColor.WHITE)
    assert len(legal_moves) == 9
    assert game_with_empty_board.board.grid[expected_legal_moves[0]][expected_legal_moves[1]] in legal_moves

def test_game_switch_players(normal_game: Game) -> None:
    current_player_before_switch: Player = normal_game.current_player
    normal_game.switch_players()
    assert normal_game.current_player != current_player_before_switch
    assert normal_game.current_player in normal_game.players

def test_game_get_castling_moves(game_with_empty_board: Game) -> None:
    game_with_empty_board.board.grid[0][4].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[0][0].content = Rook(PieceColor.WHITE)
    game_with_empty_board.board.grid[0][7].content = Rook(PieceColor.WHITE)

    castling_moves: list[Case] = game_with_empty_board.get_castling_moves(0, 4)
    assert len(castling_moves) == 2
    assert game_with_empty_board.board.grid[0][2] in castling_moves
    assert game_with_empty_board.board.grid[0][6] in castling_moves

    game_with_empty_board.board.grid[0][0].content.has_moved = True
    castling_moves = game_with_empty_board.get_castling_moves(0, 4)
    assert len(castling_moves) == 1
    assert game_with_empty_board.board.grid[0][6] in castling_moves

    game_with_empty_board.board.grid[7][5].content = Rook(PieceColor.BLACK)
    castling_moves = game_with_empty_board.get_castling_moves(0, 4)
    assert len(castling_moves) == 0

def test_game_get_en_passant_moves(normal_game: Game) -> None:
    normal_game.play_move(Move(normal_game.board.grid[1][4], normal_game.board.grid[3][4]))
    normal_game.play_move(Move(normal_game.board.grid[6][4], normal_game.board.grid[5][4]))
    normal_game.play_move(Move(normal_game.board.grid[3][4], normal_game.board.grid[4][4]))
    normal_game.play_move(Move(normal_game.board.grid[6][5], normal_game.board.grid[4][5]))

    en_passant_moves: list[Case] = normal_game.get_en_passant_moves(4, 4)
    assert len(en_passant_moves) == 1
    assert normal_game.board.grid[5][5] in en_passant_moves

def test_game_get_king_case(game_with_empty_board: Game) -> None:
    game_with_empty_board.board.grid[0][4].content = King(PieceColor.WHITE)
    king_case: Case = game_with_empty_board.board.get_king_case(PieceColor.WHITE)
    assert king_case.line == 0
    assert king_case.column == 4

    with pytest.raises(Exception):
        game_with_empty_board.board.get_king_case(PieceColor.BLACK)

def test_game_is_stalemate(game_with_empty_board: Game) -> None:
    game_with_empty_board.board.grid[0][0].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[7][7].content = King(PieceColor.BLACK)
    game_with_empty_board.board.grid[7][1].content = Rook(PieceColor.BLACK)
    game_with_empty_board.board.grid[1][7].content = Rook(PieceColor.BLACK)

    assert game_with_empty_board.is_stalemate(PieceColor.WHITE) == True
    assert game_with_empty_board.is_stalemate(PieceColor.BLACK) == False

def test_game_is_checkmate(game_with_empty_board: Game) -> None:
    game_with_empty_board.board.grid[0][0].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[7][7].content = King(PieceColor.BLACK)
    game_with_empty_board.board.grid[7][0].content = Rook(PieceColor.BLACK)
    game_with_empty_board.board.grid[1][0].content = Queen(PieceColor.BLACK)

    assert game_with_empty_board.is_checkmate(PieceColor.WHITE) == True
    assert game_with_empty_board.is_checkmate(PieceColor.BLACK) == False

def test_game_is_game_over(game_with_empty_board: Game) -> None:
    game_with_empty_board.board.grid[0][0].content = King(PieceColor.WHITE)
    game_with_empty_board.board.grid[7][7].content = King(PieceColor.BLACK)
    assert game_with_empty_board.is_game_over(game_with_empty_board.current_player) == False
    game_with_empty_board.board.grid[7][0].content = Rook(PieceColor.BLACK)
    game_with_empty_board.board.grid[1][0].content = Queen(PieceColor.BLACK)
    assert game_with_empty_board.is_game_over(game_with_empty_board.current_player) == True

def test_game_promotion(game_with_empty_board: Game) -> None:
    game_with_empty_board.board.grid[1][0].content = Pawn(PieceColor.BLACK)
    game_with_empty_board.board.grid[6][0].content = Pawn(PieceColor.WHITE)
    game_with_empty_board.board.grid[6][4].content = King(PieceColor.BLACK)
    game_with_empty_board.board.grid[1][4].content = King(PieceColor.WHITE)

    game_with_empty_board.play_move(Move(game_with_empty_board.board.grid[6][0], game_with_empty_board.board.grid[7][0], SpecialMove.PROMOTION, Rook))
    assert isinstance(game_with_empty_board.board.grid[7][0].content, Rook)
    assert game_with_empty_board.board.grid[7][0].content.piece_color == PieceColor.WHITE

    game_with_empty_board.play_move(Move(game_with_empty_board.board.grid[1][0], game_with_empty_board.board.grid[0][0], SpecialMove.PROMOTION, Queen))
    assert isinstance(game_with_empty_board.board.grid[0][0].content, Queen)
    assert game_with_empty_board.board.grid[0][0].content.piece_color == PieceColor.BLACK

@pytest.mark.parametrize("case1, case2", [
    ((1, 0), (3, 0)),
    ((6, 0), (4, 0)),
    ((0, 1), (2, 2)),
    ((7, 1), (5, 2)),
])
def test_game_play_move(normal_game: Game, case1: tuple[int, int], case2: tuple[int, int]) -> None:
    case: Case = normal_game.board.grid[case1[0]][case1[1]]
    assert isinstance(case.content, Piece)
    piece: Piece = case.content
    if piece.piece_color != normal_game.current_player.color:
        normal_game.switch_players()
    assert piece.piece_color == normal_game.current_player.color
    move: Move = Move(case, normal_game.board.grid[case2[0]][case2[1]])
    normal_game.play_move(move)
    assert normal_game.board.grid[case2[0]][case2[1]].content == piece
    assert case.content is None
    assert normal_game.moves[-1] == move
    assert normal_game.current_player.color != piece.piece_color

def test_game_play_move_illegal_move(normal_game: Game) -> None:
    case: Case = normal_game.board.grid[0][0]
    assert isinstance(case.content, Piece)
    move: Move = Move(case, normal_game.board.grid[2][2])
    with pytest.raises(IllegalMoveError):
        normal_game.play_move(move)

def test_game_play_move_wrong_color(normal_game: Game) -> None:
    case: Case = normal_game.board.grid[6][0]
    assert isinstance(case.content, Piece)
    move: Move = Move(case, normal_game.board.grid[4][0])
    with pytest.raises(IllegalMoveError):
        normal_game.play_move(move)