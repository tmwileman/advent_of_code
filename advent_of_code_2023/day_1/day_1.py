class Line:
    def __init__(self, line):
        self.line = line

    def get_first_digit(self) -> int:
        for char in self.line:
            if char.isdigit():
                return char
        return None
    
    def get_last_digit(self) -> int:
        for char in reversed(self.line):
            if char.isdigit():
                return char
        return None
    
    def get_first_calibration_value(self) -> int:
        first_digit = self.get_first_digit()
        last_digit = self.get_last_digit()

        calibration_value = int(str(first_digit) + str(last_digit))

        return calibration_value
    
    def get_digit_dict(self) -> int:
        written_to_digit = {
        'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 
        'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9'
        }

        digit_positions = {}

        position = 0

        while position < len(self.line):
            found_digit = False

            if self.line[position].isdigit():
                digit = self.line[position]
                if position not in digit_positions:
                    digit_positions[position] = []
                digit_positions[position].append(digit)
                position += 1
                found_digit = True

            if not found_digit:
                for written_digit, digit in written_to_digit.items():
                    if self.line[position:].startswith(written_digit):
                        if position not in digit_positions:
                            digit_positions[position] = []
                        digit_positions[position].append(digit)
                        position += len(written_digit)
                        found_digit = True

            if not found_digit:
                position += 1
        return digit_positions
    
    def get_second_calibration_value(self) -> int:
        digit_positions = self.get_digit_dict()

        lowest_key = min(digit_positions.keys())
        highest_key = max(digit_positions.keys())

        first_digit = digit_positions[lowest_key][0]
        last_digit = digit_positions[highest_key][0]

        calibration_value = int(str(first_digit) + str(last_digit))

        return calibration_value

def main():
    sum_of_first_calibration_values = 0
    sum_of_second_calibration_values = 0

    with open('input.txt', 'r') as f:
        for l in f:
            line = Line(l.strip())
            first_calibration_value = line.get_first_calibration_value()
            sum_of_first_calibration_values += first_calibration_value
            second_calibration_value = line.get_second_calibration_value()
            sum_of_second_calibration_values += second_calibration_value

    print(f"The sum of first calibration values is {sum_of_first_calibration_values}.")
    print(f"The sum of second calibration values is {sum_of_second_calibration_values}.")

if __name__ == "__main__":
    main()  