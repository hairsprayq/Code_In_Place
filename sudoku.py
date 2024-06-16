# sudoku.py

import random

import math

import copy


class Sudoku:

    def __init__(self, N, difficulty=None):

        self.N = N

        self.difficulty = difficulty

        self.SRN = int(math.sqrt(N))

        self.table = [[0 for x in range(N)] for y in range(N)]

        self.answerable_table = None

        if self.difficulty:
            self._generate_table()

    def count_solutions(self):

        """Counts the number of valid Sudoku solutions."""

        empty_cell = self._find_empty_cell()

        if not empty_cell:  # Base case: No empty cells left

            return 1

        row, col = empty_cell

        count = 0

        for num in range(1, self.N + 1):

            if self.safe_position(row, col, num):

                self.table[row][col] = num

                count += self.count_solutions()

                self.table[row][col] = 0

                if count > 1:  # Optimization: stop early if we have 3 solutions

                    return count

        return count

    def _find_empty_cell(self):

        """Finds an empty cell in the table."""

        for row in range(self.N):

            for col in range(self.N):

                if self.table[row][col] == 0:
                    return (row, col)

        return None

    def _generate_table(self):

        """Generates a table until there is 1 solution."""

        while True:

            self.fill_diagonal()

            self.fill_remaining(0, self.SRN)

            self.remove_digits()

            if self.count_solutions() == 1:
                break  # Found a valid puzzle with 1 solution

    def fill_diagonal(self):

        for x in range(0, self.N, self.SRN):
            self.fill_cell(x, x)

    def not_in_subgroup(self, rowstart, colstart, num):

        for x in range(self.SRN):

            for y in range(self.SRN):

                if self.table[rowstart + x][colstart + y] == num:
                    return False

        return True

    def fill_cell(self, row, col):

        num = 0

        for x in range(self.SRN):

            for y in range(self.SRN):

                while True:

                    num = self.random_generator(self.N)

                    if self.not_in_subgroup(row, col, num):
                        break

                self.table[row + x][col + y] = num

    def random_generator(self, num):

        return math.floor(random.random() * num + 1)

    def safe_position(self, row, col, num):

        return (

                self.not_in_row(row, num)

                and self.not_in_col(col, num)

                and self.not_in_subgroup(row - row % self.SRN, col - col % self.SRN, num)

        )

    def not_in_row(self, row, num):

        for col in range(self.N):

            if self.table[row][col] == num:
                return False

        return True

    def not_in_col(self, col, num):

        for row in range(self.N):

            if self.table[row][col] == num:
                return False

        return True

    def fill_remaining(self, row, col):

        if row == self.N - 1 and col == self.N:
            return True

        if col == self.N:
            row += 1

            col = 0

        if self.table[row][col] != 0:
            return self.fill_remaining(row, col + 1)

        for num in range(1, self.N + 1):

            if self.safe_position(row, col, num):

                self.table[row][col] = num

                if self.fill_remaining(row, col + 1):
                    return True

            self.table[row][col] = 0

        return False

    def remove_digits(self):

        if self.difficulty == "hard":

            count = random.randint(51, 55)

        elif self.difficulty == "medium":

            count = random.randint(41, 50)

        elif self.difficulty == "easy":

            count = random.randint(31, 40)

        else:

            count = self.E

        self.answerable_table = copy.deepcopy(self.table)

        while count != 0:

            row = self.random_generator(self.N) - 1

            col = self.random_generator(self.N) - 1

            if self.answerable_table[row][col] != 0:
                count -= 1

                self.answerable_table[row][col] = 0

    def puzzle_table(self):

        return self.answerable_table

    def puzzle_answers(self):

        return self.table

    def puzzle_solved(self):

        for row in range(self.N):

            for col in range(self.N):

                if self.answerable_table[row][col] == 0:
                    return False

        return True

    def print_sudoku(self):

        for row in range(self.N):

            for col in range(self.N):
                print(self.table[row][col], end=" ")

            print()

        print("")

        for row in range(self.N):

            for col in range(self.N):
                print(self.answerable_table[row][col], end=" ")

            print()


if __name__ == "__main__":
    N = 9

    E = (N * N) // 2

    sudoku = Sudoku(N, E)

    sudoku.print_sudoku()