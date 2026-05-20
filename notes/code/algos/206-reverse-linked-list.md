## Number
206
## Tags
leetcode
### Name
Reverse Linked List
### Problem
Reverse a singly linked list and return the new head.
### Solution
Iterative pointer juggling with a `prev` accumulator and a saved `next`:

```python
class Solution:
    def reverseList(self, head):
        prev = None
        curr = head
        while curr:
            nxt = curr.next       # save before overwrite
            curr.next = prev      # flip pointer
            prev = curr           # advance prev
            curr = nxt            # advance curr
        return prev
```

Order of the four assignments matters — you must save `curr.next` before overwriting it. Same skill set as the doubly-linked-list helpers in LRU Cache.
### Source
LeetCode
