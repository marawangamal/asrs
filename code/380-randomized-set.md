## Number
380
## Tags
leetcode,design
### Name
Insert Delete GetRandom O(1)
### Problem
Implement a set supporting `insert`, `remove`, and `getRandom`, all in O(1) average time.
### Solution
Hash map (`val -> index`) + array of values. The trick for O(1) deletion is **swap with the last element, then pop**.

```python
import random

class RandomizedSet:
    def __init__(self):
        self.values = []
        self.idx_of = {}

    def insert(self, val):
        if val in self.idx_of:
            return False
        self.idx_of[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val):
        if val not in self.idx_of:
            return False
        idx = self.idx_of[val]
        last = self.values[-1]
        self.values[idx] = last
        self.idx_of[last] = idx
        self.values.pop()
        del self.idx_of[val]
        return True

    def getRandom(self):
        return random.choice(self.values)
```

The swap-with-last-then-pop trick is worth committing to muscle memory — it makes O(1) deletion from an array possible whenever order doesn't matter.
### Source
LeetCode
