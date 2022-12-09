import numpy as np
from typing import List

class Section:
    def __init__(self, lower1: int, upper1: int, lower2: int, upper2: int, wholly_contained: int, overlap: int):
        self.lower1 = lower1
        self.upper1 = upper1
        self.lower2 = lower2
        self.upper2 = upper2
        self.wholly_contained = wholly_contained
        self.overlap = overlap

    @staticmethod
    def parse(s: str) -> 'Section':
        range1 = s.split(",")[0]
        range2 = s.split(",")[1]
        lower1 = int(range1.split("-")[0])
        upper1 = int(range1.split("-")[1])
        lower2 = int(range2.split("-")[0])
        upper2 = int(range2.split("-")[1])
        wholly_contained = np.where(((lower1 >= lower2) & (upper1 <= upper2) or (lower2 >= lower1) & (upper2 <= upper1)), 1, 0)
        overlap = np.where(((lower1 >= lower2) & (lower1 <= upper2) or (lower2 >= lower1) & (lower2 <= upper1)), 1, 0)

        return Section(lower1, upper1, lower2, upper2, wholly_contained, overlap)

def count_wholly_contained(Sections: List[Section]):
    count = 0
    for section in Sections:
        count += section.wholly_contained
    return count

def count_overlapping(Sections: List[Section]):
    count = 0
    for section in Sections:
        count += section.overlap
    return count

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = f.read()
    sections = [Section.parse(s) for s in input.splitlines()]
    print(count_wholly_contained(sections))
    print(count_overlapping(sections))
