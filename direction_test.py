from mazegen.generator import Direction

for d in Direction:
    dx, dy = d.step
    ox, oy = d.opposite.step
    print(d.name, d.step, d.opposite.name, (dx + ox, dy + oy))
