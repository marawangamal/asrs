## Number
173
## Tags
leetcode,design
### Name
Binary Search Tree Iterator
### Problem
Implement an iterator over a BST that supports `next()` (return next in-order value) and `hasNext()`. Should use O(h) memory, where h is tree height.
### Solution
Maintain an explicit stack of nodes representing the "leftmost spine" of the remaining tree. On `next`, pop the top, push the right child's leftmost spine.

```python
class BSTIterator:
    def __init__(self, root):
        self.stack = []
        self._push_left(root)

    def _push_left(self, node):
        while node:
            self.stack.append(node)
            node = node.left

    def next(self):
        node = self.stack.pop()
        self._push_left(node.right)
        return node.val

    def hasNext(self):
        return bool(self.stack)
```

Amortized O(1) per `next` (each node is pushed and popped exactly once across all calls), O(h) memory. Implements in-order traversal lazily, the same way recursion would unroll but explicitly via a stack.
### Source
LeetCode
