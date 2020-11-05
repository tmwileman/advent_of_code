"""
You're not sure what it's trying to paint, but it's definitely not a registration identifier. The Space Police are getting impatient.

Checking your external ship cameras again, you notice a white panel marked "emergency hull painting robot starting panel". The rest of the panels are still black, but it looks like the robot was expecting to start on a white panel, not a black one.

Based on the Space Law Space Brochure that the Space Police attached to one of your windows, a valid registration identifier is always eight capital letters. After starting the robot on a single white panel instead, what registration identifier does it paint on your hull?
"""

from typing import List, NamedTuple, Tuple, Iterable, Set
from enum import Enum
import itertools
from collections import deque, defaultdict
import logging


logging.basicConfig(level=logging.INFO)


class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    ADJUST_RELATIVE_BASE = 9

    END_PROGRAM = 99


Modes = List[int]
Program = List[int]


class EndProgram(Exception): pass


def parse_opcode(opcode: int, num_modes: int = 3) -> Tuple[Opcode, Modes]:
    logging.debug(f"parsing {opcode}")

    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


class IntcodeComputer:
    def __init__(self, program: List[int]) -> None:
        self.program = defaultdict(int)
        self.program.update({i: value for i, value in enumerate(program)})
        self.inputs = deque()
        self.pos = 0
        self.relative_base = 0

    def _get_value(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos]]}")
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos] + self.relative_base]}")
            return self.program[self.program[pos] + self.relative_base]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def _loc(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos] + self.relative_base}")
            return self.program[pos] + self.relative_base

    def __call__(self, input_values: Iterable[int] = ()) -> int:
        self.inputs.extend(input_values)

        while True:
            logging.debug(f"program: {self.program}")
            logging.debug(f"pos: {self.pos}, inputs: {self.inputs}, relative_base: {self.relative_base}")

            opcode, modes = parse_opcode(self.program[self.pos])

            logging.debug(f"opcode: {opcode}, modes: {modes}")

            if opcode == Opcode.END_PROGRAM:
                raise EndProgram

            elif opcode == Opcode.ADD:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 + value2
                self.pos += 4

            elif opcode == Opcode.MULTIPLY:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 * value2
                self.pos += 4

            elif opcode == Opcode.STORE_INPUT:
                # Get input and store at location
                loc = self._loc(self.pos + 1, modes[0])
                input_value = self.inputs.popleft()
                self.program[loc] = input_value
                self.pos += 2

            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self._get_value(self.pos + 1, modes[0])
                self.pos += 2
                logging.debug(f"output: {value}")
                return value

            elif opcode == Opcode.JUMP_IF_TRUE:
                # jump if true
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 != 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.JUMP_IF_FALSE:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 == 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.LESS_THAN:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 < value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 == value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                value = self._get_value(self.pos + 1, modes[0])

                logging.debug(f"value: {value}")

                self.relative_base += value
                self.pos += 2

            else:
                raise ValueError(f"invalid opcode: {opcode}")


def run(program: Program, inputs: List[int]) -> List[int]:
    outputs = []
    computer = IntcodeComputer(program)

    try:
        while True:
            outputs.append(computer(inputs))
            inputs = ()
    except EndProgram:
        return outputs

PROGRAM = [3,8,1005,8,315,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,101,0,8,29,2,1006,16,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,55,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,76,1,101,17,10,1006,0,3,2,1005,2,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,110,1,107,8,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,135,1,108,19,10,2,7,14,10,2,104,10,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,170,1,1003,12,10,1006,0,98,1006,0,6,1006,0,59,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,205,1,4,18,10,1006,0,53,1006,0,47,1006,0,86,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,239,2,9,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,266,1006,0,8,1,109,12,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,294,101,1,9,9,1007,9,1035,10,1005,10,15,99,109,637,104,0,104,1,21102,936995730328,1,1,21102,1,332,0,1105,1,436,21102,1,937109070740,1,21101,0,343,0,1106,0,436,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,179410308187,1,21101,0,390,0,1105,1,436,21101,0,29195603035,1,21102,1,401,0,1106,0,436,3,10,104,0,104,0,3,10,104,0,104,0,21102,825016079204,1,1,21102,1,424,0,1105,1,436,21102,1,825544672020,1,21102,435,1,0,1106,0,436,99,109,2,21202,-1,1,1,21102,1,40,2,21102,467,1,3,21101,0,457,0,1105,1,500,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,462,463,478,4,0,1001,462,1,462,108,4,462,10,1006,10,494,1102,0,1,462,109,-2,2106,0,0,0,109,4,1202,-1,1,499,1207,-3,0,10,1006,10,517,21102,1,0,-3,22101,0,-3,1,22101,0,-2,2,21101,1,0,3,21101,0,536,0,1106,0,541,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,564,2207,-4,-2,10,1006,10,564,21202,-4,1,-4,1105,1,632,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21101,583,0,0,1106,0,541,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,602,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,624,21202,-1,1,1,21101,624,0,0,106,0,499,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

def turn(current_direction: Direction, should_turn: int) -> Direction:
    if current_direction == Direction.UP:
        return Direction.LEFT if should_turn == 0 else Direction.RIGHT
    elif current_direction == Direction.RIGHT:
        return Direction.UP if should_turn == 0 else Direction.DOWN
    elif current_direction == Direction.DOWN:
        return Direction.RIGHT if should_turn == 0 else Direction.LEFT
    elif current_direction == Direction.LEFT:
        return Direction.DOWN if should_turn == 0 else Direction.UP

def move_forward(x: int, y: int, direction: Direction) -> Tuple[int, int]:
    if direction == Direction.UP:
        return x, y + 1
    if direction == Direction.RIGHT:
        return x + 1, y
    if direction == Direction.DOWN:
        return x, y - 1
    if direction == Direction.LEFT:
        return x - 1, y

def robot(program: Program) -> int:
    computer = IntcodeComputer(program)
    grid = defaultdict(int)
    grid[(0, 0)] = 1
    x = y = 0
    direction = Direction.UP
    painted = set()

    step = 0

    try:
        while True:
            step += 1
            current_color = grid[(x, y)]
            color_to_paint = computer([current_color])
            should_turn = computer()
            painted.add((x, y))
            grid[(x, y)] = color_to_paint
            direction = turn(direction, should_turn)
            x, y = move_forward(x, y, direction)

    except EndProgram:
        return {pos for pos, color in grid.items() if color == 1}

painted = robot(PROGRAM)

def show(positions: Set[Tuple[int, int]]):
    x_min = min(x for (x, y) in positions)
    x_max = max(x for (x, y) in positions)
    y_min = min(y for x, y in positions)
    y_max = max(y for x, y in positions)

    for y in reversed(range(y_min, y_max + 1)):
        row = ["*" if (x, y) in positions else " " for x in range (x_min, x_max + 1)]
        print("".join(row))

show(painted)