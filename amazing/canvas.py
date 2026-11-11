"""Canvas types shared by the maze display."""

from enum import Enum, auto

from mazegen.generator import Direction


class Tile(Enum):
    """What a canvas position represents."""

    WALL = auto()
    FLOOR = auto()
    ENTRY = auto()
    EXIT = auto()
    PATH = auto()
    PATTERN = auto()


Canvas = list[list[Tile]]
Cell = tuple[int, int]


def build_canvas(grid: list[list[int]], entry: Cell, exit_pos: Cell,
                 pattern: set[Cell]) -> Canvas:
    """Build a tile canvas from a maze grid.

    Args:
        grid: wall bits for each cell, grid[y][x].
        entry: entry cell as (x, y).
        exit_pos: exit cell as (x, y).
        pattern: cells forming the "42" (may be empty).

    Returns:
        A canvas of (2*height + 1) x (2*width + 1) tiles.
    """
    height = len(grid)
    width = len(grid[0])
    canvas = [[Tile.WALL] * (2 * width + 1) for _ in range(2 * height + 1)]
    for y in range(height):
        for x in range(width):
            cx = 2 * x + 1
            cy = 2 * y + 1
            if (x, y) in pattern:
                canvas[cy][cx] = Tile.PATTERN
                continue
            canvas[cy][cx] = Tile.FLOOR
            for direction in Direction:
                if (grid[y][x] & direction) == 0:
                    dx, dy = direction.step
                    canvas[cy + dy][cx + dx] = Tile.FLOOR
    canvas[2 * entry[1] + 1][2 * entry[0] + 1] = Tile.ENTRY
    canvas[2 * exit_pos[1] + 1][2 * exit_pos[0] + 1] = Tile.EXIT
    return canvas


def add_path(canvas: Canvas, entry: Cell, solution: str) -> None:
    """Mark the solution path on the canvas, in place.

    Args:
        canvas: tile canvas built by build_canvas.
        entry: entry cell as (x, y).
        solution: moves made of the letters N, E, S, W.
    """
    letters = {d.letter: d for d in Direction}
    cx = 2 * entry[0] + 1
    cy = 2 * entry[1] + 1
    for letter in solution:
        dx, dy = letters[letter].step
        for _ in range(2):
            cy += dy
            cx += dx
            if canvas[cy][cx] is Tile.FLOOR:
                canvas[cy][cx] = Tile.PATH
