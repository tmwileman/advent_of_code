from __future__ import annotations

from collections import Counter
from typing import List, Tuple, Set, Dict, Iterator

Hex = Tuple[float, float]

def parse(raw: str) -> List[str]:
    out = []
    while raw:
        if raw[:2] in ('nw', 'ne', 'sw', 'se'):
            out.append(raw[:2])
            raw = raw[2:]
        else:
            out.append(raw[0])
            raw = raw[1:]
    return out

def find_tile(steps: List[str]) -> Tuple[int, int]:
    x = y = 0
    for step in steps:
        if step == 'e':
            x += 1
        elif step == 'ne':
            x += 0.5
            y += 1
        elif step == 'nw':
            x -= 0.5
            y += 1
        elif step == 'w':
            x -= 1
        elif step == 'sw':
            x -= 0.5
            y -= 1
        elif step == 'se':
            x += 0.5
            y -= 1
            
    return x, y

def find_black_tiles(raw: str) -> Set[Hex]:
    counts: Dict[Hex, int] = Counter()
    
    for line in raw.split("\n"):
        steps = parse(line)
        x, y = find_tile(steps)
        counts[(x, y)] += 1
        
    return {k for k, v in counts.items() if v % 2 == 1}

def count_black_tiles(raw: str) -> int:
    return len(find_black_tiles(raw))

def neighbors(hex: Hex) -> Iterator[Hex]:
    x, y = hex
    yield x + 1, y
    yield x - 1, y
    yield x + 0.5, y + 1
    yield x - 0.5, y + 1
    yield x + 0.5, y - 1
    yield x - 0.5, y - 1

def step(black_tiles: Set[Hex]) -> Set[Hex]:
    neighbor_counts = Counter()
    for hex in black_tiles:
        for neighbor in neighbors(hex):
            neighbor_counts[neighbor] += 1
            
    return {
        hex
        for hex, count in neighbor_counts.items()
        if (hex in black_tiles and  1 <= count <= 2) or (hex not in black_tiles and count == 2)
    }

RAW = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

assert count_black_tiles(RAW) == 10

TILES = find_black_tiles(RAW)

for i in range(10):
    TILES = step(TILES)
    print(i, len(TILES))

with open ('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_24/input.txt') as f:
    raw = f.read()
    print(count_black_tiles(raw))
    tiles = find_black_tiles(raw)
    for i in range(100):
        tiles = step(tiles)
    print(len(tiles))