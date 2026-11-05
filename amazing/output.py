def format_maze(grid: list[list[int]], entry: tuple[int, int],
                exit_pos: tuple[int, int], solution: str) -> str:
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
    with open(path, "w", encoding="utf-8") as file:
        file.write(output)
