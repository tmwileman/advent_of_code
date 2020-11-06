"""
Out here in deep space, many things can go wrong. Fortunately, many of those things have indicator lights. Unfortunately, one of those lights is lit: the oxygen system for part of the ship has failed!

According to the readouts, the oxygen system must have failed days ago after a rupture in oxygen tank two; that section of the ship was automatically sealed once oxygen levels went dangerously low. A single remotely-operated repair droid is your only option for fixing the oxygen system.

The Elves' care package included an Intcode program (your puzzle input) that you can use to remotely control the repair droid. By running that program, you can direct the repair droid to the oxygen system and fix the problem.

The remote control program executes the following steps in a loop forever:

    Accept a movement command via an input instruction.
    Send the movement command to the repair droid.
    Wait for the repair droid to finish the movement operation.
    Report on the status of the repair droid via an output instruction.

Only four movement commands are understood: north (1), south (2), west (3), and east (4). Any other command is invalid. The movements differ in direction, but not in distance: in a long enough east-west hallway, a series of commands like 4,4,4,4,3,3,3,3 would leave the repair droid back where it started.

The repair droid can reply with any of the following status codes:

    0: The repair droid hit a wall. Its position has not changed.
    1: The repair droid has moved one step in the requested direction.
    2: The repair droid has moved one step in the requested direction; its new position is the location of the oxygen system.

You don't know anything about the area around the repair droid, but you can figure it out by watching the status codes.

For example, we can draw the area using D for the droid, # for walls, . for locations the droid can traverse, and empty space for unexplored locations. Then, the initial state looks like this:

      
      
   D  
      
      

To make the droid go north, send it 1. If it replies with 0, you know that location is a wall and that the droid didn't move:

      
   #  
   D  
      
      

To move east, send 4; a reply of 1 means the movement was successful:

      
   #  
   .D 
      
      

Then, perhaps attempts to move north (1), south (2), and east (4) are all met with replies of 0:

      
   ## 
   .D#
    # 
      

Now, you know the repair droid is in a dead end. Backtrack with 3 (which you already know will get a reply of 1 because you already know that location is open):

      
   ## 
   D.#
    # 
      

Then, perhaps west (3) gets a reply of 0, south (2) gets a reply of 1, south again (2) gets a reply of 0, and then west (3) gets a reply of 2:

      
   ## 
  #..#
  D.# 
   #  

Now, because of the reply of 2, you know you've found the oxygen system! In this example, it was only 2 moves away from the repair droid's starting position.

What is the fewest number of movement commands required to move the repair droid from its starting position to the location of the oxygen system?
"""

from typing import List, NamedTuple, Tuple, Iterable, Set, Dict, Callable
from enum import Enum
import itertools
from collections import deque, defaultdict
import logging
import copy


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
    # logging.debug(f"parsing {opcode}")

    opcode_part = opcode % 100

    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10

    return Opcode(opcode_part), modes


