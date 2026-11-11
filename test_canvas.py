"""Print a canvas as letters, before and after drawing the path."""

from amazing.canvas import Tile, add_path, build_canvas
from mazegen.generator import MazeGenerator

SYMBOLS = {Tile.WALL: "#", Tile.FLOOR: " ", Tile.ENTRY: "S",
           Tile.EXIT: "E", Tile.PATH: ".", Tile.PATTERN: "4"}

gen = MazeGenerator(52, 27, seed=3, entry=(0, 0), exit_pos=(34, 14))
gen.generate()
canvas = build_canvas(gen.grid, gen.entry, gen.exit_pos, gen.pattern)
print("\n".join("".join(SYMBOLS[t] for t in row) for row in canvas))

add_path(canvas, gen.entry, gen.solution)
print("\n\n")
print("\n".join("".join(SYMBOLS[t] for t in row) for row in canvas))