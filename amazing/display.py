"""ASCII rendering of a maze."""

from mazegen.generator import Direction

WALL = "#"
FLOOR = " "


def build_canvas(grid: list[list[int]], entry: tuple[int, int],
                 exit_pos: tuple[int, int]) -> list[list[str]]:
    """Build a character canvas from a maze grid.

    Args:
        grid: wall bits for each cell, grid[y][x].
        entry: entry cell as (x, y).
        exit_pos: exit cell as (x, y).

    Returns:
        A canvas of (2*height + 1) x (2*width + 1) characters.
    """
    height = len(grid)
    width = len(grid[0])
    canvas = [[WALL] * (2 * width + 1) for _ in range (2 * height + 1)]
    for y in range(height):
        for x in range(width):
            cx = 2 * x + 1
            cy = 2 * y + 1
            canvas[cy][cx] = FLOOR
            for direction in Direction:
                if (grid[y][x] & direction) == 0:
                    dx, dy = direction.step
                    canvas[cy + dy][cx + dx] = FLOOR
    canvas[2 * entry[1] + 1][2 * entry[0] + 1] = "S"
    canvas[2 * exit_pos[1] + 1][2 * exit_pos[0] + 1] = "E"
    return canvas