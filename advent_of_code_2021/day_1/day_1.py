from typing import List

INPUTS = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def count_increasing_depth(inputs: List[int]) -> int:
    """
    Count the number of times the input list is increasing in depth.

    Inputs:
        inputs: List of integers.
    Output:
        int: Number of times the input list is increasing in depth.
    """

    # Initalize the count of increasing depth
    increasing_depth_count = 0

    # Compare each input to the next input.
    # If the initial is smaller, increase the count by one.
    for i, depth in enumerate(inputs[:-1]):
        next_depth = inputs[i + 1]
        if next_depth > depth:
            increasing_depth_count += 1
        else:
            pass

    return increasing_depth_count


assert count_increasing_depth(INPUTS) == 7


def sum_three_depths(inputs: List[int]) -> List[int]:
    """
    Create a list of all sums of three sequential depths.

    Inputs:
        inputs: List of integers.
    Output:
        List: Sums of the combinations of three sequential depths.
    """

    combinations = []
    for i, depth in enumerate(inputs[:-2]):
        second_depth = inputs[i + 1]
        third_depth = inputs[i + 2]
        sum_of_depths = depth + second_depth + third_depth
        combinations.append(sum_of_depths)

    return combinations


assert sum_three_depths(INPUTS) == [607, 618, 618, 617, 647, 716, 769, 792]


with open(
    "/Users/thomaswileman/advent_of_code/advent_of_code_2021/day_1/input.txt"
) as f:
    raw = [int(i) for i in f.read().splitlines()]
    print(count_increasing_depth(raw))
    print(count_increasing_depth(sum_three_depths(raw)))
