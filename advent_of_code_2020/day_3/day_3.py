from __future__ import annotations

from typing import List, NamedTuple, Tuple, Set

RAW = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

# Define each point as a tuple of ints
Point = Tuple[int, int]

# Create a class that contains the list of tree locations, the width and length of the slope
class Slope(NamedTuple):
    trees: Set[Point]
    width: int
    height: int

    # Create a static method that parses the data to define a slope
    @staticmethod
    def parse(raw: str) -> Slope:
        lines = raw.split("\n")
        trees = {(x, y)
                for y, row in enumerate(lines) # Enumerate the rows
                for x, c in enumerate(row.strip()) # Enumerate the columns
                if c == '#'} # If character is #, record the column and row
        width = len(lines[0])
        height = len(lines)

        return Slope(trees, width, height)

SLOPE = Slope.parse(RAW)

# Count the trees in the slope.
def count_trees(slope: Slope, right: int = 3, down: int = 1) -> int:
    num_trees = 0
    x = 0
    for y in range(0, slope.height, down): # For each row starting at (0, 0)
        if (x, y) in slope.trees:          # If that point is in the set of known trees
            num_trees += 1                 # Count that point
        x = (x + right) % slope.width      # Change the x value by the defined int
    return num_trees

assert count_trees(SLOPE) == 7

with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_3/input.txt') as f:
    raw = f.read()
slope = Slope.parse(raw)
print(count_trees(slope))

def trees_product(slope: Slope, slopes: List[Point]) -> int:
    product = 1
    for right, down in slopes:
        product *= count_trees(slope, right = right, down = down)

    return product

SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

assert trees_product(SLOPE, SLOPES) == 336

print(trees_product(slope, SLOPES))