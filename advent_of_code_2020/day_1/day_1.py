from typing import List

INPUTS = [1721, 979, 366, 299, 675, 1456]

def find_product(inputs: List[int]) -> int:
    """
    Find the two elements that add up to 2020 and return their product
    """

    # Create a set of the difference between 2020 and each input.
    needs = {2020 - i for i in inputs}
    
    # For each value in the input list, if it is also in the needs list, return that number and the difference of 2020 and that number (the number in the needs set).
    for i in inputs:
        if i in needs:
            return i * (2020 - i)

assert find_product(INPUTS) == 514579

with open("/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_1/input.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print(find_product(inputs))

def find_product3(inputs: List[int]) -> int:
    """
    Find the three elements that add up to 2020 and return their product
    """

    # Create a set of the result of 2020 minus each combination of input values.
    needs = {2020 - i  - j: (i, j)
            for i in inputs
            for j in inputs
            if i != j}
    
    # For each input, if that input is in needs, j and k equal the previous i and j values. Return the product of the three numbers.
    for i in inputs:
        if i in needs:
            j, k = needs[i]
            return i * j * k

assert find_product3(INPUTS) == 241861950

with open("/Users/thomaswileman/advent_of_code/advent_of_code_2020/day_1/input.txt") as f:
    inputs = [int(line.strip()) for line in f]
    print(find_product3(inputs))