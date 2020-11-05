from typing import List

program = [int]

def run(program: program) -> None:
    pos = 0

    while program[pos] != 99:
        opcode, pos1, pos2, pos3 = program[pos], program[pos + 1], program[pos + 2], program[pos + 3]
        if opcode == 1:
            program[pos3] = program[pos1] + program[pos2]
        elif opcode == 2:
            program[pos3] = program[pos1] * program[pos2]
        else:
            raise RuntimeError(f"invalid opcode {program[pos]}")
    
        pos += 4

def reset_alarm(program: program, one: int = 12, two: int = 2) -> int:
    program = program[:]
    program[1] = one
    program[2] = two
    run(program)
    return print(program[0])

program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,9,1,19,1,19,6,23,2,6,23,27,2,27,9,31,1,5,31,35,1,35,10,39,2,39,9,43,1,5,43,47,2,47,10,51,1,51,6,55,1,5,55,59,2,6,59,63,2,63,6,67,1,5,67,71,1,71,9,75,2,75,10,79,1,79,5,83,1,10,83,87,1,5,87,91,2,13,91,95,1,95,10,99,2,99,13,103,1,103,5,107,1,107,13,111,2,111,9,115,1,6,115,119,2,119,6,123,1,123,6,127,1,127,9,131,1,6,131,135,1,135,2,139,1,139,10,0,99,2,0,14,0]

reset_alarm(program)