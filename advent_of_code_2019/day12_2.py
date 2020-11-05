"""
All this drifting around in space makes you wonder about the nature of the universe. Does history really repeat itself? You're curious whether the moons will ever return to a previous state.

Determine the number of steps that must occur before all of the moons' positions and velocities exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly match a previous point in time; it eventually returns to the initial state:

After 0 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

After 2770 steps:
pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>

After 2771 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>

After 2772 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

Of course, the universe might last for a very long time before repeating. Here's a copy of the second example from above:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>

This set of initial positions takes 4686774924 steps before it repeats a previous state! Clearly, you might need to find a more efficient way to simulate the universe.

How many steps does it take to reach the first state that exactly matches a previous state?
"""

from typing import NamedTuple, List
from dataclasses import dataclass
import copy
import math

@dataclass
class XYZ:
    x: int
    y: int
    z: int

    def energy(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

class Moon:
    def __init__(self, position: XYZ, velocity: XYZ = None) -> None:
        self.position = position
        self.velocity = velocity or XYZ(0, 0, 0)

    def __repr__(self) -> str:
        return f"Moon(position = {self.position}, velocity = {self.velocity})"

    def potential_energy(self) -> int:
        return self.position.energy()

    def kinetic_energy(self) -> int:
        return self.velocity.energy()

    def total_energy(self) -> int:
        return self.potential_energy() * self.kinetic_energy()

    def apply_velocity(self) -> None:
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z
    
    def sig_x(self):
        return (self.position.x, self.velocity.x)

    def sig_y(self):
        return (self.position.y, self.velocity.y)

    def sig_z(self):
        return (self.position.z, self.velocity.z)

def step(moons: List[Moon]) -> None:
    n = len(moons)
    for moon1 in moons:
        for moon2 in moons:
            if moon1 != moon2:
                if moon1.position.x < moon2.position.x:
                    moon1.velocity.x += 1
                elif moon1.position.x > moon2.position.x:
                    moon1.velocity.x -= 1

                if moon1.position.y < moon2.position.y:
                    moon1.velocity.y += 1
                elif moon1.position.y > moon2.position.y:
                    moon1.velocity.y -= 1

                if moon1.position.z < moon2.position.z:
                    moon1.velocity.z += 1
                elif moon1.position.z > moon2.position.z:
                    moon1.velocity.z -= 1
        
    for moon in moons:
        moon.apply_velocity()

MOONS = [
    Moon(XYZ(-1, 0, 2)),
    Moon(XYZ(2, -10, -7)),
    Moon(XYZ(4, -8, 8)),
    Moon(XYZ(3, 5, -1))
]

for n in range(10):
    print(n)
    for moon in MOONS:
        print(moon)
    step(MOONS)

moons = [
    Moon(XYZ(-13, -13, -13)),
    Moon(XYZ(5, -8, 3)),
    Moon(XYZ(-6, -10, -3)),
    Moon(XYZ(0, 5, -5))
]

def sig_x(moons: List[Moon]):
    return tuple(moon.sig_x() for moon in moons)

def sig_y(moons: List[Moon]):
    return tuple(moon.sig_y() for moon in moons)

def sig_z(moons: List[Moon]):
    return tuple(moon.sig_z() for moon in moons)

def steps_to_repeat(moons: List[Moon], sig_fn) -> int:
    moons = copy.deepcopy(moons)

    seen = set()
    seen.add(sig_fn(moons))

    num_steps = 0

    while True:
        num_steps += 1
        step(moons)
        sig = sig_fn(moons)
        if sig in seen:
            return num_steps
        else:
            seen.add(sig)

a = steps_to_repeat(moons, sig_x)
b = steps_to_repeat(moons, sig_y)
c = steps_to_repeat(moons, sig_z)

ab = a * b // math.gcd(a, b)
answer = ab * c // math.gcd(ab, c)

print(answer)
