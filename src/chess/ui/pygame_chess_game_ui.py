from src.chess.ai.ai_player import AIPlayer
from src.chess.case import Case
from src.chess.constants import BOARD_SIZE, CASE_SIZE
from src.chess.game import Game, GameStatus
from src.chess.move import Move
from src.chess.pieces.bishop import Bishop
from src.chess.pieces.king import King
from src.chess.pieces.knight import Knight
from src.chess.pieces.pawn import Pawn
from src.chess.pieces.piece import Piece, PieceColor
from src.chess.pieces.queen import Queen
from src.chess.pieces.rook import Rook
from src.chess.profile import Profile
import pygame

def board_line_to_pygame_line(line: int) -> int:
    return (BOARD_SIZE - 1 - line) * CASE_SIZE

def board_position_to_pygame_position(position: tuple[int, int]) -> tuple[int, int]:
    return (position[1] * CASE_SIZE, board_line_to_pygame_line(position[0]))

def pygame_line_to_board_line(line: int) -> int:
    return BOARD_SIZE - 1 - (line // CASE_SIZE)

def pygame_position_to_board_position(position: tuple[int, int]) -> tuple[int, int]:
    return (pygame_line_to_board_line(position[1]), position[0] // CASE_SIZE)

def piece_type_to_str(piece: Piece) -> str:
    if not isinstance(piece, Piece):
        raise TypeError("piece_type_to_str Le paramètre piece doit être du type Piece.")
    
    elif isinstance(piece, Bishop):
        return "Bishop"

    elif isinstance(piece, Knight):
        return "Knight"

    elif isinstance(piece, King):
        return "King"

    elif isinstance(piece, Pawn):
        return "Pawn"

    elif isinstance(piece, Queen):
        return "Queen"
    
    elif isinstance(piece, Rook):
        return "Rook"

    else:
        return "None"

def get_piece_image(piece_name: str) -> pygame.Surface:
    return pygame.image.load("images/pieces/" + piece_name + ".png")

def display_possible_promotion(screen, game: Game, color: PieceColor):
    pieces: list[Piece] = [Bishop(color), Knight(color), Queen(color), Rook(color)]
    line: int = 1 if color == PieceColor.BLACK else 6
    column: int = 2
    for piece in pieces:
        piece_name: str = piece_type_to_str(piece)
        piece_color: str = piece.piece_color.value
        piece_full_name: str = piece_color + "_" + piece_name
        piece_image: pygame.Surface = get_piece_image(piece_full_name)
        piece_image = pygame.transform.scale(piece_image, (CASE_SIZE, CASE_SIZE))
        position: tuple[int, int] = (line, column)

        position = board_position_to_pygame_position(position)
        screen.blit(piece_image, (position[0], position[1]))
        column += 1

def get_promotion_choice(game: Game, move: Move):
    running_promotion: bool = True
    while running_promotion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_promotion = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                board_position: tuple[int, int] = pygame_position_to_board_position(event.pos)
                line: int = 1 if game.current_player.color == PieceColor.BLACK else 6
                bishop_pos: tuple[int, int] = (line, 2)
                knight_pos: tuple[int, int] = (line, 3)
                queen_pos: tuple[int, int] = (line, 4)
                rook_pos: tuple[int, int] = (line, 5)

                if board_position in [bishop_pos, knight_pos, queen_pos, rook_pos]:
                    if board_position == bishop_pos:
                        move.promotion_piece_type = Bishop
                    elif board_position == knight_pos:
                        move.promotion_piece_type = Knight
                    elif board_position == queen_pos:
                        move.promotion_piece_type = Queen
                    elif board_position == rook_pos:
                        move.promotion_piece_type = Rook
                    running_promotion = False

def display_chess_board(screen) -> None:
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if (i + j) % 2 == 0:
                color = (50, 50, 50)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, (i * CASE_SIZE, board_line_to_pygame_line(j), CASE_SIZE, CASE_SIZE))

def display_chess_piece(screen, game: Game, position: tuple[int, int]) -> None:
    case: Case = game.board.grid[position[0]][position[1]]
    if isinstance(case.content, Piece):
        piece_name: str = piece_type_to_str(case.content)
        piece_color: str = case.content.piece_color.value
        piece_full_name: str = piece_color + "_" + piece_name
        piece_image: pygame.Surface = get_piece_image(piece_full_name)
        piece_image = pygame.transform.scale(piece_image, (CASE_SIZE, CASE_SIZE))

        position = board_position_to_pygame_position(position)
        screen.blit(piece_image, (position[0], position[1]))

def display_chess_pieces(screen, game: Game):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            case: Case = game.board.grid[i][j]
            if isinstance(case.content, Piece):
                display_chess_piece(screen, game, (i, j))

def display_game(screen, game: Game):
    display_chess_board(screen)
    display_chess_pieces(screen, game)

def turn_case_to_yellow(screen, position: tuple[int, int]):
    pygame_position: tuple[int, int] = board_position_to_pygame_position(position)
    yellow_case: pygame.Surface = pygame.Surface((CASE_SIZE, CASE_SIZE))
    yellow_case.set_alpha(128)
    yellow_case.fill((255, 255, 0))
    screen.blit(yellow_case, (pygame_position[0], pygame_position[1]))
    #pygame.draw.rect(screen, (255, 255, 0, 0), (pygame_position[0], pygame_position[1], CASE_SIZE, CASE_SIZE))

def pygame_main(game: Game) -> None:
    pygame.init()

    ai: AIPlayer = AIPlayer(Profile(), PieceColor.BLACK)

    chess_screen = pygame.display.set_mode((BOARD_SIZE * CASE_SIZE - 1, BOARD_SIZE * CASE_SIZE - 1))

    running: bool = True
    game_running: bool = True
    piece_legal_moves: list[Case] = []
    selected_case: Case | None = None

    display_game(chess_screen, game)
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        while game_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    board_position: tuple[int, int] = pygame_position_to_board_position(event.pos)
                    case: Case = game.board.grid[board_position[0]][board_position[1]]
                    if (isinstance(case.content, Piece) and 
                        case.content.piece_color == game.current_player.color):
                        selected_case = case
                        piece_legal_moves = game.get_legal_moves(board_position[0], board_position[1])
                        display_game(chess_screen, game)
                        for case in piece_legal_moves:
                            turn_case_to_yellow(chess_screen, (case.line, case.column))
                        display_chess_pieces(chess_screen, game)
                    else:
                        if (case in piece_legal_moves and 
                            selected_case is not None):
                            move: Move = Move(selected_case, case)
                            if game.is_promotion(move):
                                display_possible_promotion(chess_screen, game, game.current_player.color)
                                pygame.display.flip()
                                get_promotion_choice(game, move)
                            game.play_move(move)
                            piece_legal_moves = []
                            ai.minimax_depth_1(game)
                        display_game(chess_screen, game)
                        selected_case = None

            if game.status not in [GameStatus.IN_PROGRESS, GameStatus.CHECK]:
                print(game.status.value)
                if game.status == GameStatus.CHECKMATE and game.winner is not None:
                    print("winner : " + game.winner.color.value)
                else:
                    print("draw")
                game_running = False
            pygame.display.flip()
    pygame.quit()