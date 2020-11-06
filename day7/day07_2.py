"""
It's no good - in this configuration, the amplifiers can't generate a large enough output signal to produce the thrust you'll need. The Elves quickly talk you through rewiring the amplifiers into a feedback loop:

      O-------O  O-------O  O-------O  O-------O  O-------O
0 -+->| Amp A |->| Amp B |->| Amp C |->| Amp D |->| Amp E |-.
   |  O-------O  O-------O  O-------O  O-------O  O-------O |
   |                                                        |
   '--------------------------------------------------------+
                                                            |
                                                            v
                                                     (to thrusters)

Most of the amplifiers are connected as they were before; amplifier A's output is connected to amplifier B's input, and so on. However, the output from amplifier E is now connected into amplifier A's input. This creates the feedback loop: the signal will be sent through the amplifiers many times.

In feedback loop mode, the amplifiers need totally different phase settings: integers from 5 to 9, again each used exactly once. These settings will cause the Amplifier Controller Software to repeatedly take input and produce output many times before halting. Provide each amplifier its phase setting at its first input instruction; all further input/output instructions are for signals.

Don't restart the Amplifier Controller Software on any amplifier during this process. Each one should continue receiving and sending signals until it halts.

All signals sent or received in this process will be between pairs of amplifiers except the very first signal and the very last signal. To start the process, a 0 signal is sent to amplifier A's input exactly once.

Eventually, the software on the amplifiers will halt after they have processed the final loop. When this happens, the last output signal from amplifier E is sent to the thrusters. Your job is to find the largest output signal that can be sent to the thrusters using the new phase settings and feedback loop arrangement.

Here are some example programs:

    Max thruster signal 139629729 (from phase setting sequence 9,8,7,6,5):

    3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
    27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5

    Max thruster signal 18216 (from phase setting sequence 9,7,8,5,6):

    3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
    -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
    53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10

Try every combination of the new phase settings on the amplifier feedback loop. What is the highest signal that can be sent to the thrusters?
"""

from typing import List, NamedTuple, Tuple
from enum import Enum
import itertools
from collections import deque

class Opcode(Enum):
    ADD = 1
    MULTIPLY = 2
    STORE_INPUT = 3
    SEND_TO_OUTPUT = 4
    JUMP_IF_TRUE = 5
    JUMP_IF_FALSE = 6
    LESS_THAN = 7
    EQUALS = 8
    END_PROGRAM = 99

Modes = List[int]

def parse_opcode(opcode: int, num_modes: int = 3) -> Tuple[Opcode, Modes]:
    opcode_part = opcode % 100
    
    modes: List[int] = []
    opcode = opcode // 100

    for _ in range(num_modes):
        modes.append(opcode % 10)
        opcode = opcode // 10
    
    return Opcode(opcode_part), modes

Program = List[int]

class Amplifier:
    def __init__(self, program: List[int], phase: int) -> None:
        self.program = program[:]
        self.inputs = deque([phase])
        self.pos = 0
    
    def get_value(self, pos: int, mode: int) -> int:
        if mode == 0:
            return self.program[self.program[pos]]
        elif mode == 1:
            return self.program[pos]
        else:
            raise ValueError(f"unknown mode: {mode}")

    def step(self: int, input_value: int) -> int:
        self.inputs.append(input_value)

        while True:
            opcode, modes = parse_opcode(self.program[self.pos])

            if opcode == Opcode.END_PROGRAM:
                return None
            elif opcode == Opcode.ADD:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])
                self.program[self.program[self.pos + 3]] = value1 + value2
                self.pos += 4

            elif opcode == Opcode.MULTIPLY:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])
                self.program[self.program[self.pos + 3]] = value1 * value2
                self.pos += 4

            elif opcode == Opcode.STORE_INPUT:
                # Get input and store at location
                loc = self.program[self.pos + 1]
                input_value = self.inputs.popleft()
                self.program[loc] = input_value
                self.pos += 2

            elif opcode == Opcode.SEND_TO_OUTPUT:
                # Get output from location
                value = self.get_value(self.pos + 1, modes[0])
                self.pos += 2
                return value

            elif opcode == Opcode.JUMP_IF_TRUE:
                # jump if true
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 != 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.JUMP_IF_FALSE:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 == 0:
                    self.pos = value2
                else:
                    self.pos += 3

            elif opcode == Opcode.LESS_THAN:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 < value2:
                    self.program[self.program[self.pos + 3]] = 1
                else:
                    self.program[self.program[self.pos + 3]] = 0
                self.pos += 4

            elif opcode == Opcode.EQUALS:
                value1 = self.get_value(self.pos + 1, modes[0])
                value2 = self.get_value(self.pos + 2, modes[1])

                if value1 == value2:
                    self.program[self.program[self.pos + 3]] = 1
                else:
                    self.program[self.program[self.pos + 3]] = 0
                self.pos += 4

            else:
                raise RuntimeError(f"invalid opcode: {opcode}")

def run_amplifiers(program: List[int], phases: List[int]) -> int:
    amplifiers = [Amplifier(program, phase) for phase in phases]
    n = len(amplifiers)
    num_finished = 0

    last_output = 0
    last_non_none_output = None
    aid = 0

    while num_finished < n:
        last_output = amplifiers[aid].step(last_output)
        if last_output is None:
            num_finished += 1
        else:
            last_non_none_output = last_output
        aid = (aid + 1) % n
    
    return last_non_none_output

PROG1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
PHASES1 = [9,8,7,6,5]
assert run_amplifiers(PROG1, PHASES1) == 139629729

def best_output(program: List[int]) -> int:
    return max(run_amplifiers(program, phases)
                for phases in itertools.permutations([5, 6, 7, 8, 9]))

assert best_output(PROG1) == 139629729

PROGRAM = [3,8,1001,8,10,8,105,1,0,0,21,46,59,72,93,110,191,272,353,434,99999,3,9,101,4,9,9,1002,9,3,9,1001,9,5,9,102,2,9,9,1001,9,5,9,4,9,99,3,9,1002,9,5,9,1001,9,5,9,4,9,99,3,9,101,4,9,9,1002,9,4,9,4,9,99,3,9,102,3,9,9,101,3,9,9,1002,9,2,9,1001,9,5,9,4,9,99,3,9,1001,9,2,9,102,4,9,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,99]

print(best_output(PROGRAM))