from dataclasses import dataclass
from typing import List

@dataclass
class Elf():
    foods: List[int]
    
    def cals(self) -> int:
        return sum(self.foods)
    
def parse(input) -> List[Elf]:
    return [Elf([int(x) for x in line.split("\n")]) for line in input.strip().split("\n\n")]

def max_cals():
    with open('input.txt') as f:
        input = f.read()
    
    return max([elf.cals() for elf in parse(input)])

def top_three():
    with open('input.txt') as f:
        input = f.read()
    
    return sum(sorted([elf.cals() for elf in parse(input)], reverse=True)[:3])

if __name__ == "__main__":
    print(max_cals())
    print(top_three())
