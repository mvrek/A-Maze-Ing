# mazegen

Reusable maze generator: perfect mazes, Pac-Man boards with loops,
a "42" pattern of closed cells, and the shortest path.

## Basic usage

```python
from mazegen import MazeGenerator

gen = MazeGenerator(20, 15)
gen.generate()
print(gen.solution)
```

## Custom parameters

```python
gen = MazeGenerator(
    20, 15,               # width, height (cells)
    seed=42,              # same seed -> same maze
    entry=(0, 0),         # (x, y), default (0, 0)
    exit_pos=(19, 14),    # (x, y), default: bottom-right corner
    perfect=False,        # False -> Pac-Man board with loops
)
gen.generate()
```

Invalid parameters raise `ValueError`.

## Accessing the maze and a solution

- `gen.grid[y][x]`: walls of a cell as bits (N=1, E=2, S=4, W=8; 1 = closed)
- `gen.has_wall(x, y, Direction.NORTH)`: `True` if that wall is closed
- `gen.solution`: shortest path from entry to exit, e.g. `"EESENE..."`
- `gen.pattern`: cells `(x, y)` of the "42" (empty if the grid is too small)