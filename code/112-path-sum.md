## Number
112
## Tags
leetcode
### Name
Path Sum
### Problem
Given a binary tree and a target sum, return `True` if there exists a root-to-leaf path whose node values sum to the target.
### Solution
Canonical recursion: subtract as you descend rather than accumulate. At each leaf, check whether the leaf's value equals what's left of the target. The `or` short-circuits, giving an early exit for free.

```python
class Solution:
    def hasPathSum(self, root, targetSum):
        if not root:
            return False
        if not root.left and not root.right:
            return root.val == targetSum
        remaining = targetSum - root.val
        return (self.hasPathSum(root.left, remaining) or
                self.hasPathSum(root.right, remaining))
```

Key lesson: don't try to mutate a `targetFound` flag passed as a parameter. In Python, assignment rebinds the local name and never propagates to the caller — immutable types (bool, int, float, str, tuple) can't be mutated, so the only thing you can do is rebind, and rebinding is local. **Information that needs to flow up the recursion must be returned, not written through a parameter.**

A common wrong "optimization" is to prune when `pathSum > targetSum` — unsound because the problem allows negative node values.

Iterative stack version for very deep/skewed trees:

```python
def hasPathSum(self, root, targetSum):
    if not root:
        return False
    stack = [(root, targetSum - root.val)]
    while stack:
        node, remaining = stack.pop()
        if not node.left and not node.right and remaining == 0:
            return True
        if node.right:
            stack.append((node.right, remaining - node.right.val))
        if node.left:
            stack.append((node.left, remaining - node.left.val))
    return False
```
### Source
LeetCode
