"""Terminal rendering of the maze with ANSI colors."""

from amazing.canvas import Canvas, Tile, add_path, build_canvas
from mazegen import MazeGenerator
from collections.abc import Callable
import shutil

Theme = dict[Tile, int]

RESET = "\033[0m"

THEMES: list[Theme] = [
    {Tile.WALL: 153, Tile.FLOOR: 16, Tile.ENTRY: 46, Tile.EXIT: 196,
     Tile.PATH: 226, Tile.PATTERN: 244},
    {Tile.WALL: 204, Tile.FLOOR: 16, Tile.ENTRY: 46, Tile.EXIT: 21,
     Tile.PATH: 226, Tile.PATTERN: 244},
    {Tile.WALL: 183, Tile.FLOOR: 16, Tile.ENTRY: 46, Tile.EXIT: 196,
     Tile.PATH: 226, Tile.PATTERN: 244},
    {Tile.WALL: 185, Tile.FLOOR: 16, Tile.ENTRY: 46, Tile.EXIT: 196,
     Tile.PATH: 51, Tile.PATTERN: 244},
]


def _block(colour: int, width: int) -> str:
    """Return a block of 'width' characters with the given background color."""
    return f"\033[48;5;{colour}m" + " " * width


def render(canvas: Canvas, theme: Theme, tile_width: int = 2) -> str:
    """Turn a canvas into coloured text, two characters per tile."""
    lines: list[str] = []
    line: str = ""
    for row in canvas:
        line = "".join(_block(theme[tile], tile_width) for tile in row)
        lines.append(line + RESET)
    return "\n".join(lines)


def tile_width_for(canvas: Canvas) -> int:
    """Return 2 if the canvas fits the terminal with square tiles, else 1"""
    columns = shutil.get_terminal_size().columns
    if (len(canvas[0]) * 2) <= columns:
        return 2
    else:
        return 1


def too_wide(canvas: Canvas) -> bool:
    """Tell whether the canvas does not fit even with one char per tile."""
    return len(canvas[0]) > shutil.get_terminal_size().columns


CLEAR = "\033[2J\033[H"

MENU = (
    "=== Worms' A-Maze-Ing ===\n"
    "1. Re-generate a new maze\n"
    "2. Show / Hide the shortest path\n"
    "3. Rotate the wall colours\n"
    "4. Quit"
)


def run_display(gen: MazeGenerator,
                regenerate: Callable[[], MazeGenerator]) -> None:
    """Show the maze and handle the user's choices until Quit"""
    show_path = False
    theme_index = 0
    message = ""
    while True:
        canvas = build_canvas(gen.grid, gen.entry, gen.exit_pos,
                              gen.pattern)
        if show_path:
            add_path(canvas, gen.entry, gen.solution)
        width = tile_width_for(canvas)
        print(CLEAR + render(canvas, THEMES[theme_index], width))
        print(MENU)
        if too_wide(canvas):
            print("Warning: the terminal is too small, enlarge the window!")
        if message:
            print(message)
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        message = ""
        if choice == "1":
            try:
                gen = regenerate()
            except (ValueError, OSError) as error:
                message = f"Cannot regenerate: {error}"
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "4":
            return
        else:
            message = f"Invalid choice: {choice!r}"
