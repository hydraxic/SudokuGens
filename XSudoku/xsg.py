# took my old C# X-sudoku generator and converted it to python, making some changes too

import math
import random
from typing import List, Tuple
import json

class Extensions:
    @staticmethod
    def shuffle(lst: List):
        n = len(lst)
        while n > 1:
            n -= 1
            k = random.randint(0, n)
            lst[k], lst[n] = lst[n], lst[k]

class XSudoku:
    def __init__(self, N: int, K: int):
        self.N = N
        self.K = K
        self.SRN = int(math.sqrt(N))
        self.mat = [[0 for _ in range(N)] for _ in range(N)]
        self.sMat = [[0 for _ in range(N)] for _ in range(N)]
        self.diagonal_main = {(i, i) for i in range(N)}
        self.diagonal_secondary = {(i, N - 1 - i) for i in range(N)}
        self.candidates = [[set(range(1, N + 1)) for _ in range(N)] for _ in range(N)]
        self.found_solutions = []

    def random_generator(self, num: int) -> int:
        return random.randint(1, num)

    def fill_values(self) -> bool:
        self.mat = [[0 for _ in range(self.N)] for _ in range(self.N)]
        if not self.fill_remaining(0, 0):
            return False

        self.sMat = [row[:] for row in self.mat]
        if self.check_if_complete():
            self.remove_k_digits_v2()
            return True
        return False

    def fill_remaining(self, i: int, j: int) -> bool:
        if j >= self.N:
            i += 1
            j = 0
        if i >= self.N:
            return True

        if self.mat[i][j] != 0:
            return self.fill_remaining(i, j + 1)

        # Shuffle candidates to avoid predictable patterns
        candidate_list = list(self.candidates[i][j])
        Extensions.shuffle(candidate_list)

        for num in candidate_list:
            if self.is_valid(i, j, num):
                self.mat[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.mat[i][j] = 0

        return False

    def is_valid(self, row: int, col: int, num: int) -> bool:
        return (
            self.unused_in_row(row, num) and
            self.unused_in_col(col, num) and
            self.unused_in_box(row - row % self.SRN, col - col % self.SRN, num) and
            self.unused_in_diagonals(row, col, num)
        )

    def unused_in_row(self, row: int, num: int) -> bool:
        return num not in self.mat[row]

    def unused_in_col(self, col: int, num: int) -> bool:
        return all(self.mat[i][col] != num for i in range(self.N))

    def unused_in_box(self, box_start_row: int, box_start_col: int, num: int) -> bool:
        for i in range(self.SRN):
            for j in range(self.SRN):
                if self.mat[box_start_row + i][box_start_col + j] == num:
                    return False
        return True

    def unused_in_diagonals(self, row: int, col: int, num: int) -> bool:
        if (row, col) in self.diagonal_main:
            if any(self.mat[i][i] == num for i in range(self.N)):
                return False
        if (row, col) in self.diagonal_secondary:
            if any(self.mat[i][self.N - 1 - i] == num for i in range(self.N)):
                return False
        return True

    def check_if_complete(self) -> bool:
        for row in self.mat:
            if sorted(row) != list(range(1, self.N + 1)):
                return False
        for col in zip(*self.mat):
            if sorted(col) != list(range(1, self.N + 1)):
                return False
        return True

    def remove_k_digits_v2(self):
        count = self.K
        while count > 0:
            row = random.randint(0, self.N - 1)
            col = random.randint(0, self.N - 1)
            if self.mat[row][col] != 0:
                self.mat[row][col] = 0
                count -= 1

    def find_empty(self, board: List[List[int]]) -> Tuple[int, int] | None:
        for i in range(self.N):
            for j in range(self.N):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def valid(self, board: List[List[int]], pos: Tuple[int, int], num: int) -> bool:
        for i in range(self.N):
            if board[i][pos[1]] == num:
                return False

        for j in range(self.N):
            if board[pos[0]][j] == num:
                return False

        start_i = pos[0] - pos[0] % self.SRN
        start_j = pos[1] - pos[1] % self.SRN
        for i in range(self.SRN):
            for j in range(self.SRN):
                if board[start_i + i][start_j + j] == num:
                    return False
        return True

    def find_all_solutions(self, board: List[List[int]]) -> bool:
        empty = self.find_empty(board)
        if not empty:
            return True

        for nums in range(1, self.N + 1):
            if self.valid(board, empty, nums):
                board[empty[0]][empty[1]] = nums

                if self.find_all_solutions(board):
                    if board not in self.found_solutions:
                        self.found_solutions.append(board)
                    if len(self.found_solutions) > 1:
                        return False
                    #return True
                board[empty[0]][empty[1]] = 0

        return True

# print sudoku
#count = 1

amt = 10

with open("/content/goodSudoku.json", "w") as f:
    json.dump([], f)

with open("/content/goodSudokuSolution.json", "w") as f:
    json.dump([], f)

for _ in range(amt):

    with open("/content/sudoku_dancing_links-main/genSudoku.txt", "w") as f:

        sudoku = XSudoku(9, 50)
        output_string = ""
        if sudoku.fill_values():
            for row in sudoku.mat:
                for i in row:
                    output_string += str(i) + " "
                output_string += "\n"
            f.write(output_string)

    # run this file
    #!python sudoku_dancing_links-main/main.py sudoku_dancing_links-main/genSudoku.txt

#sudoku.found_solutions = []
#print(sudoku.find_all_solutions(sudoku.mat))
#print(len(sudoku.found_solutions))

'''

    for row in sudoku.mat:
        rount = 1
        for i in row:
            # if round divided by 3 is integer,
            if rount % 3 == 0 and rount != 9:
                print(f"{i} |", end=" ")
            else:
                print(i, end=" ")
            rount += 1

        if count % 3 == 0 and count != 9:
            print("\n" + "-" * 25)
        else:
            print("\n")

        count += 1;

    print("\n" + "-" * 25 + "\n")

    for row in sudoku.sMat:
        rount = 1
        for i in row:
            # if round divided by 3 is integer,
            if rount % 3 == 0 and rount != 9:
                print(f"{i} |", end=" ")
            else:
                print(i, end=" ")
            rount += 1

        if count % 3 == 0 and count != 9:
            print("\n" + "-" * 25)
        else:
            print("\n")

        count += 1;

'''

# -----------
# unique solution verification

