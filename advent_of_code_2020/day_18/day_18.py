from __future__ import annotations
from dataclasses import dataclass
from typing import List
import re

Expression = List[str]

def evaluate(expression: Expression) -> int:
    value = int(expression[0])
    for i in range(1, len(expression), 2):
        op = expression[i]
        if op == "+":
            value = value + int(expression[i+1])
        elif op == "*":
            value = value * int(expression[i+1])
        else:
            raise ValueError(f"bad op: {op}")
    
    return value

rgx = r"\([^\(]+?\)"

def evaluate_raw(raw: str) -> int:
    while (match := re.search(rgx, raw)):
        value = evaluate(match.group()[1:-1].split())
        raw = raw[:match.start()] + str(value) + raw[match.end():]
    else:
        tokens = raw.split()
        return evaluate(tokens)
    
def evaluate2(expression: Expression) -> int:
    while len(expression) > 1:
        if "+" in expression:
            i = expression.index("+")
            new_val = int(expression[i - 1]) + int(expression[i + 1])
            expression = expression[:i - 1] + [str(new_val)] + expression[i + 2:]
        else:
            return evaluate(expression)
    
    return int(expression[0])

def evaluate_raw2(raw: str) -> int:
    while (match := re.search(rgx, raw)):
        value = evaluate2(match.group()[1:-1].split())
        raw = raw[:match.start()] + str(value) + raw[match.end():]
    else:
        tokens = raw.split()
        return evaluate2(tokens)

RAW = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

assert evaluate_raw(RAW) == 13632
assert evaluate_raw2(RAW) == 23340

with open('/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_18/input.txt') as f:
    raw = f.read()
    lines = raw.split("\n")
    print(sum(evaluate_raw(line) for line in lines))
    print(sum(evaluate_raw2(line) for line in lines))