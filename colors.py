import curses


def main(stdscr: curses.window):
    # if not curses.has_extended_color_support():
    #     raise ValueError("No extended color support")
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(8, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    while True:
        for i in range(-1, 10):
            # stdscr.addstr(i + 1, 0, f"color: {i}")
            stdscr.addstr(i + 1, 0, f"color: {i}", curses.color_pair(i))
        stdscr.timeout(1000)
        stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(lambda stdscr: main(stdscr))
