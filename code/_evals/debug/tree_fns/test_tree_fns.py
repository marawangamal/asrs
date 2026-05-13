import unittest

from tree_fns import (
    TreeDir,
    TreeFile,
    tree_files_at_depth,
    tree_find_files,
    tree_total_size,
)


class TestTreeDebug(unittest.TestCase):
    def setUp(self):
        self.tree = TreeDir(
            "root",
            (
                TreeFile("a.txt", 10),
                TreeDir(
                    "sub",
                    (
                        TreeFile("b.txt", 20),
                        TreeFile("c.txt", 30),
                    ),
                ),
                TreeFile("d.txt", 40),
            ),
        )

    def test_total_size(self):
        self.assertEqual(tree_total_size(self.tree), 100)

    def test_total_size_leaf(self):
        self.assertEqual(tree_total_size(TreeFile("x", 7)), 7)

    def test_find_files(self):
        out = tree_find_files(self.tree, min_size=20)
        self.assertEqual(sorted(out), ["b.txt", "c.txt", "d.txt"])

    def test_find_files_called_twice(self):
        # A second call should NOT see results from the first.
        tree_find_files(self.tree, min_size=0)
        out = tree_find_files(self.tree, min_size=100)
        self.assertEqual(out, [])

    def test_files_at_depth_0_root_is_dir(self):
        self.assertEqual(tree_files_at_depth(self.tree, 0), [])

    def test_files_at_depth_1(self):
        self.assertEqual(sorted(tree_files_at_depth(self.tree, 1)), ["a.txt", "d.txt"])

    def test_files_at_depth_2(self):
        self.assertEqual(sorted(tree_files_at_depth(self.tree, 2)), ["b.txt", "c.txt"])


if __name__ == "__main__":
    unittest.main()
