"""Canvas types shared by the maze display."""

from enum import Enum, auto


class Tile(Enum):
    """What a canvas position represents."""

    WALL = auto()
    FLOOR = auto()
    ENTRY = auto()
    EXIT = auto()
    PATH = auto()
    PATTERN = auto()


Canvas = list[list[Tile]]