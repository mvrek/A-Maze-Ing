from amazing.output import format_maze, write_output
from mazegen.generator import MazeGenerator

gen = MazeGenerator(20, 15, seed=42)
gen.generate()
print(all(gen.grid[y][x] == 15 for x, y in gen.pattern))
print(gen.solution)
text = format_maze(gen.grid, gen.entry, gen.exit_pos, gen.solution)
write_output(text, "maze_test.txt")

try:
    MazeGenerator(20, 15, entry=(6, 5))
except ValueError as err:
    print("ok:", err)
