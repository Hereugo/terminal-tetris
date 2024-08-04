import curses
import random
import time
import logging

from utils import rectangle
from pieces import *


# For debugging purposes
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("tetris.log")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


SCORE_SYSTEM: list[int] = [40, 100, 300, 1200]


class Game:
    map: list[list[int]]
    nlines = 20
    ncols = 10
    speed = 60
    cur_piece: BasePiece
    pieces: list[BasePiece] = []
    num_next_pieces = 3
    force: bool = False

    score: int = 0
    level: float = 1
    lines: int = 0

    def __init__(self, stdscr: curses.window):
        if curses.has_colors():
            logger.info("Color detected")
            curses.use_default_colors()
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
            curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_CYAN)
            curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_GREEN)
            curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
            curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        else:
            logger.info("NO COLORS")

        self.map = [[0 for _ in range(self.ncols)] for _ in range(self.nlines)]

        self.cur_piece = self.get_random_piece(self.ncols / 2 - 2, 0)
        for _ in range(self.num_next_pieces):
            self.pieces.append(self.get_random_piece())

        self.win = curses.newwin(self.nlines, len(CELL_STR) * self.ncols + 2, 1, 1)
        self.win.keypad(True)
        self.win.nodelay(True)
        rectangle(stdscr, self.win)

        self.upnext_win = curses.newwin(
            4 * self.num_next_pieces,
            len(CELL_STR) * 4 + 2,
            1,
            self.win.getmaxyx()[1] + 3,
        )
        rectangle(stdscr, self.upnext_win)

        self.stats_win = curses.newwin(
            self.win.getmaxyx()[0] - self.upnext_win.getmaxyx()[0] - 2,
            self.upnext_win.getmaxyx()[1],
            self.upnext_win.getmaxyx()[0] + 3,
            self.win.getmaxyx()[1] + 3,
        )
        rectangle(stdscr, self.stats_win)

        stdscr.refresh()
        curses.curs_set(0)

    def get_random_piece(
        self, x: float | None = None, y: float | None = None
    ) -> BasePiece:
        return random.choice([OPiece, JPiece, SPiece, TPiece, ZPiece, IPiece, LPiece])(
            self,
            x,
            y,
        )

    def in_bounds(self, x: float, y: float) -> bool:
        return 0 <= int(x) < self.ncols and 0 <= int(y) < self.nlines

    def is_valid(self, x: float, y: float, shape: list[list[int]]) -> bool:
        # check if the piece collides with the map
        for row in range(len(shape)):
            for col in range(len(shape[row])):
                if not self.in_bounds(x + col, y + row):
                    if shape[row][col]:
                        return False
                elif self.map[int(y + row)][int(x + col)] and shape[row][col]:
                    return False
        return True

    def handle_input(self):
        ch = self.win.getch()

        if ch == curses.KEY_UP:  # UP / ROTATE
            self.cur_piece.rotate()
        elif ch == curses.KEY_LEFT:  # LEFT
            self.cur_piece.move(dx=-1)
        elif ch == curses.KEY_RIGHT:  # RIGHT
            self.cur_piece.move(dx=1)
        elif ch == curses.KEY_DOWN:  # DOWN / SOFT DROP
            self.cur_piece.move(dy=1)
        elif ch == 0x20:  # SPACEBAR / HARD DROP
            while self.cur_piece.move(dy=1):
                pass
            self.force = True

    def update(self, dt: float) -> None:
        # Move the piece down
        if not self.cur_piece.move(dy=dt):
            for row in range(len(self.cur_piece.shape)):
                for col in range(len(self.cur_piece.shape[row])):
                    if self.cur_piece.shape[row][col]:
                        if self.in_bounds(
                            self.cur_piece.x + col, self.cur_piece.y + row
                        ):
                            self.map[int(self.cur_piece.y + row)][
                                int(self.cur_piece.x + col)
                            ] = self.cur_piece.color

            self.cur_piece = self.pieces.pop(0)
            self.cur_piece.x = self.ncols / 2 - 2
            self.pieces.append(self.get_random_piece())

        # update map if contains full rows
        count = 0
        for row in range(len(self.map)):
            for col in range(len(self.map[row])):
                if self.map[row][col] == 0:
                    break
            else:
                self.map.pop(row)
                self.map.insert(0, [0 for _ in range(self.ncols)])
                count += 1

        if count > 0:
            self.score += SCORE_SYSTEM[count - 1]
            if int(self.level + count / 10) != int(self.level):
                self.speed += 10
            self.level += count / 10
            self.lines += count

    def render(self) -> None:

        # render main window
        self.win.clear()

        future_piece = self.cur_piece.copy()
        future_piece.no_color = True
        while future_piece.move(dy=1):
            pass
        future_piece.render(self.win)

        self.cur_piece.render(self.win)

        for row in range(self.nlines):
            for col in range(self.ncols):
                if self.map[row][col]:
                    self.win.addstr(
                        row,
                        col * len(CELL_STR) + 1,
                        CELL_STR,
                        curses.color_pair(self.map[row][col]),
                    )
        self.win.refresh()

        # render next pieces window
        self.upnext_win.clear()
        for i, piece in enumerate(self.pieces):
            piece.render(self.upnext_win, 0, i * 4)
        self.upnext_win.refresh()

        # render stats window
        self.stats_win.clear()
        self.stats_win.addstr(0, 1, "Score: {}".format(self.score))
        self.stats_win.addstr(2, 1, "Lines: {}".format(self.lines))
        self.stats_win.addstr(4, 1, "Level: {}".format(int(self.level)))
        self.stats_win.refresh()

    def run(self):
        before = time.time()
        while True:
            interval = 1 / self.speed
            now = time.time()
            dt = now - before
            if dt >= interval or self.force:
                self.force = False
                before = now

                self.handle_input()
                self.update(dt)
                self.render()


if __name__ == "__main__":
    curses.wrapper(lambda stdscr: Game(stdscr).run())
