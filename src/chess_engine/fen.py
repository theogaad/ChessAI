from __future__ import annotations

from dataclasses import dataclass
import re
from typing import TYPE_CHECKING

from src.chess_engine.constants import BOARD_SIZE, PIECE_TYPE_NUMBER, ASCII_VALUE
from src.chess_engine.types import Color, PieceType, CastlingRights
from src.chess_engine.piece_bitboards import PieceBitboards

if TYPE_CHECKING:
    from src.chess_engine.position import Position


PIECE_TO_FEN: tuple[str] = (
    'K', 'Q', 'R', 'B', 'N', 'P', 
    'k', 'q', 'r', 'b', 'n', 'p'
)


@dataclass
class FENData:
    """Représente les données extraites d'une chaîne FEN.

    Cette classe regroupe les différentes informations nécessaires à la
    construction d'une position d'échecs à partir d'une chaîne FEN.

    Attributes:
        piece_bitboards: Représentation des pièces sous forme de bitboards.
        side_to_move: Couleur du joueur dont c'est le tour.
        castling_rights: Droits de roque encore disponibles.
        en_passant_square: Indice de la case pouvant être utilisée pour une
            capture en passant, ou None si aucune capture en passant n'est
            disponible.
        halfmove_clock: Nombre de demi-coups écoulés depuis le dernier
            déplacement de pion ou de la dernière capture.
        fullmove_number: Numéro du coup complet dans la partie.
    """

    piece_bitboards: PieceBitboards
    side_to_move: Color
    castling_rights: CastlingRights
    en_passant_square: int | None
    halfmove_clock: int
    fullmove_number: int


def parse_fen(fen: str) -> FENData:
    """Analyse une chaîne FEN et extrait les données de la position.

    Args:
        fen: Chaîne représentant une position au format FEN.

    Returns:
        Les données extraites de la chaîne FEN.

    Raises:
        ValueError: Si la chaîne FEN est invalide.
    """
    fen_infos: list[str] = fen.split()

    if len(fen_infos) != 6:
        raise ValueError("Une chaîne FEN doit contenir exactement six champs.")
    
    bitboards_info: PieceBitboards = fen_to_bitboards(fen_infos[0])
    side_to_move_info: Color = fen_to_color(fen_infos[1])
    castling_rights_info: CastlingRights = fen_to_castling_rights(fen_infos[2])
    en_passant_square_info: int | None = fen_to_en_passant_square(fen_infos[3])

    try:
        halfmove_clock_info: int = int(fen_infos[4])
        fullmove_number_info: int = int(fen_infos[5])

    except ValueError as error:
        raise ValueError("Les compteurs halfmove_clock_info et fullmove_number_info doivent être des entiers.") from error
    
    if halfmove_clock_info < 0:
        raise ValueError("Le compteur halfmove_clock ne peut pas être négatif.")
    
    if fullmove_number_info < 1:
        raise ValueError("Le compteur fullmove_number doit être supérieur à 0.")

    fen_data: FENData = FENData(bitboards_info, 
                                side_to_move_info, 
                                castling_rights_info, 
                                en_passant_square_info, 
                                halfmove_clock_info, 
                                fullmove_number_info)

    return fen_data

def fen_to_bitboards(string: str) -> PieceBitboards:
    """Convertit la partie positionnelle d'une FEN en bitboards.
    
    La partie positionnelle d'une FEN décrit les pièces rangée par rangée, 
    de la huitième à la première, et de la colonne a à la colonne h.
    
    La conversion respecte la convention de numérotation du moteur : 
    la case h8 correspond au bit 0 et la case a1 au bit 63.
    
    Args:
        string: Partie positionnelle de la FEN, composée de huit rangées séparées par le caractère '/'.
    
    Returns:
        Les bitboards correspondant aux pièces décrites dans la FEN.
        
    Raises:
        ValueError: Si la partie positionnelle de la FEN est invalide.
    """
    lines: list[str] = string.split('/')

    if len(lines) != BOARD_SIZE:
        raise ValueError("La partie positionnelle d'une FEN doit contenir huit rangées.")

    piece_bitboards: PieceBitboards = PieceBitboards((0, ) * 12)

    for rank_index, rank in enumerate(lines):
        file_index: int = 0

        for char in rank:
            if char in ''.join([str(i) for i in range(1, BOARD_SIZE + 1)]): # Crée la chaîne "1234..." jusqu'à BOARD_SIZE
                file_index += int(char)
                continue

            else:
                if file_index >= BOARD_SIZE:
                    raise ValueError("Une rangée FEN contient plus de huit cases.")
                
                color, piece_type = fen_to_piece(char)
                square: int = rank_index * BOARD_SIZE + (BOARD_SIZE - file_index - 1)

                piece_bitboards.add_piece(color, piece_type, square)

                file_index += 1

        if file_index != BOARD_SIZE:
            raise ValueError("Une rangée FEN doit représenter exactement huit cases.")

    return piece_bitboards

