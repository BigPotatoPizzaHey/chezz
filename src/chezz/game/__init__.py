"""
Implementation of actual chess logic
"""

import dataclasses
import enum
import typing_extensions as t
from dataclasses import dataclass, field
from chezz.geo import V2


class PieceType(enum.Enum):
    KING = enum.auto()
    QUEEN = enum.auto()
    ROOK = enum.auto()
    BISHOP = enum.auto()
    KNIGHT = enum.auto()
    PAWN = enum.auto()


class Colour(enum.Enum):
    BLACK = enum.auto()
    WHITE = enum.auto()

    def is_black(self):
        return self == Colour.BLACK


_PIECE_SYMS: t.Final[dict[bool, dict[PieceType, str]]] = {
    False: {
        PieceType.KING: "♔ ",
        PieceType.QUEEN: "♕ ",
        PieceType.ROOK: "♖ ",
        PieceType.BISHOP: "♗ ",
        PieceType.KNIGHT: "♘ ",
        PieceType.PAWN: "♙ ",
    },
    True: {
        PieceType.KING: "♚ ",
        PieceType.QUEEN: "♛ ",
        PieceType.ROOK: "♜ ",
        PieceType.BISHOP: "♝ ",
        PieceType.KNIGHT: "♞ ",
        PieceType.PAWN: "♟ ",
    },
}


@dataclass
class Piece:
    type: PieceType
    colour: Colour

    def get_sym(self, full: bool):
        return _PIECE_SYMS[full][self.type]  # actual colouring will be done with ansi


@dataclass
class Move:
    start: V2
    end: V2
    piece: Piece
    promotion: t.Optional[Piece] = None

    is_en_passant: bool = False
    is_castling: bool = False


@dataclass
class State:
    """
    Holds the game state as a list of moves.
    """

    # fmt: off
    start: list[t.Optional[Piece]] = dataclasses.field(
        default_factory=lambda: [
            # r1
            Piece(PieceType.ROOK, Colour.BLACK),
            Piece(PieceType.KNIGHT, Colour.BLACK),
            Piece(PieceType.BISHOP, Colour.BLACK),
            Piece(PieceType.KING, Colour.BLACK),
            Piece(PieceType.QUEEN, Colour.BLACK),
            Piece(PieceType.BISHOP, Colour.BLACK),
            Piece(PieceType.KNIGHT, Colour.BLACK),
            Piece(PieceType.ROOK, Colour.BLACK),
            # r2
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            Piece(PieceType.PAWN, Colour.BLACK),
            # r3-6
            None, None, None, None, None, None, None, None, 
            None, None, None, None, None, None, None, None, 
            None, None, None, None, None, None, None, None, 
            None, None, None, None, None, None, None, None, 
            # r7
            Piece(PieceType.PAWN, Colour.WHITE),    
            Piece(PieceType.PAWN, Colour.WHITE),
            Piece(PieceType.PAWN, Colour.WHITE),
            Piece(PieceType.PAWN, Colour.WHITE),
            Piece(PieceType.PAWN, Colour.WHITE),
            Piece(PieceType.PAWN, Colour.WHITE),
            Piece(PieceType.PAWN, Colour.WHITE),
            Piece(PieceType.PAWN, Colour.WHITE),
            # r1
            Piece(PieceType.ROOK, Colour.WHITE),
            Piece(PieceType.KNIGHT, Colour.WHITE),
            Piece(PieceType.BISHOP, Colour.WHITE),
            Piece(PieceType.QUEEN, Colour.WHITE),
            Piece(PieceType.KING, Colour.WHITE),
            Piece(PieceType.BISHOP, Colour.WHITE),
            Piece(PieceType.KNIGHT, Colour.WHITE),
            Piece(PieceType.ROOK, Colour.WHITE),
        ]
    )

    moves: list[Move] = dataclasses.field(default_factory=list)
    selected: t.Optional[V2] = None
    accessible: list[V2] = field(default_factory=list)

    def get_positions(self) -> tuple[list[t.Optional[Piece]], dict[Colour, list[Piece]]]:
        board = self.start.copy()
        takes: dict[Colour, list[Piece]] = {
            Colour.BLACK: [],
            Colour.WHITE: []
        }
        for move in self.moves:
            if move.is_en_passant:
                raise NotImplementedError("no en passant")
            elif move.is_castling:
                raise NotImplementedError("no castling")
            elif move.promotion is not None:
                raise NotImplementedError("no promotion")
            piece = board[move.start.into_idx()]
            target = board[move.end.into_idx()]
            # print(f"{piece} takes {target}")
            board[move.start.into_idx()] = None
            board[move.end.into_idx()] = piece
        return board, takes

    def get_moves_for(self, board: list[t.Optional[Piece]], pos: V2):
        self.accessible.clear()
        piece = board[pos.into_idx()]
        if piece is None:
            return
        
        match piece.type:
            case PieceType.KNIGHT:
                vecs = (
                    V2(1, 2), V2(2, 1), V2(2, -1), V2(1, -2), 
                    V2(-1, -2), V2(-2, -1), V2(-2, 1), V2(-1, 2)
                )
                for vec in vecs:
                    new = pos + vec
                    if not new.is_valid():
                        continue
                    target = board[new.into_idx()]
                    if target and target.colour == piece.colour:
                        continue
                        
                    self.accessible.append(new)
            case PieceType.KING:
                vecs = (
                    V2(-1, 1), V2(0, 1), V2(1, 1), 
                    V2(-1, 0),           V2(1, 0),
                    V2(-1, -1),V2(0, -1),V2(1, -1)
                )
                for vec in vecs:
                    new = pos + vec
                    if not new.is_valid():
                        continue
                    target = board[new.into_idx()]
                    if target and target.colour == piece.colour:
                        continue
                        
                    self.accessible.append(new)
            case PieceType.PAWN:
                hasnt_moved = pos.y == 1 if piece.colour.is_black() else pos.y == 6
                sign = -1 + 2 * piece.colour.is_black()
                print(hasnt_moved, sign)

                new = pos + V2(0, sign)
                if new.is_valid() and not board[new.into_idx()]:
                    self.accessible.append(new)
                    # assuming that idx will always be valid because we are on y=1 or 6
                    if hasnt_moved and not board[(pos + V2(0, sign)).into_idx()]:
                        self.accessible.append(pos + V2(0, 2 * sign))
                # TODO: pawn capture, en passant

            case _:
                raise NotImplementedError(f"{piece.type} move logic not determined")

    def __str__(self) -> str:
        board = self.get_positions()[0]
        if self.selected:
            self.get_moves_for(board, self.selected)
        else:
            self.accessible.clear()
        ret = ""
        for i in range(0, len(board), 8):
            row = board[i:i + 8]
            ret += str(8 - i // 8) + " "
            for j, piece in enumerate(row):
                ret += self.make_sym(piece, V2.from_idx(i + j))
            ret += "\n"
        ret += "  a b c d e f g h"
        return ret

    def make_sym(self, piece: t.Optional[Piece], pos: V2) -> str:
        body = piece.get_sym(pos.is_black() ^ piece.colour.is_black()) if piece else "  "
        if self.selected and self.selected == pos:
            bg = "\033[41m"
        elif self.selected and pos in self.accessible:
            bg = "\033[43m"
        else:
            bg = "\033[40m" if pos.is_black() else "\033[47m"
        if piece:
            fg = "\033[37m" if pos.is_black() else "\033[30m"
        else:
            fg = ""

        return f"{fg}{bg}{body}\033[49m\033[39m"
