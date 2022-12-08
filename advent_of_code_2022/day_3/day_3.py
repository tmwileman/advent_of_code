def get_input():
    with open("input.txt", "r") as f:
        input = f.read().splitlines()
    return input

def double_packed_items(input):
    double_packed_items = []
    for line in input:
        first_half = line[:len(line)//2]
        second_half = line[len(line)//2:]
        double_packed_items.append(list(set(first_half) & set(second_half)))
    return double_packed_items

def assign_values(input):   
    values = []
    for line in input:
        value = 0
        for letter in line:
            if letter.islower():
                value += ord(letter) - 96
            else:
                value += ord(letter) - 38
        values.append(value)
    return values

def badges(input):
    groups = [(input[x:x+3]) for x in range(0, len(input), 3)]
    common_elements = []
    for group in groups:
        common_elements.append(list(set(group[0]) & set(group[1]) & set(group[2])))
    return common_elements

def first_priority_score():
    input = get_input()
    items = double_packed_items(input)
    values = assign_values(items)
    print(sum(values))
    
def find_second_priority_score():
    input = get_input()
    common_items = badges(input)
    values = assign_values(common_items)
    print(sum(values))

if __name__ == "__main__":
    first_priority_score()
    find_second_priority_score()
    