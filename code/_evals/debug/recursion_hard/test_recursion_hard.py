import unittest

from recursion_hard import is_match, solve_n_queens


class TestIsMatch(unittest.TestCase):
    def test_empty_both(self):
        self.assertTrue(is_match("", ""))

    def test_literal_match(self):
        self.assertTrue(is_match("abc", "abc"))

    def test_literal_mismatch(self):
        self.assertFalse(is_match("abc", "abd"))

    def test_dot(self):
        self.assertTrue(is_match("abc", "a.c"))

    def test_star_zero(self):
        self.assertTrue(is_match("", "a*"))

    def test_star_one(self):
        self.assertTrue(is_match("a", "a*"))

    def test_star_many(self):
        self.assertTrue(is_match("aa", "a*"))

    def test_star_many_long(self):
        self.assertTrue(is_match("aaaaaa", "a*"))

    def test_dot_star(self):
        self.assertTrue(is_match("ab", ".*"))

    def test_classic(self):
        self.assertTrue(is_match("aab", "c*a*b"))

    def test_classic_mismatch(self):
        self.assertFalse(is_match("mississippi", "mis*is*p*."))


class TestNQueens(unittest.TestCase):
    def test_n1(self):
        sols = solve_n_queens(1)
        self.assertEqual(sols, [["Q"]])

    def test_n2_no_solution(self):
        self.assertEqual(solve_n_queens(2), [])

    def test_n3_no_solution(self):
        self.assertEqual(solve_n_queens(3), [])

    def test_n4_count(self):
        self.assertEqual(len(solve_n_queens(4)), 2)

    def test_n4_well_formed(self):
        # Each solution should have exactly n rows, each of length n,
        # and exactly n queens total (one per row).
        sols = solve_n_queens(4)
        for sol in sols:
            self.assertEqual(len(sol), 4)
            for row in sol:
                self.assertEqual(len(row), 4)
                self.assertEqual(row.count("Q"), 1)
            total_qs = sum(row.count("Q") for row in sol)
            self.assertEqual(total_qs, 4)

    def test_n5_count(self):
        self.assertEqual(len(solve_n_queens(5)), 10)

    def test_n6_count(self):
        self.assertEqual(len(solve_n_queens(6)), 4)


if __name__ == "__main__":
    unittest.main()
