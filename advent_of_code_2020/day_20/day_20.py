from __future__ import annotations

from typing import NamedTuple, List, Tuple, Iterator, Dict, Set, Optional
from collections import Counter
from functools import reduce
import operator
import math

Edge = str

class Edges(NamedTuple):
    top: Edge
    bottom: Edge
    left: Edge
    right: Edge
    
Pixels = List[List[str]]

class Tile(NamedTuple):
    tile_id: int
    pixels: Pixels
    
    def rotate(self, n: int) -> Tile:
        pixels = self.pixels
        for _ in range(n):
            rotated = []
            for c in range(len(pixels[0])):
                rotated.append([row[c] for row in reversed(pixels)])
            pixels = rotated
        return self._replace(pixels = pixels)
    
    def flip_horizontal(self, do: bool = False) -> Tile:
        pixels = [list(reversed(row)) for row in self.pixels] if do else self.pixels
        return self._replace(pixels = pixels)
    
    def flip_vertical(self, do: bool = False) -> Tile:
        pixels = list(reversed(self.pixels)) if do else self.pixels
        return self._replace(pixels = pixels)
    
    def all_rotations(self) -> Iterator[Tile]:
        for flip_h in [True, False]:
            for rot in [0, 1, 2, 3]:
                yield (self
                       .flip_horizontal(flip_h)
                       .rotate(rot)
                )
                
    def show(self) -> None:
        for row in self.pixels:
            print(''.join(row))
            
    @property
    def top(self) -> str:
        return ''.join(self.pixels[0])
    
    @property
    def bottom(self) -> str:
        return ''.join(self.pixels[-1])
    
    @property
    def left(self) -> str:
        return ''.join([row[0] for row in self.pixels])
    
    @property
    def right(self) -> str:
        return ''.join([row[-1] for row in self.pixels])
    
    def edges(self, reverse: bool = False) -> Edges:
        if reverse:
            return self.rotate(2).edges()
        return Edges(
            top = self.top, bottom = self.bottom, right = self.right, left = self.left
        )
        
    @staticmethod
    def parse(raw_tile: str) -> Tile:
        lines = raw_tile.split("\n")
        tile_id = int(lines[0].split()[-1][:-1])
        pixels = [list(line) for line in lines[1:]]
        return Tile(tile_id, pixels)

def make_tiles(raw: str) -> List[Tile]:
    tiles_raw = raw.split("\n\n")
    return [Tile.parse(tile_raw) for tile_raw in tiles_raw]

def find_corners(tiles: List[Tile]) -> List[Tile]:

    edge_counts = Counter(
        edge 
        for tile in tiles 
        for reverse in [True, False]
        for edge in tile.edges(reverse)
    )

    corners = []

    for tile in tiles:
        sides_with_no_matches = 0
        for edge in tile.edges():
            if edge_counts[edge] == 1 and edge_counts[edge[::-1]] == 1:
                sides_with_no_matches += 1

        if sides_with_no_matches == 2:
            for rot in [0, 1, 2, 3]:
                tile = tile.rotate(rot)
                edges = tile.edges()

                if edge_counts[edges.left] == 1 and edge_counts[edges.top] == 1:
                    corners.append(tile)
                    break

    return corners

Assembly = List[List[Optional[Tile]]] 

class Constraint(NamedTuple):
    i: int
    j: int
    top: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None
    right: Optional[str] = None

    def satisfied_by(self, tile: Tile) -> bool:
        if self.top and tile.top != self.top:
            return False
        if self.bottom and tile.bottom != self.bottom:
            return False
        if self.left and tile.left != self.left:
            return False
        if self.right and tile.right != self.right:
            return False
        return True
        
    @property
    def num_constraints(self) -> int:
        return (
            (self.top is not None) +
            (self.bottom is not None) + 
            (self.left is not None) + 
            (self.right is not None)
        )
        
