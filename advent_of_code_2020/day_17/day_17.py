from __future__ import annotations

from typing import Tuple, NamedTuple, Set
import itertools

class Point(NamedTuple):
    x: int
    y: int
    z: int
    
    def neighbors(self) -> Iterator[Point]:
        for dx, dy, dz in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            if dx != 0 or dy != 0 or dz != 0:
                yield Point(self.x + dx, self.y + dy, self.z + dz)
            
    
Grid = Set[Point]

def step(grid: Grid) -> Grid:
    new_candidates = {p for point in grid for p in point.neighbors() if p not in grid}
    
    new_grid = set()
    
    for point in grid:
        n = sum(p in grid for p in point.neighbors())
        if n in (2, 3):
            new_grid.add(point)
    
    for point in new_candidates:
        n = sum(p in grid for p in point.neighbors())
        if n == 3:
            new_grid.add(point)
    
    return new_grid

def make_grid(raw: str):
    lines = raw.split("\n")
    return {
        Point(x, y, 0)
        for y, row in enumerate(lines)
        for x, c in enumerate(row)
        if c == '#'
    }

RAW = """.#.
..#
###"""

GRID = make_grid(RAW)

for _ in range(6):
    GRID = step(GRID)
    
assert len(GRID) == 112

class Point4(NamedTuple):
    x: int
    y: int
    z: int
    w: int
    
    def neighbors(self) -> Iterator[Point4]:
        for dx, dy, dz, dw in itertools.product([-1, 0, 1], [-1, 0, 1], [-1, 0, 1], [-1, 0, 1]):
            if dx != 0 or dy != 0 or dz != 0 or dw != 0:
                yield Point4(self.x + dx, self.y + dy, self.z + dz, self.w + dw)

Grid4 = Set[Point4]

def step4(grid: Grid4) -> Grid4:
    new_candidates = {p for point in grid for p in point.neighbors() if p not in grid}
    
    new_grid = set()
    
    for point in grid:
        n = sum(p in grid for p in point.neighbors())
        if n in (2, 3):
            new_grid.add(point)
    
    for point in new_candidates:
        n = sum(p in grid for p in point.neighbors())
        if n == 3:
            new_grid.add(point)
    
    return new_grid

def make_grid4(raw: str):
    lines = raw.split("\n")
    return {
        Point4(x, y, 0, 0)
        for y, row in enumerate(lines)
        for x, c in enumerate(row)
        if c == '#'
    }

GRID4 = make_grid4(RAW)
for _ in range(6):
    GRID4 = step4(GRID4)

assert len(GRID4) == 848

with open("/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_17/input.txt") as f:
    raw = f.read()
    grid = make_grid(raw)
    for _ in range(6):
        grid = step(grid)
    print(len(grid))
    grid4 = make_grid4(raw)
    for _ in range(6):
        grid4 = step4(grid4)
    print(len(grid4))