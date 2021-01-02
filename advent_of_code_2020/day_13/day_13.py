from __future__ import annotations

from functools import reduce
from typing import List

def earliest_bus(depart: int, buses: List[int]) -> int:
    # How much did I miss each bus by
    missed_by = [depart % bus for bus in buses]
    # What is the difference between the time each bus departs and how much I missed it by
    waits = {
        bus: bus - miss if miss > 0 else 0 
        for bus, miss in zip(buses, missed_by)
    }
    
    # Choose the minimum wait time.
    bus = min(buses, key = lambda bus: waits[bus])
    
    return bus * waits[bus]

RAW = """939
7,13,x,x,59,x,31,19"""

L1, L2 = RAW.split("\n")
DEPART = int(L1)
BUSES = [int(x) for x in L2.split(",") if x != "x"]

assert earliest_bus(DEPART, BUSES) == 295

def make_factors(raw_buses: List[str]):
    indexed = [(i, int(bus)) for i, bus in enumerate(raw_buses) if bus != 'x']
    
    factors = [(bus, (bus - i) % bus) for i, bus in indexed]
    
    return factors

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1
 
with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_13/input.txt') as f:
    depart = int(next(f))
    buses_raw = [x for x in next(f).split(",")]
    buses = [int(x) for x in buses_raw if x != "x"]

print(earliest_bus(depart, buses))
n, a = zip(*make_factors(buses_raw))
print(chinese_remainder(n, a))