def find_constraints(assembly: Assembly) -> Iterator[Constraint]:
    n = len(assembly)

    for i, row in enumerate(assembly):
        for j, tile in enumerate(row):
            # already have a tile here
            if assembly[i][j]:
                continue
            constraints: Dict[str, str] = {}
            if i > 0 and (nbr := assembly[i-1][j]):
                constraints["top"] = nbr.bottom
            if i < n-1 and (nbr := assembly[i+1][j]):
                constraints["bottom"] = nbr.top 
            if j > 0 and (nbr := assembly[i][j-1]):
                constraints["left"] = nbr.right
            if j < n-1 and (nbr := assembly[i][j+1]):
                constraints["right"] = nbr.left

            if constraints:
                yield Constraint(i, j, **constraints)
                
def assemble_image(tiles: List[Tile]) -> Assembly:
    """
    Take the tiles and figure out how to stick them together
    """
    num_tiles = len(tiles)
    side_length = int(math.sqrt(num_tiles))
    corners = find_corners(tiles)
    tile = corners[0]
    assembly: Assembly = [[None for _ in range(side_length)] for _ in range(side_length)]
    assembly[0][0] = tile
    placed: Dict[int, Tuple[int, int]] = {tile.tile_id: (0, 0)}
    while len(placed) < num_tiles:
        tiles = [t for t in tiles if t.tile_id not in placed]
        constraints = list(find_constraints(assembly))
        constraints.sort(key=lambda c: c.num_constraints, reverse=True)
        found_one = False
        for constraint in constraints:
            for tile in tiles:
                for rot in tile.all_rotations():
                    if constraint.satisfied_by(rot):
                        assembly[constraint.i][constraint.j] = rot 
                        placed[rot.tile_id] = (constraint.i, constraint.j)
                        found_one = True
                        break
                if found_one:
                    break
            if found_one:
                break

    return assembly

def glue(assembly: Assembly) -> Pixels:
    N = len(assembly)
    n = len(assembly[0][0].pixels)
    nout = (n - 2) * N
    glued = [['' for _ in range(nout)] for _ in range(nout)]
    for i, row in enumerate(assembly):
        for j, tile in enumerate(row):
            cropped = [line[1:-1] for line in tile.pixels[1:-1]]
            for ii, crow in enumerate(cropped):
                for jj, pixel in enumerate(crow):
                    glued[i * (n - 2) + ii][j * (n - 2) + jj] = pixel
                    
    return glued

SEA_MONSTER_RAW = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #  """
 
SEA_MONSTER = [
    (i, j) 
    for i, row in enumerate(SEA_MONSTER_RAW.split("\n"))
    for j, c in enumerate(row)
    if c == '#']

def find_sea_monsters(pixels: Pixels) -> Iterator[Tuple[int, int]]:
    for i, row in enumerate(pixels):
        for j, c in enumerate(row):
            try:
                if all(pixels[i + di][j + dj] == '#' for di, dj in SEA_MONSTER):
                    yield (i, j)
            except IndexError:
                continue
             
def roughness(glued: Pixels) -> int:
    tile = Tile(0, glued)
    finds = [(t, list(find_sea_monsters(t.pixels))) for t in tile.all_rotations()]
    finds = [(t, sm) for t, sm in finds if sm]
    assert len(finds) == 1
    t, sms = finds[0]
    sea_monster_pixels = {(i + di, j + dj)
                          for i, j in sms
                          for di, dj in SEA_MONSTER}
    return sum(c == '#' and (i, j) not in sea_monster_pixels
               for i, row in enumerate(t.pixels)
               for j, c in enumerate(row))
            
RAW = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

TILES = make_tiles(RAW)
CORNERS = find_corners(TILES)
CORNER_IDS = [tile.tile_id for tile in CORNERS]
assert reduce(operator.mul, CORNER_IDS, 1) == 20899048083289

IMAGES = assemble_image(TILES)
GLUED = glue(IMAGES)
assert roughness(GLUED) == 273

with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_20/input.txt') as f:
    raw = f.read()
    tiles = make_tiles(raw)
    corners = find_corners(tiles)
    corner_ids = [tile.tile_id for tile in corners]
    print(reduce(operator.mul, corner_ids, 1))
    images = assemble_image(tiles) 
    glued = glue(images)
    print(roughness(glued))