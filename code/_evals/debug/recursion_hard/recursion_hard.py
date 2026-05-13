"""
Debug problem — hard recursion

Two recursive functions. Tests in test_recursion_hard.py fail. Find and fix.

Hint: 1 bug per function.
  - One is an off-by-one in how an indexed recursion advances on a repeat.
  - One is missing state restoration during backtracking.
"""


def is_match(s, p):
    """Regex match `s` against pattern `p`. Pattern supports:
      - '.' matches any single character
      - '*' matches zero or more of the preceding element
    The match must cover the entire string.
    """

    def dp(i, j):
        if j == len(p):
            return i == len(s)
        first_match = i < len(s) and (p[j] == s[i] or p[j] == ".")
        if j + 1 < len(p) and p[j + 1] == "*":
            return dp(i, j + 2) or (first_match and dp(i + 1, j + 2))
        return first_match and dp(i + 1, j + 1)

    return dp(0, 0)


def solve_n_queens(n):
    """Return all distinct solutions to the N-Queens puzzle.

    Each solution is a list of n strings of length n where 'Q' marks a queen
    and '.' marks an empty cell.
    """
    solutions = []
    cols = set()
    pos_diag = set()  # cells where row + col matches
    neg_diag = set()  # cells where row - col matches
    board = [["."] * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            solutions.append(["".join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row + col) in pos_diag or (row - col) in neg_diag:
                continue
            cols.add(col)
            pos_diag.add(row + col)
            neg_diag.add(row - col)
            board[row][col] = "Q"
            backtrack(row + 1)
            cols.remove(col)
            pos_diag.remove(row + col)
            neg_diag.remove(row - col)

    backtrack(0)
    return solutions
