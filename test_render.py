from amazing.canvas import Tile
from amazing.display import THEMES, render

W, F = Tile.WALL, Tile.FLOOR
canvas = [
    [W, W, W, W, W],
    [W, Tile.ENTRY, F, Tile.EXIT, W],
    [W, W, W, W, W],
]
print(repr(render([[W, F]], {W: 250, F: 16})))
print(render(canvas, THEMES[0]))