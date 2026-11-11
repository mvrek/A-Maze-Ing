*This project has been created as part of the 42 curriculum by lfoti, mde-matt.*

# A-Maze-ing

## Description

A-Maze-ing generates random mazes from a configuration file, writes them to a
text file in a hexadecimal format, and displays them in the terminal.

Main features:

- random but **reproducible** mazes (same seed, same maze);
- **perfect** mazes (exactly one path between any two cells) or
  **Pac-Man style** boards (full connectivity, loops, no dead ends where possible);
- a visible **"42"** drawn with fully closed cells;
- the **shortest path** from entry to exit, written to the output file and
  shown in the terminal on request;
- an interactive terminal display (ANSI colours);
- a reusable generator package, `mazegen`, installable with `pip`.

## Instructions

### Requirements

Python 3.10 or later.

### Installation and execution

```bash
make install        # create .venv and install flake8, mypy, build
make run            # run the program with config.txt
python3 a_maze_ing.py config.txt     # same, with any config file
```

Other Makefile rules:

| Rule | What it does |
|---|---|
| `make debug` | run the program under `pdb` |
| `make lint` | `flake8` and `mypy` with the required flags |
| `make lint-strict` | `flake8` and `mypy --strict` |
| `make clean` | remove `__pycache__`, `.mypy_cache`, build files |
| `make fclean` | `clean`, and remove `.venv` |

### Terminal menu

| Choice | Action |
|---|---|
| `1` | generate a new maze |
| `2` | show / hide the shortest path |
| `3` | rotate the wall colours |
| `4` | quit |

### Configuration file format

One `KEY=VALUE` pair per line. Lines starting with `#` and empty lines are
ignored.

| Key | Meaning | Example |
|---|---|---|
| `WIDTH` | number of cells per row (integer, at least 1) | `WIDTH=20` |
| `HEIGHT` | number of rows (integer, at least 1) | `HEIGHT=15` |
| `ENTRY` | entry cell `x,y` | `ENTRY=0,0` |
| `EXIT` | exit cell `x,y`, different from the entry | `EXIT=19,14` |
| `OUTPUT_FILE` | path of the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` or `False` (exactly this spelling) | `PERFECT=True` |
| `SEED` | optional integer; without it every run is different | `SEED=42` |

Coordinates are `(x, y)` with `(0, 0)` in the top-left corner. Entry and exit
must be inside the grid. Any error (missing file, missing key, bad value) is
reported on `stderr` with exit code 1; the program never crashes with a
traceback.

Default configuration (`config.txt`):

```
# default configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

If the grid is too small to contain the "42" (it needs at least 9 columns and
7 rows), the maze is generated without it and a message is printed on `stderr`.

### Output file format

One hexadecimal digit per cell, one row of the maze per line. Each digit
encodes the closed walls: bit 0 = North, bit 1 = East, bit 2 = South,
bit 3 = West (1 = wall closed). For example `3` = walls to the North and East,
`F` = fully closed (the cells of the "42").

After the grid come an empty line, then the entry `x,y`, the exit `x,y`, and
the shortest path as a string of `N`, `E`, `S`, `W`. Every line ends with `\n`.

## Algorithms

### Generation: iterative depth-first search (recursive backtracker)

Starting from the entry, the generator repeatedly moves to a random
unvisited neighbour, opening the wall between the two cells, and backtracks
when it has no unvisited neighbour left. The cells of the "42" are marked as
visited at the start, so they stay fully closed.

Why this algorithm:

- it visits every cell once and produces a spanning tree, so the maze is
  **perfect** by construction: connected, with no loops;
- it is simple to write, to explain and to test;
- it is **iterative** (an explicit stack), so large mazes do not hit Python's
  recursion limit;
- all randomness comes from a private `random.Random(seed)`, so the same seed
  always gives the same maze.

### Non-perfect mode (`PERFECT=False`)

The perfect maze is generated first, then modified:

1. **Dead ends are removed** by opening one more wall in each of them,
   preferring a wall shared with another dead end. A wall is never opened if it
   would create a 3x3 open area.
2. **Loops are guaranteed**: the number of independent loops is computed as
   `passages - cells + 1`; extra walls are opened until there are at least 2.
   If the grid is too small to hold them, a clear error is reported.

### Shortest path: breadth-first search

A BFS from the entry stores, for each cell, the cell it came from; following
these links back from the exit gives the shortest path, which is then
converted to `N`/`E`/`S`/`W` letters.

### Display

The maze is converted to a canvas of `(2 * height + 1) x (2 * width + 1)` tiles:
cell `(x, y)` is at canvas position `(2x + 1, 2y + 1)`, and the positions in
between are walls or passages. Each tile type (wall, floor, entry, exit, path,
"42") is then drawn as a coloured block with ANSI escape codes.

## Reusable code

The maze generator is a standalone package, `mazegen`, with no dependency on the
rest of the project. The built package is `mazegen-1.0.0-py3-none-any.whl` at the
root of the repository.

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

```python
from mazegen import MazeGenerator

gen = MazeGenerator(20, 15, seed=42, perfect=False)
gen.generate()
print(gen.grid[0][0])   # walls of the cell (0, 0) as bits
print(gen.solution)     # shortest path, e.g. "EESENE..."
```

To rebuild the package after changing `mazegen/`:

```bash
python3 -m build
```

Full instructions (custom parameters, accessing the structure and the
solution) are in [`mazegen/README.md`](mazegen/README.md).

Other parts that can be reused: `amazing/config.py` (a validated
`KEY=VALUE` parser returning a frozen dataclass) and `amazing/canvas.py` /
`amazing/display.py` (any grid of wall bits can be turned into a tile canvas and
displayed).

## Team and project management

### Roles

- **lfoti**: configuration parser (`amazing/config.py`), entry point
  (`a_maze_ing.py`), canvas building (`amazing/canvas.py`).
- **mde-matt**: maze generator (`mazegen/generator.py`) including the "42" and
  the non-perfect mode, output file (`amazing/output.py`), terminal rendering
  and menu (`amazing/display.py`), packaging.

### Planning

TODO (to be filled in by the team: the initial plan, how it evolved, and when
each part was finished).

### What worked well / what could be improved

TODO (to be filled in by the team).

### Tools

- Git and GitHub for collaboration;
- `flake8` and `mypy --strict` for code quality;
- `maze_analyzer.py` (provided with the subject) to check the output files.

## Resources

- Maze generation algorithms: Wikipedia, "Maze generation algorithm".
- Python documentation: `random`, `enum`, `dataclasses`, `collections`.
- PEP 8 and PEP 257 (style and docstrings).
- ANSI escape codes (Wikipedia, "ANSI escape code").

### Use of AI

An AI assistant (Claude) was used as a tutor during the project: to explain
concepts (iterative DFS, bit masks, `IntFlag`, dataclasses, exceptions), to
review code written by the team and point out bugs and style problems, and to
help draft this README. The code was written and tested by the team members,
who can explain it.