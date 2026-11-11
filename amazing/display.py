"""Terminal rendering of the maze with ANSI colors."""

from amazing.canvas import Canvas, Tile, build_canvas
from mazegen import MazeGenerator
from collections.abc import Callable

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

def _block(colour: int) -> str:
    """Return a two-character block with the given background color."""
    return f"\033[48;5;{colour}m  "

def render(canvas: Canvas, theme: Theme) -> str:
    """Turn a canvas into coloured text, two characters per tile."""
    lines: list[str] = []
    line: str = ""
    for row in canvas:
        line = "".join(_block(theme[tile]) for tile in row)
        lines.append(line + RESET)
    return "\n".join(lines)

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
        canvas = build_canvas(gen, show_path)
        print(CLEAR + render(canvas, THEMES[theme_index]))
        print(MENU)
        if message:
            print(message)
        try:
            choice = input("Choice? (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        message = ""
        if choice == "1":
            gen = regenerate()
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            theme_index = (theme_index + 1) % len(THEMES)
        elif choice == "4":
            return
        else:
            message = f"Invalid choice: {choice!r}"
