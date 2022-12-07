from dataclasses import dataclass
from typing import List

outcomes = {
    "A X":4, 
    "A Y":8, 
    "A Z":3,
    "B X":1, 
    "B Y":5, 
    "B Z":9,
    "C X":7, 
    "C Y":2, 
    "C Z":6
}

new_outcomes = {
    "A X":3, 
    "A Y":4, 
    "A Z":8,
    "B X":1, 
    "B Y":5, 
    "B Z":9,
    "C X":2, 
    "C Y":6, 
    "C Z":7
}

def parse(input) -> List[str]:
    return [line for line in input.strip().split("\n")]

def max_points():
    with open('input.txt') as f:
        input = f.read()
    
    return sum([outcomes[x] for x in parse(input)])

def new_max_points():
    with open('input.txt') as f:
        input = f.read()
    
    return sum([new_outcomes[x] for x in parse(input)])

if __name__ == "__main__":
    print(max_points()) 
    print(new_max_points())
