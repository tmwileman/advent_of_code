"""
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

    It is a six-digit number.
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

    111111 meets these criteria (double 11, never decreases).
    223450 does not meet these criteria (decreasing pair of digits 50).
    123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 387638-919123.
"""

from typing import List
from collections import Counter

def digits(n: int, num_digits: int = 6) -> List[int]:
    d = []
    for _ in range (num_digits):
        d.append(n % 10)
        n = n // 10
    return list(reversed(d))

assert digits(123) == [0, 0, 0, 1, 2, 3]
assert digits(594383) == [5, 9, 4, 3, 8, 3]

def is_increasing(ds: List[int]) -> bool:
    return all(x <= y for x, y in zip(ds, ds[1:]))

def adjacent_same(ds: List[int]) -> bool:
    return any(x == y for x, y in zip(ds, ds[1:]))

def is_valid(n: int) -> bool:
    d = digits(n)
    return is_increasing(d) and adjacent_same(d)

assert is_valid(111111)
assert not is_valid(223450)
assert not is_valid(123789)

LO = 387638
HI = 919123

print(sum(is_valid(d) for d in range(LO, HI + 1)))

"""
An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

    112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

How many different passwords within the range given in your puzzle input meet all of the criteria?

Your puzzle input is still 387638-919123.
"""

def has_group_of_two(ds: List[int]) -> bool:
    counts = Counter(ds)
    return any(v == 2 for v in counts.values())

def is_valid2(n: int) -> bool:
    d = digits(n)
    return is_increasing(d) and has_group_of_two(d)

assert is_valid2(112233)
assert not is_valid2(123444)
assert is_valid2(111122)

print(sum(is_valid2(d) for d in range(LO, HI + 1)))