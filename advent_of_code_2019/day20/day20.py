"""
You notice a strange pattern on the surface of Pluto and land nearby to get a closer look. Upon closer inspection, you realize you've come across one of the famous space-warping mazes of the long-lost Pluto civilization!

Because there isn't much space on Pluto, the civilization that used to live here thrived by inventing a method for folding spacetime. Although the technology is no longer understood, mazes like this one provide a small glimpse into the daily life of an ancient Pluto citizen.

This maze is shaped like a donut. Portals along the inner and outer edge of the donut can instantly teleport you from one side to the other. For example:

         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       

This map of the maze shows solid walls (#) and open passages (.). Every maze on Pluto has a start (the open tile next to AA) and an end (the open tile next to ZZ). Mazes on Pluto also have portals; this maze has three pairs of portals: BC, DE, and FG. When on an open tile next to one of these labels, a single step can take you to the other tile with the same label. (You can only walk on . tiles; labels and empty space are not traversable.)

One path through the maze doesn't require any portals. Starting at AA, you could go down 1, right 8, down 12, left 4, and down 1 to reach ZZ, a total of 26 steps.

However, there is a shorter path: You could walk from AA to the inner BC portal (4 steps), warp to the outer BC portal (1 step), walk to the inner DE (6 steps), warp to the outer DE (1 step), walk to the outer FG (4 steps), warp to the inner FG (1 step), and finally walk to ZZ (6 steps). In total, this is only 23 steps.

Here is a larger example:

                   A               
                   A               
  #################.#############  
  #.#...#...................#.#.#  
  #.#.#.###.###.###.#########.#.#  
  #.#.#.......#...#.....#.#.#...#  
  #.#########.###.#####.#.#.###.#  
  #.............#.#.....#.......#  
  ###.###########.###.#####.#.#.#  
  #.....#        A   C    #.#.#.#  
  #######        S   P    #####.#  
  #.#...#                 #......VT
  #.#.#.#                 #.#####  
  #...#.#               YN....#.#  
  #.###.#                 #####.#  
DI....#.#                 #.....#  
  #####.#                 #.###.#  
ZZ......#               QG....#..AS
  ###.###                 #######  
JO..#.#.#                 #.....#  
  #.#.#.#                 ###.#.#  
  #...#..DI             BU....#..LF
  #####.#                 #.#####  
YN......#               VT..#....QG
  #.###.#                 #.###.#  
  #.#...#                 #.....#  
  ###.###    J L     J    #.#.###  
  #.....#    O F     P    #.#...#  
  #.###.#####.#.#####.#####.###.#  
  #...#.#.#...#.....#.....#.#...#  
  #.#####.###.###.#.#.#########.#  
  #...#.#.....#...#.#.#.#.....#.#  
  #.###.#####.###.###.#.#.#######  
  #.#.........#...#.............#  
  #########.###.###.#############  
           B   J   C               
           U   P   P               

Here, AA has no direct path to ZZ, but it does connect to AS and CP. By passing through AS, QG, BU, and JO, you can reach ZZ in 58 steps.

In your maze, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ?
"""

from typing import List, Dict, Set, Iterator, NamedTuple
from collections import defaultdict, deque

deltas1 = [(0, 1), (1, 0)]
deltas2 = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class XY(NamedTuple):
    x: int
    y: int

class Maze(NamedTuple):
    start: XY
    end: XY
    neighbors: Dict[XY, List[XY]]


def parse(raw: str) -> 'Maze':
    lines = raw.strip("\n").split("\n")
    nr = len(lines)
    nc = len(lines[0])
    
    def neighbors(loc: XY, deltas) -> Iterator[XY]:
        x, y = loc
        for dx, dy in deltas:
            neighbor = XY(x + dx, y + dy)
            if 0 <= neighbor.x < nr and 0 <= neighbor.y < nc:
                yield neighbor

    # Find all portals
    portals: Dict[str, List[XY]] = defaultdict(list)

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if 'A' <= c <= 'Z':
                for i2, j2 in neighbors(XY(i, j), deltas1):
                    c2 = lines[i2][j2]
                    if 'A' <= c2 <= 'Z':
                        portals[f"{c}{c2}"].extend([XY(i, j), XY(i2, j2)])

    portal_neighbors = defaultdict(list)
    neighbor_portals = defaultdict(list)

    # Find start and end
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                # get direct neighbors
                for loc in neighbors(XY(i, j), deltas2):
                    for portal, locs in portals.items():
                        if loc in locs:
                            portal_neighbors[portal].append(XY(i, j))
                            neighbor_portals[XY(i, j)].append(portal)

    neighbor_dict = defaultdict(list)

    # Find neighbors
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                for loc2 in neighbors(loc, deltas2):
                    i2, j2 = loc2
                    c2 = lines[i2][j2]
                    if c2 == '.':
                        neighbor_dict[loc].append(loc2)
                #get portal neighbors
                for portal in neighbor_portals.get(loc, []):
                    for nbor in portal_neighbors[portal]:
                        if nbor != loc:
                            neighbor_dict[loc].append(nbor)

    return Maze(start = portal_neighbors['AA'][0], 
    end = portal_neighbors['ZZ'][0],
    neighbors = neighbor_dict)

RAW = """         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z """

MAZE = parse(RAW)

def shortest_path(maze: Maze) -> int:
    visited = {maze.start}
    q = deque([(maze.start, 0)])

    while q:
        loc, num_steps = q.popleft()
            
        for nbor in maze.neighbors[loc]:
            if nbor == maze.end:
                return num_steps + 1
            if nbor not in visited:
                visited.add(nbor)
                q.append((nbor, num_steps + 1))

with open('day20.txt') as f:
    raw = f.read()

maze = parse(raw)

print(shortest_path(maze))