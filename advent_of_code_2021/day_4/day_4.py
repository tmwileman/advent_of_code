from typing import List, Dict

RAW = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19
 
 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


class BingoBoard:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])

        self.row_count = [0 for _ in range(self.num_rows)]
        self.col_count = [0 for _ in range(self.num_cols)]

    def mark(self, number: int) -> None:
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.grid[i][j] == number:
                    self.grid[i][j] = 0
                    self.row_count[i] += 1
                    self.col_count[j] += 1

    def score(self, number: int) -> int:
        grid_sum = sum(num for row in self.grid for num in row)
        score = grid_sum * number
        return score

    def winner(self) -> bool:
        for i in range(self.num_rows):
            if self.row_count[i] == self.num_cols:
                return True
        for i in range(self.num_cols):
            if self.col_count[i] == self.num_rows:
                return True
        return False

    @staticmethod
    def parse(raw: str) -> "BingoBoard":
        grid = []
        for line in raw.split("\n"):
            grid.append([int(x) for x in line.split()])
        return BingoBoard(grid)


class Play:
    def __init__(self, boards: List[BingoBoard], numbers: List[int]) -> None:
        self.boards = boards
        self.numbers = numbers

    def play(self) -> Dict:
        results = {}
        starting_boards = len(self.boards)
        place = 1
        for number in self.numbers:
            for board in self.boards:
                board.mark(number)
                if board.winner() and place == 1:
                    results["winner"] = board.score(number)
                    self.boards.remove(board)
                    place += 1
                elif board.winner() and place != starting_boards:
                    self.boards.remove(board)
                    place += 1
                elif board.winner() and place == starting_boards:
                    results["loser"] = board.score(number)
                else:
                    continue
        return results  # loser isn't correct

    @staticmethod
    def parse(raw: str) -> "Play":
        sections = raw.split("\n\n")
        numbers = [int(n) for n in sections[0].split(",")]

        boards = [BingoBoard.parse(board) for board in sections[1:]]

        return Play(boards, numbers)


# game = Play.parse(RAW)
# score = game.play()
# print(score)
# assert score == 4512
# score = game.loser()
# print(score)
# assert score == 1924

if __name__ == "__main__":
    raw = open(
        "/Users/thomaswileman/advent_of_code/advent_of_code_2021/day_4/input.txt"
    ).read()
    game = Play.parse(raw)
    print(game.play())
