## Number
141
## Tags
leetcode
### Name
Linked List Cycle
### Problem
Return `True` if a linked list contains a cycle.
### Solution
Floyd's tortoise and hare. Two pointers, slow advances by 1, fast by 2. If there's a cycle, they meet; if fast reaches `None`, no cycle.

```python
class Solution:
    def hasCycle(self, head):
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False
```

O(n) time, O(1) space. A hash set of visited nodes also works (O(n) space) but Floyd's is the canonical answer.
### Source
LeetCode
