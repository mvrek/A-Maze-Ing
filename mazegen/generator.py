from enum import IntFlag
import random

class Direction(IntFlag):

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        return _OPPOSITE[self]

    @property
    def step(self) -> tuple[int, int]:
        return _STEP[self]


class MazeGenerator:

    def __init__(self, width: int, height: int,
                 seed: int | None = None) -> None:
        self.width: int = width
        self.height: int = height
        self._rng = random.Random(seed)
        self.grid: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]

    def _in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y <= self.height

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        return self.grid[y][x] & direction

    def _open_wall(self, x: int, y: int, direction: Direction) -> None:
        dx, dy = direction.step
        nx, ny = x + dx, y + dy
        if not self._in_bounds(x, y) or not self._in_bounds(nx, ny):
            raise ValueError(
                f"({x}, {y}) verso {direction.name}: fuori dalla griglia!"
            )
        self.grid[y][x] &= ~direction.value
        self.grid[ny][nx] &= ~direction.opposite.value

_OPPOSITE: dict[Direction, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST
}

_STEP: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0)
}

ALL_WALLS: int = 0b1111
