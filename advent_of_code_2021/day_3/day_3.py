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
    def parse(line: str) -> DiagnosticData:
        code = line
        return DiagnosticData(code=code)


class PowerConsumption:
    """
    Class to calculate rates and power from diagnostic data.
    """

    gamma: int
    epsilon: int
    power: int
    code_by_position: Dict

    @staticmethod
    def code_by_position(codes: List):
        codes_by_position = {}
        for code in codes:
            code_dict = {i: j for i, j in enumerate(code)}
            for key, value in code_dict.items():
                if key in codes_by_position:
                    codes_by_position[key].append(value)
                else:
                    codes_by_position[key] = [value]

        return codes_by_position

    @staticmethod
    def calc_rates(self, code_dict: Dict) -> int:

        self.gamma = ""
        self.epsilon = ""

        for key, value in code_dict.items():
            count = Counter(value).most_common()
            x = count[0][0]
            y = count[-1][0]
            self.gamma += x
            self.epsilon += y

        return self.gamma, self.epsilon

    @staticmethod
    def calc_power(self, gamma: str, epsilon: str) -> int:

        self.gamma = int(gamma, 2)
        self.epsilon = int(epsilon, 2)

        self.power = self.gamma * self.epsilon

        return self.power


pwr = PowerConsumption()
data = [DiagnosticData.parse(line) for line in RAW.split("\n")]
code_list = pwr.code_by_position(data)
gamma, epsilon = pwr.calc_rates(code_list)
power = pwr.calc_power(gamma, epsilon)

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
print(power)
