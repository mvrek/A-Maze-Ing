from mazegen.generator import MazeGenerator
from amazing.display import build_canvas

gen = MazeGenerator(15, 15, seed=3, entry=(0, 0), exit_pos=(2, 10))
gen.generate()
canvas = build_canvas(gen.grid, gen.entry, gen.exit_pos)
print("\n".join("".join(row) for row in canvas))