def fen_to_piece(char: str) -> tuple[Color, PieceType]:
    """Convertit un caractère FEN en couleur et type de pièce.
    
    Args:
        char: Caractère représentant une pièce dans une FEN.
        
    Returns:
        Un tuple contenant la couleur et le type de la pièce.
        
    Raises:
        ValueError: Si le caractère ne représente aucune pièce d'échecs.
    """
    match char:
        case 'K':
            return (Color.WHITE, PieceType.KING)
        case 'Q':
            return (Color.WHITE, PieceType.QUEEN)
        case 'R':
            return (Color.WHITE, PieceType.ROOK)
        case 'B':
            return (Color.WHITE, PieceType.BISHOP)
        case 'N':
            return (Color.WHITE, PieceType.KNIGHT)
        case 'P':
            return (Color.WHITE, PieceType.PAWN)
        case 'k':
            return (Color.BLACK, PieceType.KING)
        case 'q':
            return (Color.BLACK, PieceType.QUEEN)
        case 'r':
            return (Color.BLACK, PieceType.ROOK)
        case 'b':
            return (Color.BLACK, PieceType.BISHOP)
        case 'n':
            return (Color.BLACK, PieceType.KNIGHT)
        case 'p':
            return (Color.BLACK, PieceType.PAWN)

        case _:
            raise ValueError(f"fen_to_piece(string) '{char}' n'est pas un caractère reconnu.")

def fen_to_color(string: str) -> Color:
    """Convertit le champ de couleur d'une FEN en objet Color.
    
    Args:
        string: Caractère indiquant le joueur dont c'est le tour. 'w' pour les Blancs ou 'b' pour les Noirs.
    
    Returns:
        La couleur du joueur dont c'est le tour.
    
    Raises:
        ValueError: Si le caractère n'est ni 'w' ni 'b'.
    """
    if string == 'w':
        return Color.WHITE

    elif string == 'b':
        return Color.BLACK

    else:
        raise ValueError(f"fen_to_color(string) : '{string}' n'est pas une chaîne valide.")

def fen_to_castling_rights(string: str) -> CastlingRights:
    """Convertit le champ des droits de roque d'une FEN.
    
    Args:
        string: Champ FEN représentant les droits de roque. Le caractère '-' 
            indique qu'aucun droit de roque n'est disponible.
        
    Returns:
        Les droits de roque représentés par un CastlingRights.
        
    Raises:
        ValueError: Si le champ contient un caractère invalide ou un droit de roque en double.
    """
    if string == '-':
        return CastlingRights.NONE

    elif not 0 < len(string) <= 4:
        raise ValueError(f"fen_to_castling_rights(string) : string doit contenir 4 caractères maximum.")

    elif len(string) != len(set(string)):
        raise ValueError(f"fen_to_castling_rights(string) : string ne doit pas contenir 2 fois le même caractère.")

    else:
        castling_rights: CastlingRights = CastlingRights.NONE
        
        for char in string:
            match char:
                case 'K':
                    castling_rights |= CastlingRights.WHITE_KINGSIDE
                case 'Q':
                    castling_rights |= CastlingRights.WHITE_QUEENSIDE
                case 'k':
                    castling_rights |= CastlingRights.BLACK_KINGSIDE
                case 'q':
                    castling_rights |= CastlingRights.BLACK_QUEENSIDE

                case _:
                    raise ValueError(f"fen_to_castling_rights(string) : '{char}' n'est pas un caractère reconnu.")

        return castling_rights

