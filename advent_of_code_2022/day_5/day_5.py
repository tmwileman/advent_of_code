import regex as re
from typing import List

TEST = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

MOVE_RGX = r"move (\d+) from (\d+) to (\d+)"

class Instruction():
    def __init__(self, num_containers, origin, destination):
        self.num_containers = num_containers
        self.origin = origin
        self.destination = destination

    @staticmethod
    def get_instructions(s: str) -> List['Instruction']:
        instructions = []
        for line in s.splitlines():
            match = re.search(MOVE_RGX, line)
            if match:
                instructions.append(Instruction(int(match.group(1)), int(match.group(2)), int(match.group(3))))
        return instructions
    
class Stack():
    def __init__(self, containers: List[str]):
        self.containers = containers

    @staticmethod
    def get_stacks(s: str):
        s = s.split("\n\n")[0]
        reversed_input = list(reversed(s.splitlines()))
        input = "\n".join(reversed_input)
        lines = input.split("\n")[1:]
        
        clean_lines = []
        for line in lines:
            new_line = re.sub(r"\s\s\s\s", " * ", line)
            clean_lines.append(new_line)
        
        stacks = {}
        for line in clean_lines:
            for i, container in enumerate(line.split()):
                if container != "*":
                    if i+1 not in stacks:
                        stacks[i+1] = []
                    stacks[i+1].append(container.replace("[", "").replace("]", ""))
                
        return stacks

def move_containers(instructions: List[Instruction], stacks: dict):
    
    for instruction in instructions:
        origin = instruction.origin
        destination = instruction.destination
        origin_values = stacks.get(origin)
        destination_values = stacks.get(destination)

        for i in range(int(instruction.num_containers)):
            if len(origin_values) == 0:
                break
            
            container = stacks.get(origin).pop(-1)
            destination_values.append(container)
        
            stacks[instruction.origin] = origin_values
            stacks[instruction.destination] = destination_values
        
    return stacks

def top_of_stacks(stacks: dict):
    s = ""
    for i in range(1, len(stacks)+1):
        value = stacks.get(i)[-1]
        if value != None:
            s += value
    print(s)
    
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        input = f.read()
    instructions = Instruction.get_instructions(input)
    stacks = Stack.get_stacks(input)
    new_stacks = move_containers(instructions, stacks)
    top_of_stacks(new_stacks)