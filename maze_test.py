from amazing.output import format_maze, write_output
from mazegen.generator import Direction, MazeGenerator

gen = MazeGenerator(10, 10, seed=42, entry=(5, 3))
genb= MazeGenerator(10, 10, seed=42)
genb.generate()
gen.generate()
text = format_maze(gen.grid, gen.entry, gen.exit_pos, gen._solve())
text2 = format_maze(genb.grid, genb.entry, genb.exit_pos, "EESWW")
write_output(text, "maze_test.txt")
write_output(text2, "maze_test2.txt")