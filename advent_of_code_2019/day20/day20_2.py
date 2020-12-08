"""
Strangely, the exit isn't open when you reach it. Then, you remember: the ancient Plutonians were famous for building recursive spaces.

The marked connections in the maze aren't portals: they physically connect to a larger or smaller copy of the maze. Specifically, the labeled tiles around the inside edge actually connect to a smaller copy of the same maze, and the smaller copy's inner labeled tiles connect to yet a smaller copy, and so on.

When you enter the maze, you are at the outermost level; when at the outermost level, only the outer labels AA and ZZ function (as the start and end, respectively); all other outer labeled tiles are effectively walls. At any other level, AA and ZZ count as walls, but the other outer labeled tiles bring you one level outward.

Your goal is to find a path through the maze that brings you back to ZZ at the outermost level of the maze.

In the first example above, the shortest path is now the loop around the right side. If the starting level is 0, then taking the previously-shortest path would pass through BC (to level 1), DE (to level 2), and FG (back to level 1). Because this is not the outermost level, ZZ is a wall, and the only option is to go back around to BC, which would only send you even deeper into the recursive maze.

In the second example above, there is no path that brings you to ZZ at the outermost level.

Here is a more interesting example:

             Z L X W       C                 
             Z P Q B       K                 
  ###########.#.#.#.#######.###############  
  #...#.......#.#.......#.#.......#.#.#...#  
  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  
  #.#...#.#.#...#.#.#...#...#...#.#.......#  
  #.###.#######.###.###.#.###.###.#.#######  
  #...#.......#.#...#...#.............#...#  
  #.#########.#######.#.#######.#######.###  
  #...#.#    F       R I       Z    #.#.#.#  
  #.###.#    D       E C       H    #.#.#.#  
  #.#...#                           #...#.#  
  #.###.#                           #.###.#  
  #.#....OA                       WB..#.#..ZH
  #.###.#                           #.#.#.#  
CJ......#                           #.....#  
  #######                           #######  
  #.#....CK                         #......IC
  #.###.#                           #.###.#  
  #.....#                           #...#.#  
  ###.###                           #.#.#.#  
XF....#.#                         RF..#.#.#  
  #####.#                           #######  
  #......CJ                       NM..#...#  
  ###.#.#                           #.###.#  
RE....#.#                           #......RF
  ###.###        X   X       L      #.#.#.#  
  #.....#        F   Q       P      #.#.#.#  
  ###.###########.###.#######.#########.###  
  #.....#...#.....#.......#...#.....#.#...#  
  #####.#.###.#######.#######.###.###.#.#.#  
  #.......#.......#.#.#.#.#...#...#...#.#.#  
  #####.###.#####.#.#.#.#.###.###.#.###.###  
  #.......#.....#.#...#...............#...#  
  #############.#.#.###.###################  
               A O F   N                     
               A A D   M                     

One shortest path through the maze is the following:

    Walk from AA to XF (16 steps)
    Recurse into level 1 through XF (1 step)
    Walk from XF to CK (10 steps)
    Recurse into level 2 through CK (1 step)
    Walk from CK to ZH (14 steps)
    Recurse into level 3 through ZH (1 step)
    Walk from ZH to WB (10 steps)
    Recurse into level 4 through WB (1 step)
    Walk from WB to IC (10 steps)
    Recurse into level 5 through IC (1 step)
    Walk from IC to RF (10 steps)
    Recurse into level 6 through RF (1 step)
    Walk from RF to NM (8 steps)
    Recurse into level 7 through NM (1 step)
    Walk from NM to LP (12 steps)
    Recurse into level 8 through LP (1 step)
    Walk from LP to FD (24 steps)
    Recurse into level 9 through FD (1 step)
    Walk from FD to XQ (8 steps)
    Recurse into level 10 through XQ (1 step)
    Walk from XQ to WB (4 steps)
    Return to level 9 through WB (1 step)
    Walk from WB to ZH (10 steps)
    Return to level 8 through ZH (1 step)
    Walk from ZH to CK (14 steps)
    Return to level 7 through CK (1 step)
    Walk from CK to XF (10 steps)
    Return to level 6 through XF (1 step)
    Walk from XF to OA (14 steps)
    Return to level 5 through OA (1 step)
    Walk from OA to CJ (8 steps)
    Return to level 4 through CJ (1 step)
    Walk from CJ to RE (8 steps)
    Return to level 3 through RE (1 step)
    Walk from RE to IC (4 steps)
    Recurse into level 4 through IC (1 step)
    Walk from IC to RF (10 steps)
    Recurse into level 5 through RF (1 step)
    Walk from RF to NM (8 steps)
    Recurse into level 6 through NM (1 step)
    Walk from NM to LP (12 steps)
    Recurse into level 7 through LP (1 step)
    Walk from LP to FD (24 steps)
    Recurse into level 8 through FD (1 step)
    Walk from FD to XQ (8 steps)
    Recurse into level 9 through XQ (1 step)
    Walk from XQ to WB (4 steps)
    Return to level 8 through WB (1 step)
    Walk from WB to ZH (10 steps)
    Return to level 7 through ZH (1 step)
    Walk from ZH to CK (14 steps)
    Return to level 6 through CK (1 step)
    Walk from CK to XF (10 steps)
    Return to level 5 through XF (1 step)
    Walk from XF to OA (14 steps)
    Return to level 4 through OA (1 step)
    Walk from OA to CJ (8 steps)
    Return to level 3 through CJ (1 step)
    Walk from CJ to RE (8 steps)
    Return to level 2 through RE (1 step)
    Walk from RE to XQ (14 steps)
    Return to level 1 through XQ (1 step)
    Walk from XQ to FD (8 steps)
    Return to level 0 through FD (1 step)
    Walk from FD to ZZ (18 steps)

This path takes a total of 396 steps to move from AA at the outermost layer to ZZ at the outermost layer.

In your maze, when accounting for recursion, how many steps does it take to get from the open tile marked AA to the open tile marked ZZ, both at the outermost layer?
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

    # handle start and end separately
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                # get direct neighbors
                for loc2 in neighbors(loc, deltas2):
                    if loc2 in portals['AA']:
                        start = loc
                    elif loc2 in portals['ZZ']:
                        end = loc

    inside_portal_neighbors = {}
    inside_neighbor_portals = {}
    outside_portal_neighbors = {}
    outside_neighbor_portals = {}
    
    # Find dots next to portals
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                outside = i == 2 or i == nr - 3 or j == 2 or j == nc - 3
                for loc2 in neighbors(loc, deltas2):                    
                    for portal, locs in portals.items():
                        if loc2 in locs:
                            if outside:
                                outside_neighbor_portals[loc] = portal
                                outside_portal_neighbors[portal] = loc
                            else:
                                inside_neighbor_portals[loc] = portal
                                inside_portal_neighbors[portal] = loc

    # each entry has a square and a change in level
    neighbor_dict = defaultdict(list)

    # Find neighbors
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '.':
                loc = XY(i, j)
                # get direct neighbors
                for loc2 in neighbors(loc, deltas2):
                    i2, j2 = loc2
                    c2 = lines[i2][j2]
                    if c2 == '.':
                        neighbor_dict[loc].append((loc2, 0))
                # get portal neighbors
                outside_portal = outside_neighbor_portals.get(loc)
                if outside_portal and outside_portal not in ['AA', 'ZZ']:
                    other_loc = inside_portal_neighbors[outside_portal]
                    neighbor_dict[loc].append((other_loc, -1))
                
                inside_portal = inside_neighbor_portals.get(loc)
                if inside_portal:
                    other_loc = outside_portal_neighbors[inside_portal]
                    neighbor_dict[loc].append((other_loc, +1))

    return Maze(start, end, neighbors = neighbor_dict)

def shortest_path(maze: Maze) -> int:
    visited = {(maze.start, 0)}

    q = deque([(maze.start, 0, 0)])

    while q:
        loc, level, num_steps = q.popleft()
            
        for nbor, level_delta in maze.neighbors[loc]:
            if nbor == maze.end and level == 0:
                return num_steps + 1
            
            new_level = level + level_delta

            if new_level >= 0 and (nbor, new_level) not in visited:
                visited.add((nbor, new_level))
                q.append((nbor, new_level, num_steps + 1))

with open('day20.txt') as f:
    raw = f.read()

maze = parse(raw)

print(shortest_path(maze))