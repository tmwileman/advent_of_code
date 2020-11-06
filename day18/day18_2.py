"""
You arrive at the vault only to discover that there is not one vault, but four - each with its own entrance.

On your map, find the area in the middle that looks like this:

...
.@.
...

Update your map to instead use the correct data:

@#@
###
@#@

This change will split your map into four separate sections, each with its own entrance:

#######       #######
#a.#Cd#       #a.#Cd#
##...##       ##@#@##
##.@.##  -->  #######
##...##       ##@#@##
#cB#Ab#       #cB#Ab#
#######       #######

Because some of the keys are for doors in other vaults, it would take much too long to collect all of the keys by yourself. Instead, you deploy four remote-controlled robots. Each starts at one of the entrances (@).

Your goal is still to collect all of the keys in the fewest steps, but now, each robot has its own position and can move independently. You can only remotely control a single robot at a time. Collecting a key instantly unlocks any corresponding doors, regardless of the vault in which the key or door is found.

For example, in the map above, the top-left robot first collects key a, unlocking door A in the bottom-right vault:

#######
#@.#Cd#
##.#@##
#######
##@#@##
#cB#.b#
#######

Then, the bottom-right robot collects key b, unlocking door B in the bottom-left vault:

#######
#@.#Cd#
##.#@##
#######
##@#.##
#c.#.@#
#######

Then, the bottom-left robot collects key c:

#######
#@.#.d#
##.#@##
#######
##.#.##
#@.#.@#
#######

Finally, the top-right robot collects key d:

#######
#@.#.@#
##.#.##
#######
##.#.##
#@.#.@#
#######

In this example, it only took 8 steps to collect all of the keys.

Sometimes, multiple robots might have keys available, or a robot might have to wait for multiple keys to be collected:

###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############

First, the top-right, bottom-left, and bottom-right robots take turns collecting keys a, b, and c, a total of 6 + 6 + 6 = 18 steps. Then, the top-left robot can access key d, spending another 6 steps; collecting all of the keys here takes a minimum of 24 steps.

Here's a more complex example:

#############
#DcBa.#.GhKl#
#.###@#@#I###
#e#d#####j#k#
###C#@#@###J#
#fEbA.#.FgHi#
#############

    Top-left robot collects key a.
    Bottom-left robot collects key b.
    Top-left robot collects key c.
    Bottom-left robot collects key d.
    Top-left robot collects key e.
    Bottom-left robot collects key f.
    Bottom-right robot collects key g.
    Top-right robot collects key h.
    Bottom-right robot collects key i.
    Top-right robot collects key j.
    Bottom-right robot collects key k.
    Top-right robot collects key l.

In the above example, the fewest steps to collect all of the keys is 32.

Here's an example with more choices:

#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############

One solution with the fewest steps is:

    Top-left robot collects key e.
    Top-right robot collects key h.
    Bottom-right robot collects key i.
    Top-left robot collects key a.
    Top-left robot collects key b.
    Top-right robot collects key c.
    Top-left robot collects key d.
    Top-left robot collects key f.
    Top-left robot collects key g.
    Bottom-right robot collects key k.
    Bottom-right robot collects key j.
    Top-right robot collects key l.
    Bottom-left robot collects key n.
    Bottom-left robot collects key m.
    Bottom-left robot collects key o.

This example requires at least 72 steps to collect all keys.

After updating your map and using the remote-controlled robots, what is the fewest steps necessary to collect all of the keys?
"""

from typing import List, NamedTuple, Dict, Set, Tuple
from collections import deque
import heapq

class XY(NamedTuple):
    x: int
    y: int


class Grid(NamedTuple):
    walls: Set[XY]
    keys: Dict[XY, str]
    doors: Dict[XY, str]
    starts: List[XY]

    @staticmethod
    def parse(raw: str) -> 'Grid':
        walls = set()
        keys = {}
        doors = {}
        starts = []

        lines = raw.strip().split("\n")

        for i, line in enumerate(lines):
            for j, c in enumerate(line):
                loc = XY(i, j)
                if c == '#':
                    walls.add(loc)
                elif c == '@':
                    starts.append(loc)
                elif 'a' <= c <= 'z':
                    keys[loc] = c
                elif 'A' <= c <= 'Z':
                    doors[loc] = c

        return Grid(walls, keys, doors, starts)

deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def one_source_shortest_path(grid: Grid, start: XY):
    # key is key_name, value is pair (distance, doors_passed_through)
    results = {}
    visited = {start}

    frontier = deque([(0, start, [])])

    while frontier:
        num_steps, (x, y), doors = frontier.popleft()
        for dx, dy in deltas:
            new_pos = XY(x + dx, y + dy)
            
            if new_pos in visited or new_pos in grid.walls:
                continue

            visited.add(new_pos)

            if new_pos in grid.keys:
                key = grid.keys[new_pos]
                results[key] = (num_steps + 1, doors)
                frontier.append((num_steps + 1, new_pos, doors))
            elif new_pos in grid.doors:
                new_doors = doors + [grid.doors[new_pos]]
                frontier.append((num_steps + 1, new_pos, new_doors))
            else:
                frontier.append((num_steps + 1, new_pos, doors))

    return results


def all_source_shortest_path(grid: Grid):
    results = {}

    for i, start in enumerate(grid.starts):
        results[str(i)] = one_source_shortest_path(grid, start)
    for key_loc, key in grid.keys.items():
        results[key] = one_source_shortest_path(grid, key_loc)

    return results



RAW = """#########
#b.A.@.a#
#########"""

GRID = Grid.parse(RAW)

GRID2 = Grid.parse("""#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""")

GRID3 = Grid.parse("""########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################""")

def signature(prev_keys: Set[str], curr_locs: List[str]) -> str:
    loc = ''.join(curr_locs)
    return f"{loc}:{''.join(sorted(prev_keys))}"

def shortest_path(grid: Grid) -> int:
    assp = all_source_shortest_path(grid)
    seen_signatures = set()

    num_keys = len(grid.keys)
    # maintain priority queue of num_steps, key at, keys had
    pq = [(0, ['0', '1', '2', '3'], set())]

    while pq:
        num_steps, source_keys, keys_had = heapq.heappop(pq)
        sig = signature(keys_had, source_keys)
        if sig in seen_signatures:
            continue
        seen_signatures.add(sig)

        print(num_steps, source_keys, keys_had)

        if len(keys_had) == num_keys:
            return num_steps

        for i, source_key in enumerate(source_keys):
            ossp = assp[source_key]
            for dest_key, (steps_to_key, doors) in ossp.items():
                if dest_key in keys_had:
                    continue
                if any(door.lower() not in keys_had for door in doors):
                    continue

                new_source_keys = source_keys[:]
                new_source_keys[i] = dest_key

                new_keys = keys_had | {dest_key}
                heapq.heappush(pq, (num_steps + steps_to_key, new_source_keys, new_keys))


GRID = Grid.parse("""###############
#d.ABC.#.....a#
######@#@######
###############
######@#@######
#b.....#.....c#
###############""")

GRID2 = Grid.parse("""#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba@#@BcIJ#
#############
#nK.L@#@G...#
#M###N#H###.#
#o#m..#i#jk.#
#############""")




with open('day_18_2_input.txt') as f:
    grid = Grid.parse(f.read())

print(shortest_path(grid))