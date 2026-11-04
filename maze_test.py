from amazing.output import format_maze, write_output
from mazegen.generator import Direction, MazeGenerator

gen = MazeGenerator(10, 10)
gen.generate()
text = format_maze(gen.grid, (0, 0), (0, 1), "EESWW")
write_output(text, "maze_test2.txt")