"""A-Maze-ing: maze generator entry point."""

import sys

from amazing.config import ConfigError, load_config
from amazing.output import format_maze, write_output
from mazegen.generator import MazeGenerator


def main(argv: list[str]) -> int:
    """Run the program and return the process exit code.

    Args:
        argv: command line arguments, without the program name.

    Returns:
        0 on success, 1 on error.
    """
    if len(argv) != 1:
        print("usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1
    try:
        config = load_config(argv[0])
    except ConfigError as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1
    try:
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            seed=config.seed,
            entry=config.entry,
            exit_pos=config.exit_pos,
            perfect=config.perfect
        )
        if not generator.pattern:
            print("Maze too small to display the 42 pattern",
                  file=sys.stderr)        
        generator.generate()
        text = format_maze(
            generator.grid, generator.entry,
            generator.exit_pos, generator.solution
        )
        write_output(text, config.output_file)
    except ValueError as e:
        print(f"Maze error: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"Cannot write output: {e}", file=sys.stderr)
        return 1
    print(f"Maze written to {config.output_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
