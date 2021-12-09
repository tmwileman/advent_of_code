from collections import Counter
from typing import Dict, List

RAW = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""


class DiagnosticData(str):
    """
    Class to hold the data for the diagnostic.
    """

    code: str

    @staticmethod
    def parse(line: str) -> "DiagnosticData":
        code = line
        return DiagnosticData(code)


class PowerConsumption:
    """
    Class to calculate rates and power from diagnostic data.
    """

    gamma: int
    epsilon: int
    power: int
    code_by_position: Dict
    oxygen: int
    co2: int

    def code_by_position(self, codes: List):
        codes_by_position = {}
        for code in codes:
            code_dict = {i: j for i, j in enumerate(code)}
            for key, value in code_dict.items():
                if key in codes_by_position:
                    codes_by_position[key].append(value)
                else:
                    codes_by_position[key] = [value]

        return codes_by_position

    def calc_rates(self, code_dict: Dict) -> int:

        gamma = ""
        epsilon = ""

        for key, value in code_dict.items():
            count = Counter(value).most_common()
            x = count[0][0]
            y = count[-1][0]
            gamma += x
            epsilon += y

        return gamma, epsilon

    def calc_power(self, gamma: str, epsilon: str) -> int:

        gamma = int(gamma, 2)
        epsilon = int(epsilon, 2)

        power = gamma * epsilon

        return power

    def most_common_int(self, codes: List, position: int) -> int:

        self.zero = 0
        self.one = 0

        for self.code in codes:
            for self.x, self.y in enumerate(self.code):
                if self.x == position and self.y == "1":
                    self.one += 1
                elif self.x == position and self.y == "0":
                    self.zero += 1

        return self.zero, self.one

    @staticmethod
    def filter_list(
        codes: List, rating: str, position: int, zero_count: int, one_count: int
    ) -> List:

        filtered_codes = []

        if rating == "o2":
            if zero_count > one_count:
                bit = "0"
            elif one_count >= zero_count:
                bit = "1"

        if rating == "co2":
            if zero_count <= one_count:
                bit = "0"
            elif one_count < zero_count:
                bit = "1"

        for code in codes:
            for i, j in enumerate(code):
                if i == position and j == bit:
                    filtered_codes.append(code)
                else:
                    pass

        return filtered_codes

    def calc_o2(self, codes: List) -> int:

        for code in codes[0:1]:
            length = len(code)

        for x in range(length):
            position = x
            zero, one = self.most_common_int(codes, position)
            filtered_codes = self.filter_list(codes, "o2", position, zero, one)
            codes = filtered_codes
            if len(filtered_codes) == 1:
                code = filtered_codes[0]
                break

        o2 = int(code, 2)

        return o2

    def calc_co2(self, codes: List) -> int:

        for code in codes[0:1]:
            length = len(code)

        for x in range(length):
            position = x
            zero, one = self.most_common_int(codes, position)
            filtered_codes = self.filter_list(codes, "co2", position, zero, one)
            codes = filtered_codes
            if len(filtered_codes) == 1:
                code = filtered_codes[0]
                break

        co2 = int(code, 2)
        return co2

    def calc_life_support(self, o2: int, co2: int) -> int:

        life_support = o2 * co2

        return life_support


pwr = PowerConsumption()
data = [DiagnosticData.parse(line) for line in RAW.split("\n")]
code_list = pwr.code_by_position(data)
gamma, epsilon = pwr.calc_rates(code_list)
power = pwr.calc_power(gamma, epsilon)
o2 = pwr.calc_o2(codes=data)
co2 = pwr.calc_co2(codes=data)
life_support = pwr.calc_life_support(o2, co2)

assert o2 == 23
assert co2 == 10
assert life_support == 230
assert power == 198

with open(
    "/Users/thomaswileman/advent_of_code/advent_of_code_2021/day_3/input.txt"
) as f:
    raw = f.read()

pwr = PowerConsumption()
data = [DiagnosticData.parse(line) for line in raw.split("\n")]
code_list = pwr.code_by_position(data)
gamma, epsilon = pwr.calc_rates(code_list)
power = pwr.calc_power(gamma, epsilon)
o2 = pwr.calc_o2(codes=data)
co2 = pwr.calc_co2(codes=data)
life_support = pwr.calc_life_support(o2, co2)
print(power)
print(life_support)
