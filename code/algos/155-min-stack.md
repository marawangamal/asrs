## Number
155
## Tags
leetcode,design
### Name
Min Stack
### Problem
Design a stack that supports `push`, `pop`, `top`, and `getMin` all in O(1).
### Solution
Retrieving the minimum element is the hard part — the rest comes free with a list. Use two parallel stacks. Each time you push onto the main stack, push `min(curr_min, new_val)` onto the auxiliary min stack. On pop, pop both.

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.mins = []

    def push(self, val):
        self.stack.append(val)
        self.mins.append(min(val, self.mins[-1]) if self.mins else val)

    def pop(self):
        self.stack.pop()
        self.mins.pop()

    def top(self):
        return self.stack[-1]

    def getMin(self):
        return self.mins[-1]
```
### Source
LeetCode
