"""Format a maze as text and write it to the output file."""
def format_maze(grid: list[list[int]], entry: tuple[int, int],
                exit_pos: tuple[int, int], solution: str) -> str:
    """Returns the grid of the maze as a string, where the cells
    of the grid are converted in hexadecimal format. The string also
    contains coordinates related to the position of the entry cell
    and the exit cell.
    The last line of the string will contain the solution of the grid,
    meaning the letters related to every direction taken from
    entry point to exit point to exit the labyrinth in the shortest
    amount of moves possible."""
    lines: list[str] = []
    for row in grid:
        line = "".join(format(cell, "x") for cell in row)
        lines.append(line)
    lines.append("")
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit_pos[0]},{exit_pos[1]}")
    lines.append(solution)
    return "\n".join(lines) + "\n"


def write_output(output: str, path: str) -> None:
    """Write the string received in a new file.
    It is used to write the string returned by "format_maze"
    function in an output file."""
    with open(path, "w", encoding="utf-8") as file:
        file.write(output)
