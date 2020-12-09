from __future__ import annotations

from typing import NamedTuple

PASSWORDS = [
    "1-3 a: abcde",
    "1-3 b: cdefg",
    "2-9 c: ccccccccc"
]

# Create a class that can be used model each line of the input
class Password(NamedTuple):
    lo: int
    hi: int
    char: str
    password: str

    # Evaluates if the character appears >= lo and <= hi. Returns True or False (1 or 0).
    def is_valid(self) -> bool:
        return self.lo <= self.password.count(self.char) <= self.hi

    # Evaluates whether the character at the position in question matches the necessary character. Returns True or False (1 or 0).
    def is_valid2(self) -> bool:
        is_lo = self.password[self.lo - 1] == self.char
        is_hi = self.password[self.hi - 1] == self.char

        return is_lo != is_hi

    # Parses a line to identify the ints/chars needed for the class
    @staticmethod
    def from_line(line: str) -> Password:

        counts, char, password = line.strip().split()
        lo, hi = [int(n) for n in counts.split("-")]
        char = char[0]
        return Password(lo, hi, char, password)

with open("/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_2/input.txt") as f:
    passwords = [Password.from_line(line) for line in f]
    print(sum(pw.is_valid() for pw in passwords))
    print(sum(pw.is_valid2() for pw in passwords))