def fen_to_en_passant_square(string: str) -> int | None:
    """Convertit le champ de prise en passant d'une FEN en indice de case.
    
    Args:
        string: Case de prise en passant au format algébrique, ou '-' si 
            aucune prise en passant n'est disponible.
    
    Returns:
        L'indice de la case selon la convention du moteur, ou None.
    
    Raises:
        ValueError: Si le champ ne représente pas une case valide.
    """
    if string == '-':
        return None

    elif re.search(f"^[{chr(ASCII_VALUE)}-{chr(ASCII_VALUE + BOARD_SIZE - 1)}][1-{BOARD_SIZE}]$", string):
        return (BOARD_SIZE - int(string[1])) * BOARD_SIZE + (BOARD_SIZE - (ord(string[0]) - ASCII_VALUE) - 1)

    else:
        raise ValueError(f"fen_to_en_passant_square(string) : '{string}' n'est pas une chaîne valide.")

def to_fen(position: Position) -> str:
    """Convertit une position en chaîne FEN.

    Args:
        position: Position à convertir.

    Returns:
        Chaîne FEN représentant la position.
    """
    bitboards_info: str = bitboards_to_fen(position.piece_bitboards)
    side_to_move_info: str = color_to_fen(position.side_to_move)
    castling_rights_info: str = castling_rights_to_fen(position.castling_rights)
    en_passant_square_info: str = en_passant_square_to_fen(position.en_passant_square)
    halfmove_clock_info: str = str(position.halfmove_clock)
    fullmove_number_info: str = str(position.fullmove_number)

    return f"{bitboards_info} {side_to_move_info} {castling_rights_info} {en_passant_square_info} {halfmove_clock_info} {fullmove_number_info}"

def bitboards_to_fen(piece_bitboards: PieceBitboards) -> str:
    """Convertit les bitboards des pièces en représentation FEN.

    Args:
        piece_bitboards: Bitboards représentant les pièces sur l'échiquier.

    Returns:
        Partie de la FEN représentant la position des pièces.
    """
    fen_bitboards: str = ""

    for rank_index in range(BOARD_SIZE):
        empty_square_counter: int = 0

        for file_index in range(BOARD_SIZE):
            square: int = rank_index * BOARD_SIZE + (BOARD_SIZE - file_index - 1)
            piece: tuple[Color, PieceType] | None = piece_bitboards.get_piece_at(square)

            if piece:
                if empty_square_counter != 0:
                    fen_bitboards += str(empty_square_counter)
                    empty_square_counter = 0

                color, piece_type = piece
                fen_bitboards += PIECE_TO_FEN[color.value * PIECE_TYPE_NUMBER + piece_type.value]

            else:
                empty_square_counter += 1

        if empty_square_counter != 0:
            fen_bitboards += str(empty_square_counter)

        if rank_index != BOARD_SIZE - 1:
            fen_bitboards += '/'

    return fen_bitboards

def color_to_fen(color: Color) -> str:
    """Convertit une couleur en notation FEN.

    Args:
        color: Couleur à convertir.

    Returns:
        Caractère FEN correspondant à la couleur.
    """
    if color is Color.WHITE:
        return 'w'

    return 'b'

def castling_rights_to_fen(castling_rights: CastlingRights) -> str:
    """Convertit les droits de roque en notation FEN.

    Args:
        castling_rights: Droits de roque disponibles.

    Returns:
        Chaîne FEN représentant les droits de roque.
    """
    if castling_rights is CastlingRights.NONE:
        return '-'

    else:
        fen_castling_rights: str = ""

        if castling_rights & CastlingRights.WHITE_KINGSIDE:
            fen_castling_rights += "K"
        if castling_rights & CastlingRights.WHITE_QUEENSIDE:
            fen_castling_rights += "Q"
        if castling_rights & CastlingRights.BLACK_KINGSIDE:
            fen_castling_rights += "k"
        if castling_rights & CastlingRights.BLACK_QUEENSIDE:
            fen_castling_rights += "q"

        return fen_castling_rights

def en_passant_square_to_fen(en_passant_square: int | None) -> str:
    """Convertit une case de prise en passant en notation FEN.

    Args:
        en_passant_square: Indice de la case, ou None si aucune case n'est disponible.

    Returns:
        Case en notation algébrique, ou « - » si aucune case n'est définie.
    """
    if en_passant_square is None:
        return '-'

    file: str = chr(ASCII_VALUE + BOARD_SIZE - 1 - en_passant_square % BOARD_SIZE)
    rank: str = str(BOARD_SIZE - en_passant_square // BOARD_SIZE)

    return file + rank