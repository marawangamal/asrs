import unittest

from recursion_easy import ListNode, TreeNode, max_depth, reverse_list


def build_list(vals):
    head = None
    for v in reversed(vals):
        head = ListNode(v, head)
    return head


def list_to_vals(head):
    out = []
    while head is not None:
        out.append(head.val)
        head = head.next
    return out


class TestReverseList(unittest.TestCase):
    def test_empty(self):
        self.assertIsNone(reverse_list(None))

    def test_single(self):
        head = ListNode(1)
        rev = reverse_list(head)
        self.assertEqual(list_to_vals(rev), [1])

    def test_multi(self):
        head = build_list([1, 2, 3, 4, 5])
        rev = reverse_list(head)
        self.assertEqual(list_to_vals(rev), [5, 4, 3, 2, 1])


class TestMaxDepth(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(max_depth(None), 0)

    def test_single(self):
        self.assertEqual(max_depth(TreeNode(1)), 1)

    def test_balanced(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        self.assertEqual(max_depth(root), 2)

    def test_left_skewed(self):
        # 1 -> 2 -> 3 -> 4 (all left children)
        root = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
        self.assertEqual(max_depth(root), 4)

    def test_unbalanced(self):
        # depth 1 on the left, depth 3 on the right
        root = TreeNode(
            1,
            TreeNode(2),
            TreeNode(3, None, TreeNode(4, None, TreeNode(5))),
        )
        self.assertEqual(max_depth(root), 4)


if __name__ == "__main__":
    unittest.main()