class IntcodeComputer:
    def __init__(self, program: List[int], get_input: Callable[[], int]) -> None:
        self.program = defaultdict(int)
        self.program.update({i: value for i, value in enumerate(program)})
        self.get_input = get_input
        self.pos = 0
        self.relative_base = 0

    def save(self):
        return [
            copy.deepcopy(self.program),
            self.get_input,
            self.pos,
            self.relative_base
        ]

    @staticmethod
    def load(program, get_input, pos, relative_base):
        computer = IntcodeComputer([], get_input)
        computer.program = program
        computer.pos = pos
        computer.relative_base = relative_base
        return computer

    def _get_value(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos]]}")
            return self.program[self.program[pos]]
        elif mode == 1:
            # immediate mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[self.program[pos] + self.relative_base]}")
            return self.program[self.program[pos] + self.relative_base]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def _loc(self, pos: int, mode: int) -> int:
        if mode == 0:
            # pointer mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos]}")
            return self.program[pos]
        elif mode == 2:
            # relative mode
            # logging.debug(f"pos: {pos}, mode: {mode}, value: {self.program[pos] + self.relative_base}")
            return self.program[pos] + self.relative_base

    def go(self) -> int:

        while True:
            # logging.debug(f"program: {self.program}")
            # logging.debug(f"pos: {self.pos}, inputs: {self.inputs}, relative_base: {self.relative_base}")

            opcode, modes = parse_opcode(self.program[self.pos])

            # logging.debug(f"opcode: {opcode}, modes: {modes}")

            if opcode == Opcode.END_PROGRAM:
                raise EndProgram

            elif opcode == Opcode.ADD:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 + value2
                self.pos += 4

            elif opcode == Opcode.MULTIPLY:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                self.program[loc] = value1 * value2
                self.pos += 4

            elif opcode == Opcode.STORE_INPUT:
                # Get input and store at location
                loc = self._loc(self.pos + 1, modes[0])
                input_value = self.get_input()
                self.program[loc] = input_value
                self.pos += 2

            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self._get_value(self.pos + 1, modes[0])
                self.pos += 2
                # logging.debug(f"output: {value}")

                ####
                ####

                return value

            elif opcode == Opcode.JUMP_IF_TRUE:
                # jump if true
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                # logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 != 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.JUMP_IF_FALSE:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])

                # logging.debug(f"value1: {value1}, value2: {value2}")

                if value1 == 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.LESS_THAN:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 < value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                value1 = self._get_value(self.pos + 1, modes[0])
                value2 = self._get_value(self.pos + 2, modes[1])
                loc = self._loc(self.pos + 3, modes[2])

                # logging.debug(f"value1: {value1}, value2: {value2}, loc: {loc}")

                if value1 == value2:
                    self.program[loc] = 1
                else:
                    self.program[loc] = 0
                self.pos += 4

            elif opcode == Opcode.ADJUST_RELATIVE_BASE:
                value = self._get_value(self.pos + 1, modes[0])

                # logging.debug(f"value: {value}")

                self.relative_base += value
                self.pos += 2

            else:
                raise ValueError(f"invalid opcode: {opcode}")

