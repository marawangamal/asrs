"""
Debug problem — easy recursion

Two recursive functions. Tests in test_recursion_easy.py fail. Find and fix.

Hint: 1 bug per function. Both involve a base case — one is missing,
one returns the wrong combination of the two sub-results.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def reverse_list(head):
    """Reverse a singly linked list recursively. Returns the new head."""
    if head is None:
        return None
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head


def max_depth(root):
    """Return the max depth of a binary tree. Empty tree has depth 0."""
    if root is None:
        return 0
    return 1 + min(max_depth(root.left), max_depth(root.right))
