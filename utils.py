import curses


def rectangle(win: curses.window, sub_win: curses.window) -> None:
    """Draw a rectangle around the sub_win."""
    offset_y, offset_x = sub_win.getbegyx()
    sub_win_height, sub_win_width = sub_win.getmaxyx()

    offset_y -= 1
    offset_x -= 1
    sub_win_height += 1
    sub_win_width += 1

    # Draw the top and bottom borders
    for x in range(sub_win_width):
        win.addch(offset_y, offset_x + x, curses.ACS_HLINE)
        win.addch(offset_y + sub_win_height, offset_x + x, curses.ACS_HLINE)

    # Draw the left and right borders
    for y in range(sub_win_height):
        win.addch(offset_y + y, offset_x, curses.ACS_VLINE)
        win.addch(offset_y + y, offset_x + sub_win_width, curses.ACS_VLINE)

    # Draw the corners
    win.addch(offset_y, offset_x, curses.ACS_ULCORNER)
    win.addch(offset_y, offset_x + sub_win_width, curses.ACS_URCORNER)
    win.addch(offset_y + sub_win_height, offset_x, curses.ACS_LLCORNER)
    win.addch(offset_y + sub_win_height, offset_x + sub_win_width, curses.ACS_LRCORNER)