PROGRAM = [3,1033,1008,1033,1,1032,1005,1032,31,1008,1033,2,1032,1005,1032,58,1008,1033,3,1032,1005,1032,81,1008,1033,4,1032,1005,1032,104,99,101,0,1034,1039,102,1,1036,1041,1001,1035,-1,1040,1008,1038,0,1043,102,-1,1043,1032,1,1037,1032,1042,1106,0,124,1002,1034,1,1039,101,0,1036,1041,1001,1035,1,1040,1008,1038,0,1043,1,1037,1038,1042,1105,1,124,1001,1034,-1,1039,1008,1036,0,1041,1002,1035,1,1040,102,1,1038,1043,1001,1037,0,1042,1106,0,124,1001,1034,1,1039,1008,1036,0,1041,1001,1035,0,1040,1001,1038,0,1043,1001,1037,0,1042,1006,1039,217,1006,1040,217,1008,1039,40,1032,1005,1032,217,1008,1040,40,1032,1005,1032,217,1008,1039,1,1032,1006,1032,165,1008,1040,39,1032,1006,1032,165,1102,2,1,1044,1105,1,224,2,1041,1043,1032,1006,1032,179,1101,0,1,1044,1105,1,224,1,1041,1043,1032,1006,1032,217,1,1042,1043,1032,1001,1032,-1,1032,1002,1032,39,1032,1,1032,1039,1032,101,-1,1032,1032,101,252,1032,211,1007,0,45,1044,1106,0,224,1101,0,0,1044,1105,1,224,1006,1044,247,102,1,1039,1034,102,1,1040,1035,102,1,1041,1036,1001,1043,0,1038,1002,1042,1,1037,4,1044,1106,0,0,12,89,14,22,56,12,54,34,71,12,40,31,83,2,95,25,4,70,18,59,32,11,19,23,67,17,25,18,72,14,60,9,85,6,84,89,2,14,10,44,85,34,63,11,23,79,6,56,4,88,69,20,2,88,87,31,56,16,68,29,84,43,58,6,14,98,73,3,35,79,24,89,43,59,12,78,86,13,10,61,37,46,44,61,25,12,71,36,65,79,31,5,71,13,99,90,87,35,40,98,3,80,69,97,31,37,93,37,78,34,48,32,51,41,75,50,16,25,10,92,88,28,50,7,95,11,15,99,10,61,56,25,14,99,23,23,90,73,66,94,23,60,34,26,73,44,38,71,41,42,79,10,25,69,43,39,92,19,35,95,23,60,8,75,38,55,82,40,44,29,84,82,33,36,63,93,10,7,50,41,22,76,79,59,42,61,40,72,4,51,5,83,99,22,79,33,6,53,62,30,77,37,22,94,84,43,19,60,52,44,82,99,23,47,29,68,57,38,66,40,55,17,15,78,86,10,54,25,52,39,62,35,11,19,15,75,12,20,63,67,98,35,70,17,95,66,24,37,56,10,75,3,95,35,41,62,8,3,60,72,5,98,61,27,42,63,16,55,29,6,54,48,40,7,66,92,31,48,16,41,87,86,6,16,24,53,85,17,4,12,20,89,74,5,84,67,27,37,67,30,29,27,92,46,40,14,77,95,50,17,31,38,44,83,12,39,12,98,96,20,7,69,82,7,12,75,49,85,59,17,44,98,58,28,94,34,81,49,48,66,51,43,5,96,52,22,81,36,83,94,32,28,94,27,97,18,99,32,49,53,31,16,61,57,18,87,22,93,18,21,25,77,33,78,41,34,69,5,28,15,87,38,98,38,41,83,10,61,90,21,92,35,93,51,35,92,23,50,23,5,51,97,60,36,69,4,62,20,39,88,11,48,56,9,92,8,85,78,62,24,62,82,15,16,30,81,34,9,98,94,8,16,85,22,75,40,62,78,25,70,16,47,28,93,32,21,62,53,94,62,14,75,19,69,8,47,9,39,90,35,10,86,50,15,84,42,72,19,24,5,77,79,3,93,66,6,89,16,11,55,32,37,38,28,50,78,21,29,35,13,95,71,3,14,12,96,23,75,33,97,26,41,96,88,68,22,39,18,4,7,46,91,8,55,39,37,28,47,79,38,73,11,72,8,28,76,70,69,27,84,37,84,79,81,34,71,97,43,94,74,13,58,14,64,20,53,22,67,86,39,46,28,50,34,62,54,8,41,24,68,57,80,94,32,79,18,61,15,90,23,6,67,92,18,18,83,36,46,44,31,76,39,2,77,23,93,10,67,37,25,46,19,87,21,2,92,92,92,68,27,13,38,42,85,13,46,39,61,96,9,53,29,44,81,84,91,11,79,75,5,13,88,84,19,1,18,38,86,42,6,85,63,40,93,3,33,83,41,82,51,79,37,85,1,53,40,39,74,33,54,29,23,49,21,31,43,29,98,32,70,59,10,24,21,74,89,20,96,78,21,25,9,99,52,8,39,64,25,29,95,37,49,94,35,1,85,48,5,97,23,64,41,98,14,76,97,55,56,11,23,81,42,98,43,46,37,22,99,1,98,91,58,20,23,94,53,63,23,59,8,32,94,37,70,24,33,69,79,77,35,32,52,79,17,62,31,30,70,61,20,2,54,17,46,36,75,58,61,33,71,10,50,10,53,10,79,30,79,41,91,80,52,20,54,65,84,24,85,9,69,11,54,12,83,86,54,27,68,9,86,0,0,21,21,1,10,1,0,0,0,0,0,0]

class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Status(Enum):
    WALL = 0
    MOVED = 1
    OXYGEN = 2

