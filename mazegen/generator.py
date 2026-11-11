"""Maze generator: grid, "42" pattern, perfect and Pac-Man modes."""

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
                 exit_pos: tuple[int, int] | None = None,
                 perfect: bool = True) -> None:
        """Initialize the maze, checking if every
        argument respect its limitations."""
        if width < 1 or height < 1:
            raise ValueError("Width and height values must be greater than 0!")
        self.width: int = width
        self.height: int = height
        self.perfect: bool = perfect
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
        if exit_pos in self.pattern:
            raise ValueError(f"Exit point {exit_pos} is inside"
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
        from the cell from the opposite direction in order to make the wall
        coherent."""
        dx, dy = direction.step
        nx, ny = x + dx, y + dy
        if not self._in_bounds(x, y) or not self._in_bounds(nx, ny):
            raise ValueError(f"({x}, {y})'s {direction.name} neighbour"
                             " is out of the grid!")
        self.grid[y][x] &= ~direction.value
        self.grid[ny][nx] &= ~direction.opposite.value

    def _close_wall(self, x: int, y: int, direction: Direction) -> None:
        """Close the wall of a cell in a given direction, then closes it
        from the cell from the opposite direction in order to make the
        wall coherent."""
        dx, dy = direction.step
        nx, ny = x + dx, y + dy
        if not self._in_bounds(x, y) or not self._in_bounds(nx, ny):
            raise ValueError(f"({x}, {y})'s {direction.name} neighbour"
                             " is out of the grid!")
        self.grid[y][x] |= direction.value
        self.grid[ny][nx] |= direction.opposite.value

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
        dig either a perfect labyrinth that connects every cell
        or a Pac-Man style grid with no or few dead ends (the labyrinth type
        is decided by the "perfect" parameter in the constructor).
        It then calculates the shortest path possible from entry to exit point.
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
        if not self.perfect:
            self._braid()
            self._ensure_loops(MIN_LOOPS)
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

    def _is_dead_end(self, x: int, y: int) -> bool:
        """Checks if the given cell is a dead end."""
        if (x, y) in self.pattern:
            return False
        open_sides: int = 0
        for direction in Direction:
            if not self.has_wall(x, y, direction):
                open_sides += 1
        return open_sides == 1

    def _is_open_block(self, left: int, top: int) -> bool:
        """Tell whether the 3x3 block at (left, top) has
        no inner walls."""
        if not (self._in_bounds(left, top)
                and self._in_bounds(left + 2, top + 2)):
            return False
        for cy in range(top, top + 3):
            for cx in range(left, left + 3):
                if not cx == left + 2:
                    if self.has_wall(cx, cy, Direction.EAST):
                        return False
                if not cy == top + 2:
                    if self.has_wall(cx, cy, Direction.SOUTH):
                        return False
        return True

    def _creates_open_3x3(self, x: int, y: int) -> bool:
        """Checks if the given cell is in a 3x3
        block with no inner walls"""
        for top in range(y - 2, y + 1):
            for left in range(x - 2, x + 1):
                if self._is_open_block(left, top):
                    return True
        return False

    def _braid(self) -> None:
        """Remove dead ends by opening one
        more wall in each of them, while avoiding to create
        3x3 open areas."""
        cells = [(x, y) for y in range(self.height)
                 for x in range(self.width)]
        self._rng.shuffle(cells)
        for x, y in cells:
            if not self._is_dead_end(x, y):
                continue
            preferred: list[Direction] = []
            others: list[Direction] = []
            for direction in Direction:
                dx, dy = direction.step
                nx, ny = x + dx, y + dy
                if (self.has_wall(x, y, direction) and
                        self._in_bounds(nx, ny) and
                        not (nx, ny) in self.pattern):
                    if self._is_dead_end(nx, ny):
                        preferred.append(direction)
                    else:
                        others.append(direction)
            self._rng.shuffle(preferred)
            self._rng.shuffle(others)
            for direction in preferred + others:
                self._open_wall(x, y, direction)
                if self._creates_open_3x3(x, y):
                    self._close_wall(x, y, direction)
                    continue
                break

    def _count_loops(self) -> int:
        """Counts the amount of loops possible
        in an imperfect grid. At least 2 loops are
        needed for the grid to be considered valid."""
        passages: int = 0
        for y in range(self.height):
            for x in range(self.width):
                if (self._in_bounds(x + 1, y) and
                        not self.has_wall(x, y, Direction.EAST)):
                    passages += 1
                if (self._in_bounds(x, y + 1) and
                        not self.has_wall(x, y, Direction.SOUTH)):
                    passages += 1
        cells: int = self.width * self.height - len(self.pattern)
        return passages - cells + 1

    def _ensure_loops(self, minimum: int) -> None:
        """Open extra walls until the grid has
        at least the minimum amount of loops required."""
        loops: int = self._count_loops()
        if loops >= minimum:
            return
        walls = [(x, y, d) for y in range(self.height)
                 for x in range(self.width)
                 for d in (Direction.EAST, Direction.SOUTH)]
        self._rng.shuffle(walls)
        for x, y, direction in walls:
            dx, dy = direction.step
            nx, ny = x + dx, y + dy
            if (not self._in_bounds(nx, ny) or
                    not self.has_wall(x, y, direction) or
                    (x, y) in self.pattern or
                    (nx, ny) in self.pattern):
                continue
            else:
                self._open_wall(x, y, direction)
                if self._creates_open_3x3(x, y):
                    self._close_wall(x, y, direction)
                    continue
                loops += 1
                if loops >= minimum:
                    return
        raise ValueError(
            f"{self.width} * {self.height} is too small for a"
            f" Pac-Man board. It cannot have {minimum} "
            "independent loops!"
        )


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

MIN_LOOPS: int = 2
