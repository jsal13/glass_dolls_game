from attrs import define, field
import curses


@define
class Color:
    color_map: dict[str, int] = field(init=False)

    def __attrs_post_init__(self) -> None:
        self.init_colors()

    def init_colors(self) -> None:
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        self.color_map = {
            "WHITE": curses.color_pair(0),
            "RED": curses.color_pair(1),
            "YELLOW": curses.color_pair(2),
            "GREEN": curses.color_pair(3),
            "BLUE": curses.color_pair(4),
            "CYAN": curses.color_pair(5),
            "MAGENTA": curses.color_pair(6),
        }

    def __getitem__(self, color: str) -> int:
        color_int = self.color_map.get(color)
        if color_int is None:
            raise KeyError(
                f"No such color in color map: {color}.  Available colors: {list(self.color_map.keys())}"
            )
        return color_int

    def get_color_from_int(self, n: int) -> str:
        # This is lazy, but it works.
        for k, v in self.color_map.items():
            if v == n:
                return k

        raise KeyError(
            f"No such int assigned: {n}.  Possible values: {list(self.color_map.values())}"
        )
