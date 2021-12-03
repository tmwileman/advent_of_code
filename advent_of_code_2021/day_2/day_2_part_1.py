from dataclasses import dataclass
from __future__ import annotations
from typing import NamedTuple, List

RAW = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


class Instruction(NamedTuple):
    op: str
    arg: int

    # Static method to parse each line into the operation and argument
    @staticmethod
    def parse(line: str) -> Instruction:
        op, arg = line.strip().split()
        return Instruction(op, int(arg))


@dataclass
class Position:
    x_pos: int = 0
    y_pos: int = 0

    def new_position(self, op: str, arg: int) -> None:
        self.op = op
        self.arg = arg

        if op == "forward":
            self.x_pos = self.x_pos + arg
        elif op == "up":
            self.y_pos = self.y_pos - arg
        elif op == "down":
            self.y_pos = self.y_pos + arg
        else:
            raise ValueError(f"unknown op: {op}")

    def run_all_instructions(self, instructions: List[Instruction]) -> None:
        for instruction in instructions:
            self.new_position(instruction.op, instruction.arg)
        return self.x_pos, self.y_pos


INSTRUCTIONS = [Instruction.parse(line) for line in RAW.split("\n")]
pos = Position()
pos = pos.run_all_instructions(INSTRUCTIONS)
assert (pos) == (15, 10)

with open(
    "/Users/thomaswileman/advent_of_code/advent_of_code_2021/day_2/input.txt"
) as f:
    raw = f.read()

instructions = [Instruction.parse(line) for line in raw.split("\n")]
pos = Position()
print(pos.run_all_instructions(instructions))
print(pos.x_pos * pos.y_pos)
