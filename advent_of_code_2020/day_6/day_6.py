from typing import List
from collections import Counter

RAW = """
abc

a
b
c

ab
ac

a
a
a
a

b
"""

def count_yeses(raw:str) -> int:
    groups = raw.split("\n\n") # split groups by double space
    num_yeses = 0
    for group in groups:  # for each group
        yeses = {c for line in group.split("\n") for c in line.strip()}  # make a set for each group
        num_yeses += len(yeses) # count the length of each set
    return num_yeses

assert count_yeses(RAW) == 11

def count_yeses2(raw: str) -> int:
    groups = raw.split("\n\n")  # split groups by double space
    num_yeses = 0
    for group in groups:  # for each group
        people = group.split("\n")  # split each group 
        yeses = Counter(c for person in people for c in person) # count the times each character occurs for each person
        num_yeses += sum(count == len(people) for c, count in yeses.items()) # sum instances where the count of a character equals the number of people 
    return num_yeses

assert count_yeses2(RAW) == 6

with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_6/input.txt') as f:
    raw = f.read()
    print(count_yeses(raw))
    print(count_yeses2(raw))