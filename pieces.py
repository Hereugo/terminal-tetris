import curses
import logging

logger = logging.getLogger(__name__)
CELL_STR: str = "[x]"


class BasePiece:
    game: "Game"
    name: str
    shape: list[list[int]]
    no_color: bool = False
    color: int = 1
    x: float = 0
    y: float = 0

    def __init__(self, game, x: float | None = None, y: float | None = None):
        self.game = game
        self.x = x or self.x
        self.y = y or self.y

    def copy(self) -> "BasePiece":
        new = self.__class__(self.game, self.x, self.y)
        new.shape = self.shape
        new.color = self.color
        new.no_color = self.no_color
        return new

    def rotate(self) -> None:
        new_shape = list(zip(*self.shape[::-1]))
        if self.game.is_valid(self.x, self.y, new_shape):
            self.shape = new_shape

    def move(self, dx: float = 0, dy: float = 0) -> bool:
        if self.game.is_valid(self.x + dx, self.y + dy, self.shape):
            self.x += dx
            self.y += dy
            return True
        return False

    def render(
        self, win: curses.window, pos_x: float | None = None, pos_y: float | None = None
    ) -> None:
        pos_x = pos_x or self.x
        pos_y = pos_y or self.y
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.game.in_bounds(pos_x + col, pos_y + row):
                    if self.shape[row][col]:
                        logger.info(
                            f"Rendering piece {self.name} at {pos_x + col}, {pos_y + row}"
                        )
                        if self.no_color:
                            win.addstr(
                                int(pos_y + row),
                                len(CELL_STR) * (int(pos_x + col)) + 1,
                                CELL_STR,
                            )
                        else:
                            win.addstr(
                                int(pos_y + row),
                                len(CELL_STR) * (int(pos_x + col)) + 1,
                                CELL_STR,
                                curses.color_pair(self.color),
                            )


class OPiece(BasePiece):
    name: str = "square"
    color: int = 2
    shape: list[list[int]] = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]


class JPiece(BasePiece):
    name: str = "leftgun"
    color: int = 3
    shape: list[list[int]] = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]


class LPiece(BasePiece):
    name: str = "rightgun"
    color: int = 4
    shape: list[list[int]] = [
        [0, 1, 0, 0],
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]


class IPiece(BasePiece):
    name: str = "dash"
    color: int = 5
    shape: list[list[int]] = [
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]


class TPiece(BasePiece):
    name: str = "elbow"
    color: int = 6
    shape: list[list[int]] = [
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ]


class SPiece(BasePiece):
    name: str = "leftsnake"
    color: int = 7
    shape: list[list[int]] = [
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]


class ZPiece(BasePiece):
    name: str = "rightsnake"
    color: int = 8
    shape: list[list[int]] = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0],
    ]


# This import is placed here to avoid circular dependency issues.
from index import Game
