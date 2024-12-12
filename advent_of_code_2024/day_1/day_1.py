EXAMPLE = """3   4
4   3
2   5
1   3
3   9
3   3"""


class LocationLists:
    def __init__(
        self,
        lists: str,
    ):

        self.lists = lists
        self.left_list, self.right_list = self._parse_lists()
        self.distance_list = self._calc_distances()
        self.total_distances = self._sum_distances()
        self.occurence_dict = self._occurence_dict()
        self.similarity_score = self._similarity_score()

    def _parse_lists(self):
        left_list, right_list = [], []
        for line in self.lists.split("\n"):
            left, right = line.split()
            left_list.append(int(left))
            right_list.append(int(right))
        left_list = self._order_lists(left_list)
        right_list = self._order_lists(right_list)
        return left_list, right_list

    def _order_lists(self, list):
        list.sort()
        return list

    def _calc_distance(self, left, right):
        return abs(left - right)

    def _calc_distances(self):
        return [self._calc_distance(left, right) for left, right in zip(self.left_list, self.right_list)]

    def _sum_distances(self):
        return sum(self.distance_list)

    def _occurence_dict(self):
        occurence_dict = {}
        for i in self.left_list:
            if i in self.right_list:
                for val in self.right_list:
                    if i == val:
                        if i in occurence_dict:
                            occurence_dict[i] += 1
                        else:
                            occurence_dict[i] = 1
            else:
                occurence_dict[i] = 0
        return occurence_dict

    def _similarity_score(self):
        score = 0
        for key, value in self.occurence_dict.items():
            score += key * value
        return score


if __name__ == "__main__":
    example_lists = LocationLists(EXAMPLE)
    assert example_lists.total_distances == 11
    assert example_lists.similarity_score == 31
    print(f"Example Distance: {example_lists.total_distances}")
    print(f"Example Similarity Score: {example_lists.similarity_score}")

    with open("advent_of_code_2024/day_1/input.txt") as f:
        input = f.read()
    input_lists = LocationLists(input)
    print(f"Input Distance: {input_lists.total_distances}")
    print(f"Example Similarity Score: {input_lists.similarity_score}")
