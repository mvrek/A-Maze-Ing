from amazing.output import format_maze, write_output
from mazegen.generator import Direction, MazeGenerator

gen = MazeGenerator(25, 54)
gen._open_wall(0, 0, Direction.EAST)
gen._open_wall(13, 42, Direction.EAST)
gen._open_wall(2, 0, Direction.SOUTH)
gen._open_wall(2, 1, Direction.WEST)
gen._open_wall(1, 1, Direction.WEST)
text = format_maze(gen.grid, (0, 0), (0, 1), "EESWW")
write_output(text, "maze_test.txt")