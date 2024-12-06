from __future__ import annotations

from itertools import chain, product
from typing import List

from .dancing_links import dlx

import json

unsolved_grid = []

def solve_sudoku(grid: List[List[int]]) -> None:
    unsolved_grid = grid;

    assert (
        len(grid) == 9
        and all((len(x) == 9 for x in grid))
        and all(isinstance(x, int) and 0 <= x <= 9 for x in chain(*grid))
    )

    print(
        f"\n*** Initial grid ***\n\n"
        + get_board_fmt().format(*(x if x != 0 else " " for x in chain(*grid)))
    )

    possibilities = [
        (r, c, n)
        for r, c in product(range(9), range(9))
        for n in (range(9) if grid[r][c] == 0 else (grid[r][c] - 1,))
    ]

    # Constraints
    # fmt: off
    constraints =      [f"R{r+1}C{c+1}" for r in range(9) for c in range(9)]    # row col
    constraints.extend([f"R{r+1}#{n+1}" for r in range(9) for n in range(9)])   # row num
    constraints.extend([f"C{c+1}#{n+1}" for c in range(9) for n in range(9)])   # col num
    constraints.extend([f"B{b+1}#{n+1}" for b in range(9) for n in range(9)])   # box num
    constraints.extend([f"D1#{n+1}" for n in range(9)])                        # main diagonal
    constraints.extend([f"D2#{n+1}" for n in range(9)])                        # anti-diagonal
    # fmt: on

    constraints_ids = {c: i for i, c in enumerate(constraints)}

    # Exact cover matrix
    m = [[0] * len(constraints) for _ in range(len(possibilities))]
    for i, (r, c, n) in enumerate(possibilities):
        b = 3 * (r // 3) + c // 3  # compute box idx from row and col
        cell_constraints = [
            f"R{r+1}C{c+1}",
            f"R{r+1}#{n+1}",
            f"C{c+1}#{n+1}",
            f"B{b+1}#{n+1}",
        ]

        # Add diagonal constraints
        if r == c:
            cell_constraints.append(f"D1#{n+1}")  # Main diagonal
        if r + c == 8:
            cell_constraints.append(f"D2#{n+1}")  # Anti-diagonal

        for c in cell_constraints:
            m[i][constraints_ids[c]] = 1

    def format_solution(sol):
        sol_grid = [n + 1 for _, _, n in sorted([possibilities[i] for i in sol])]
        sol_grid = list(zip(*[iter(sol_grid)] * 9))  # reshape (9,9)
        return get_board_fmt().format(
            *(green(y) if x == 0 else x for x, y in zip(chain(*grid), chain(*sol_grid)))
        )

    temp_sol = []

    # Solve
    i = 0
    for i, sol in enumerate(dlx(m), start=1):
        #pass;
        sol_grid = [n + 1 for _, _, n in sorted([possibilities[i] for i in sol])]
        sol_grid = list(zip(*[iter(sol_grid)] * 9))  # reshape (9,9)
        temp_sol = sol_grid
        #if i == 2 and input("Find all? [Y|n] ").lower() == "n":
        #    break
        #print(f"\n*** Solution #{i} ***\n\n" + format_solution(sol))
    #else:
    #    print(f'--> Found {i} solution{"s" if i > 1 else ""}.\n')

    if i == 1:
        data = []
        with open("goodSudoku.json", "r") as f:
            data = json.load(f)
            print(data)
        with open("goodSudoku.json", "w") as f:
            print("Unique solution")
            data.append(unsolved_grid)
            json.dump(data, f)
            print(data)

        sdata = []
        with open("goodSudokuSolution.json", "r") as f:
            sdata = json.load(f)
            print(sdata)
        with open("goodSudokuSolution.json", "w") as f:
            print("Unique solution")
            sdata.append(temp_sol)
            json.dump(sdata, f)
            print(sdata)
    else:
        print("No solution or >1 solution")


##########################
# Helpers
##########################

def get_board_fmt():
    bar = "-------------------------\n"
    line = "|" + (" {:}" * 3 + " |") * 3 + "\n"
    return bar + (line * 3 + bar) * 3

def green(x: str) -> str:
    return f"\033[92m{x}\033[0m"
