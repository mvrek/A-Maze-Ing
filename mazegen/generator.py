from enum import IntFlag
import random
from collections import deque


Cell = tuple[int, int]


class Direction(IntFlag):
    """A side of a cell. Its value is the wall bit."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        """Returns the opposite direction."""
        return _OPPOSITE[self]

    @property
    def step(self) -> tuple[int, int]:
        """Returns the grid coordinate variation
        needed to move to the
        cell in the given direction."""
        return _STEP[self]

    @property
    def letter(self) -> str:
        """Returns the letter related to the given direction
        used in the output path."""
        return _LETTER[self]


class MazeGenerator:

    """Class containing the every parameter and method related to the
    generation of the grid."""
    def __init__(self, width: int, height: int,
                 seed: int | None = None,
                 entry: tuple[int, int] = (0, 0),
                 exit_pos: tuple[int, int] | None = None) -> None:
        """Initialize the maze, checking if every
        argument respect its limitations."""
        if width < 1 or height < 1:
            raise ValueError("Width and height values must be greater than 0!")
        self.width: int = width
        self.height: int = height
        self._rng = random.Random(seed)
        self.grid: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]
        if exit_pos is None:
            exit_pos = (self.width - 1, self.height - 1)
        self.exit_pos = exit_pos
        self.entry = entry
        self.solution: str = ""
        self.pattern: set[Cell] = self._pattern_cells()
        if not self._in_bounds(entry[0], entry[1]):
            raise ValueError("Entry point"
                             " coordinates are out of the grid bounds!")
        if not self._in_bounds(exit_pos[0], exit_pos[1]):
            raise ValueError("Exit point"
                             " coordinates are out of the grid bounds!")
        if entry == exit_pos:
            raise ValueError("Exit and entry points"
                             " are placed at the same coordinates!")
        if entry in self.pattern:
            raise ValueError(f"Entry point {entry} is inside"
                             " the 42 pattern!")

    def _pattern_cells(self) -> set[Cell]:
        """Return the cells of the centered drawn 42"""
        pattern_w: int = len(_PATTERN_42[0])
        pattern_h: int = len(_PATTERN_42)
        if self.width < (pattern_w + 2) or self.height < (pattern_h + 2):
            return set()
        ox: int = (self.width - pattern_w) // 2
        oy: int = (self.height - pattern_h) // 2
        cells: set[Cell] = set()
        for row, line in enumerate(_PATTERN_42):
            for col, char in enumerate(line):
                if char == "X":
                    cells.add((ox + col, oy + row))
        return cells

    def _in_bounds(self, x: int, y: int) -> bool:
        """Checks if the given cell
        is in the grid bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def has_wall(self, x: int, y: int, direction: Direction) -> bool:
        """Checks if the given cell has
        a wall in a given direction."""
        return (self.grid[y][x] & direction) != 0

    def _open_wall(self, x: int, y: int, direction: Direction) -> None:
        """Opens the wall of a cell in a given direction, then opens it
        from the cell in the opposit direction in order to make the wall
        coherent."""
        dx, dy = direction.step
        nx, ny = x + dx, y + dy
        if not self._in_bounds(x, y) or not self._in_bounds(nx, ny):
            raise ValueError(f"({x}, {y}) verso {direction.name}:"
                             " fuori dalla griglia!")
        self.grid[y][x] &= ~direction.value
        self.grid[ny][nx] &= ~direction.opposite.value

    def _unvisited_neighbours(
            self, x: int, y: int, visited: set[tuple[int, int]]
    ) -> list[Direction]:
        """Returns a list of directions.
        Only directions that point (from the cell given) to unvisited
        cells by the generator are included in the list."""
        result: list[Direction] = []
        for direction in Direction:
            dx, dy = direction.step
            nx, ny = x + dx, y + dy
            if self._in_bounds(nx, ny) and (nx, ny) not in visited:
                result.append(direction)
        return result

    def generate(self) -> None:
        """Generate a random grid (using the random seed if given), then
        dig a perfect labyrinth that connects every cell.
        It never returns in already visited cells."""
        self.grid = [[ALL_WALLS] * self.width for _ in range(self.height)]
        start = self.entry
        visited: set[tuple[int, int]] = {start} | self.pattern
        stack: list[tuple[int, int]] = [start]
        while stack:
            x, y = stack[-1]
            options = self._unvisited_neighbours(x, y, visited)
            if not options:
                stack.pop()
            else:
                walker = self._rng.choice(options)
                self._open_wall(x, y, walker)
                dx, dy = walker.step
                nx, ny = x + dx, y + dy
                visited.add((nx, ny))
                stack.append((nx, ny))
        self.solution = self._solve()

    def _solve(self) -> str:
        """Using queue, the method finds the most efficent way to
        solve the grid, finding the shortest path possible between
        entry point and exit point"""
        came_from: dict[Cell, tuple[Cell, Direction]] = {}
        visited: set[Cell] = {self.entry}
        queue: deque[Cell] = deque([self.entry])
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit_pos:
                break
            for direction in Direction:
                if self.has_wall(x, y, direction):
                    continue
                dx, dy = direction.step
                neighbour: Cell = (x + dx, y + dy)
                if neighbour in visited:
                    continue
                visited.add(neighbour)
                came_from[neighbour] = ((x, y), direction)
                queue.append(neighbour)
        if self.exit_pos not in visited:
            raise ValueError("Exit unreachable from entry!")
        letters: list[str] = []
        cell = self.exit_pos
        while cell != self.entry:
            previous, direction = came_from[cell]
            letters.append(direction.letter)
            cell = previous
        letters.reverse()
        return "".join(letters)


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

_LETTER: dict[Direction, str] = {
    Direction.NORTH: "N",
    Direction.EAST: "E",
    Direction.SOUTH: "S",
    Direction.WEST: "W"
}

_PATTERN_42: list[str] = [
    "X.X.XXX",
    "X.X...X",
    "XXX.XXX",
    "..X.X..",
    "..X.XXX",
]
