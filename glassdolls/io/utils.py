import curses


def get_color_map() -> dict[str, int]:
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    return {
        "WHITE": curses.color_pair(0),
        "RED": curses.color_pair(1),
        "YELLOW": curses.color_pair(2),
        "GREEN": curses.color_pair(3),
        "BLUE": curses.color_pair(4),
        "CYAN": curses.color_pair(5),
        "MAGENTA": curses.color_pair(6),
    }
