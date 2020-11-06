"""
Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

For example:

    For a mass of 12, divide by 3 and round down to get 4, then subtract 2 to get 2.
    For a mass of 14, dividing by 3 and rounding down still yields 4, so the fuel required is also 2.
    For a mass of 1969, the fuel required is 654.
    For a mass of 100756, the fuel required is 33583.
    """

def fuel(mass: int) -> int:
    fuel = mass // 3 -2
    return fuel

assert fuel(12) == 2
assert fuel(14) == 2
assert fuel(1969) == 654
assert fuel(100756) == 33583

with open('day_1_input.txt') as f:
    masses = [int(line.strip()) for line in f]
    part1 = sum(fuel(mass) for mass in masses)

print(part1)

"""
So, for each module mass, calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass and repeat the process, continuing until a fuel requirement is zero or negative. For example:

    A module of mass 14 requires 2 fuel. This fuel requires no further fuel (2 divided by 3 and rounded down is 0, which would call for a negative fuel), so the total fuel required is still just 2.
    At first, a module of mass 1969 requires 654 fuel. Then, this fuel requires 216 more fuel (654 / 3 - 2). 216 then requires 70 more fuel, which requires 21 fuel, which requires 5 fuel, which requires no further fuel. So, the total fuel required for a module of mass 1969 is 654 + 216 + 70 + 21 + 5 = 966.
    The fuel required by a module of mass 100756 and its fuel is: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346.
"""

def fuel_for_fuel(mass: int) -> int:
    fuel_for_fuel = 0
    fuel_mass = fuel(mass)

    while fuel_mass > 0:
        fuel_for_fuel += fuel_mass
        fuel_mass = fuel(fuel_mass)
    
    return fuel_for_fuel

assert fuel_for_fuel(14) == 2
assert fuel_for_fuel(1969) == 966
assert fuel_for_fuel(100756) == 50346

with open('day_1_input.txt') as f:
    masses = [int(line.strip()) for line in f]
    part2 = sum(fuel_for_fuel(mass) for mass in masses)

print(part2)