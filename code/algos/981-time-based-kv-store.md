## Number
981
## Tags
leetcode,design
### Name
Time Based Key-Value Store
### Problem
Design a structure that stores `(key, value, timestamp)` triples and, given `(key, timestamp)`, returns the value with the largest `timestamp_prev <= timestamp` (or `""` if none).
### Solution
Timestamps per key are guaranteed strictly increasing, so an append-only list of `(timestamp, value)` is already sorted. Use `bisect_right` to find the insertion point, then step back one.

```python
from collections import defaultdict
from bisect import bisect_right

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key, value, timestamp):
        self.store[key].append((timestamp, value))

    def get(self, key, timestamp):
        arr = self.store[key]
        idx = bisect_right(arr, (timestamp, chr(127)))  # first entry strictly after
        if idx == 0:
            return ""
        return arr[idx - 1][1]
```

Critical gotcha: when `idx == 0`, return `""` — never `max(0, idx-1)`, which would incorrectly return the first stored value when the query timestamp is smaller than every stored timestamp.

Generalizes to any "as of time T" / versioning / TTL pattern.
### Source
LeetCode
