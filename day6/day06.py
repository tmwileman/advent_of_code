"""
If we build a tree, each thing orbits its ancestors.
We need to count the total number of ancestors.
"""

raw = """ COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""

from typing import NamedTuple, List, Dict
from collections import defaultdict

class Orbit(NamedTuple):
    parent: str
    child: str

    @staticmethod
    def from_string(s: str) -> 'Orbit':
        parent, child = s.strip().split(")")
        return Orbit(parent, child)

ORBITS = [Orbit.from_string(s) for s in raw.strip().split("\n")]

def make_tree(orbits: List[Orbit]):
    parents = {}
    for parent, child in orbits:
        parents[child] = parent
    return parents

def count_ancestors(child: str, parents: Dict[str, str]) -> int:
    count = 0
    while child != "COM":
        count += 1
        child = parents[child]
    return count

PARENTS = make_tree(ORBITS)

assert count_ancestors('D', PARENTS) == 3
assert count_ancestors('L', PARENTS) == 7
assert count_ancestors('COM', PARENTS) == 0

def total_ancestors(orbits: List[Orbit]) -> int:
    parents = make_tree(orbits)

    return sum(count_ancestors(child, parents) for child in parents)

assert total_ancestors(ORBITS) == 42

with open('day_6_input.txt') as f:
    orbits = [Orbit.from_string(line) for line in f]

print(total_ancestors(orbits))

"""
Now, you just need to figure out how many orbital transfers you (YOU) need to take to get to Santa (SAN).

You start at the object YOU are orbiting; your destination is the object SAN is orbiting. An orbital transfer lets you move from any object to an object orbiting or orbited by that object.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN

Visually, the above map of orbits looks like this:

                          YOU
                         /
        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN

In this example, YOU are in orbit around K, and SAN is in orbit around I. To move from K to I, a minimum of 4 orbital transfers are required:

    K to J
    J to E
    E to D
    D to I

Afterward, the map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I - SAN
                 \
                  YOU

What is the minimum number of orbital transfers required to move from the object YOU are orbiting to the object SAN is orbiting? (Between the objects they are orbiting - not between YOU and SAN.)
"""

def path_to_com(child: str, parents: Dict[str, str]) -> List[str]:
    path = [child]
    while child != "COM":
        child = parents[child]
        path.append(child)

    return path

assert path_to_com("I", PARENTS) == ['I', 'D', 'C', 'B', 'COM']

def shortest_path(child1: str, child2: str, parents: Dict[str, str]) -> int:
    path1 = path_to_com(child1, parents)
    path2 = path_to_com(child2, parents)

    # J, E, D, B, C, COM
    # I, D, E, B, C, COM

    while path1 and path2 and path1[-1] == path2[-1]:
        path1.pop()
        path2.pop()

    return len(path1) + len(path2)

assert shortest_path('I', 'K', PARENTS) == 4
assert shortest_path('H', 'F', PARENTS) == 6

parents = make_tree(orbits)
print(shortest_path(parents['YOU'], parents['SAN'], parents))