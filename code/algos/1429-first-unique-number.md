## Number
1429
## Tags
leetcode,design
### Name
First Unique Number
### Problem
Design a data structure that supports `showFirstUnique()` (returns the first number in the stream that occurs exactly once, or -1) and `add(value)`.
### Solution
The read/write tradeoff problem. Optimize `add` to O(1) amortized and `showFirstUnique` to O(1) amortized by maintaining an `OrderedDict` of "currently unique" values plus a count map.

```python
from collections import OrderedDict

class FirstUnique:
    def __init__(self, nums):
        self.counts = {}
        self.uniques = OrderedDict()
        for x in nums:
            self.add(x)

    def add(self, value):
        self.counts[value] = self.counts.get(value, 0) + 1
        if self.counts[value] == 1:
            self.uniques[value] = None
        elif value in self.uniques:
            del self.uniques[value]

    def showFirstUnique(self):
        if not self.uniques:
            return -1
        return next(iter(self.uniques))
```

Trick: an `OrderedDict` preserves insertion order, and `next(iter(...))` peeks at the first key in O(1). Removing from the middle is O(1) too because it's backed by a doubly linked list. This is the same machinery LRU uses, repurposed for "first thing matching a property."
### Source
LeetCode
