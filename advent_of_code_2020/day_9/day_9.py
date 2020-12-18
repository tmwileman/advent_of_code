from __future__ import annotations

from collections import deque
from typing import List, Iterator

# Brute force. Create a que of the previous numbers defined by the lookback. View all the possible sum combinations. Find value not in possible combinations.
def not_sums(numbers: List[int], lookback: int = 25) -> Iterator[int]:
    q = deque()
    for n in numbers:
        if len(q) < lookback:
            q.append(n)
        else:
            sums = {a + b
                    for i, a in enumerate(q)
                    for j, b in enumerate(q)
                    if i < j}
            if n not in sums:
                yield n
            q.append(n)
            q.popleft()

# Brute force. Iterate over numbers. If sum is less than target add another number. If greater move on. If the target return that range of numbers.       
def range_with_sum(numbers: List[int], target: int) -> List[int]:
    for i, n in enumerate(numbers):
        j = i
        total = n
        while total < target:
            j += 1
            total += numbers[j]
        if total == target and i < j:
            slice = numbers[i: j + 1]
            assert sum(slice) == target
            return slice
    
    raise RuntimeError()

# Add the min and max of the range of numbers found in range_with_sums.
def encryption_weakness(numbers: List[int], lookback: int = 25) -> int:
    target = next(not_sums(numbers, lookback))
    slice = range_with_sum(numbers, target)
    return min(slice) + max(slice)

RAW = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

NUMBERS = [int(x) for x in RAW.split("\n")]

assert next(not_sums(NUMBERS, 5)) == 127

assert encryption_weakness(NUMBERS, 5) == 62

with open(f'/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_9/input.txt') as f:
    raw = f.read()
numbers = [int(x) for x in raw.split("\n")]
print(next(not_sums(numbers, 25)))
print(encryption_weakness(numbers))