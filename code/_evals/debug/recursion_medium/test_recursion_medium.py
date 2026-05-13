import unittest

from recursion_medium import decode_string, permutations


def canon(perms):
    """Sort permutations into a canonical form for order-independent comparison."""
    return sorted(tuple(p) for p in perms)


class TestPermutations(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(permutations([]), [[]])

    def test_single(self):
        self.assertEqual(permutations([7]), [[7]])

    def test_two(self):
        self.assertEqual(canon(permutations([1, 2])), [(1, 2), (2, 1)])

    def test_three(self):
        expected = [
            (1, 2, 3),
            (1, 3, 2),
            (2, 1, 3),
            (2, 3, 1),
            (3, 1, 2),
            (3, 2, 1),
        ]
        self.assertEqual(canon(permutations([1, 2, 3])), expected)

    def test_count(self):
        # 4! == 24 distinct permutations
        out = permutations([1, 2, 3, 4])
        self.assertEqual(len(out), 24)
        self.assertEqual(len({tuple(p) for p in out}), 24)


class TestDecodeString(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(decode_string("3[a]"), "aaa")

    def test_two_groups(self):
        self.assertEqual(decode_string("3[a]2[bc]"), "aaabcbc")

    def test_nested(self):
        self.assertEqual(decode_string("3[a2[c]]"), "accaccacc")

    def test_mixed(self):
        self.assertEqual(decode_string("2[abc]3[cd]ef"), "abcabccdcdcdef")

    def test_multi_digit(self):
        self.assertEqual(decode_string("10[a]"), "a" * 10)

    def test_multi_digit_nested(self):
        self.assertEqual(decode_string("2[12[a]]"), "a" * 24)


if __name__ == "__main__":
    unittest.main()
