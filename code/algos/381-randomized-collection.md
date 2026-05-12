## Number
381
## Tags
leetcode,design
### Name
Insert Delete GetRandom O(1) - Duplicates Allowed
### Problem
Like 380, but the collection may contain duplicates: `insert`, `remove` (one occurrence), `getRandom`, all O(1) average.
### Solution
Same idea as 380, but the index map stores a **set** of indices per value (since duplicates can live at multiple positions). On removal, pick any one index from the set and apply the swap-with-last-then-pop trick.

```python
import random
from collections import defaultdict

class RandomizedCollection:
    def __init__(self):
        self.values = []
        self.idx_of = defaultdict(set)

    def insert(self, val):
        self.idx_of[val].add(len(self.values))
        self.values.append(val)
        return len(self.idx_of[val]) == 1   # True if first occurrence

    def remove(self, val):
        if not self.idx_of[val]:
            return False
        idx = next(iter(self.idx_of[val]))
        last_idx = len(self.values) - 1
        last_val = self.values[-1]
        # Swap val at idx with last_val
        self.values[idx] = last_val
        self.idx_of[val].discard(idx)
        self.idx_of[last_val].discard(last_idx)
        if idx != last_idx:
            self.idx_of[last_val].add(idx)
        self.values.pop()
        return True

    def getRandom(self):
        return random.choice(self.values)
```

Subtlety: when the element to remove is already the last, you must `discard(last_idx)` *before* the `pop` so the set doesn't end up with a stale index. Easier said than done — trace through `[1, 1]` then `remove(1)` to convince yourself.
### Source
LeetCode