DIRECTIONS = [Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST]
ANTI_DIRECTIONS = [Direction.SOUTH, Direction.NORTH, Direction.EAST, Direction.WEST]
DELTAS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def find_oxygen() -> IntcodeComputer:
    """
    return the length of the shortest path to the oxygen
    """
    visited = {(0, 0)}

    inputs = deque([])
    def get_input() -> int:
        return inputs.popleft()

    computer = IntcodeComputer(PROGRAM, get_input)

    frontier = deque([])
    frontier.append((computer.save(), 0, (0, 0)))
    
    while frontier:
        save_state, num_steps, (x, y) = frontier.popleft()
        # print(num_steps, x, y)
        computer = IntcodeComputer.load(*save_state)
        # print("pos1", computer.pos, sum(computer.program.values()))

        for direction, anti, (dx, dy) in zip(DIRECTIONS, ANTI_DIRECTIONS, DELTAS):
            # print(direction, anti, dx, dy)
            inputs.append(direction.value)
            status = Status(computer.go())
            # print("pos2", computer.pos, sum(computer.program.values()))
            # print("status", status)
            if status == Status.OXYGEN:
                print("found oxygen after", num_steps + 1, "steps")
                return computer
            elif status == Status.WALL:
                pass
            elif status == Status.MOVED:
                new_loc = (x + dx, y + dy)
                if new_loc not in visited:
                    # print(new_loc, visited)
                    visited.add(new_loc)
                    frontier.append((computer.save(), num_steps + 1, new_loc))
                    # move back
                    inputs.append(anti.value)
                    computer.go()
                    # print("pos3", computer.pos, sum(computer.program.values()))
                else:
                    # print("already been here")
                    # move back
                    inputs.append(anti.value)
                    computer.go()
                    # print("pos3", computer.pos, sum(computer.program.values()))
            
computer = find_oxygen()

"""
You quickly repair the oxygen system; oxygen gradually fills the area.

Oxygen starts in the location containing the repaired oxygen system. It takes one minute for oxygen to spread to all open locations that are adjacent to a location that already contains oxygen. Diagonal locations are not adjacent.

In the example above, suppose you've used the droid to explore the area fully and have the following map (where locations that currently contain oxygen are marked O):

 ##   
#..## 
#.#..#
#.O.# 
 ###  

Initially, the only location which contains oxygen is the location of the repaired oxygen system. However, after one minute, the oxygen spreads to all open (.) locations that are adjacent to a location containing oxygen:

 ##   
#..## 
#.#..#
#OOO# 
 ###  

After a total of two minutes, the map looks like this:

 ##   
#..## 
#O#O.#
#OOO# 
 ###  

After a total of three minutes:

 ##   
#O.## 
#O#OO#
#OOO# 
 ###  

And finally, the whole region is full of oxygen after a total of four minutes:

 ##   
#OO## 
#O#OO#
#OOO# 
 ###  

So, in this example, all locations contain oxygen after 4 minutes.

Use the repair droid to get a complete map of the area. How many minutes will it take to fill with oxygen?
"""

def furthest_point(computer: IntcodeComputer) -> int:
    visited = {(0, 0)}

    inputs = deque([])
    def get_input() -> int:
        return inputs.popleft()

    computer.get_input = get_input

    frontier = deque([])
    frontier.append((computer.save(), 0, (0, 0)))
    
    while frontier:
        save_state, num_steps, (x, y) = frontier.popleft()
        print(num_steps, x, y)
        # print(num_steps, x, y)
        computer = IntcodeComputer.load(*save_state)
        # print("pos1", computer.pos, sum(computer.program.values()))

        for direction, anti, (dx, dy) in zip(DIRECTIONS, ANTI_DIRECTIONS, DELTAS):
            # print(direction, anti, dx, dy)
            inputs.append(direction.value)
            status = Status(computer.go())
            # print("pos2", computer.pos, sum(computer.program.values()))
            # print("status", status)
            if status == Status.WALL:
                pass
            else:
                new_loc = (x + dx, y + dy)
                if new_loc not in visited:
                    # print(new_loc, visited)
                    visited.add(new_loc)
                    frontier.append((computer.save(), num_steps + 1, new_loc))
                    # move back
                    inputs.append(anti.value)
                    computer.go()
                    # print("pos3", computer.pos, sum(computer.program.values()))
                else:
                    # print("already been here")
                    # move back
                    inputs.append(anti.value)
                    computer.go()
                    # print("pos3", computer.pos, sum(computer.program.values()))

    return num_steps

print(furthest_point(computer))