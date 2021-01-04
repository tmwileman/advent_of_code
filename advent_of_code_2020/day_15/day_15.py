from __future__ import annotations

from typing import List, Iterator, Dict
import itertools

def play_game(starting_numbers: List[int]) -> Iterator[int]:
    last_seen: Dict[int, int] = {}
    gap = None
    
    # For each starting number gap is difference between now and last time I saw it.
    for i, n in enumerate(starting_numbers):
        if n in last_seen:
            gap = i - last_seen[n]
        else:
            gap = None
        last_seen[n]  = i
        
        yield n
    
    # For each number if gap is present n is gap, else calculate gap.   
    for i in itertools.count(len(starting_numbers)):
        if gap:
            n = gap
        else:
            n = 0
        if n in last_seen:
            gap = i - last_seen[n]
        else:
            gap = None
        last_seen[n] = i
        
        yield n

def n2020(starting_numbers: List[int]) -> int:
    game = play_game(starting_numbers)
    for _ in range(2020):
        n = next(game)
    return n

def n30000000(starting_numbers: List[int]) -> int:
    game = play_game(starting_numbers)
    for i in range(30000000):
        n = next(game)
    return n
        
game = play_game([0, 3, 6])
output = [next(game) for _ in range(10)]
assert n2020([0, 3, 6]) == 436

numbers = [0,12,6,13,20,1,17]
print(n2020(numbers))
print(n30000000(numbers))