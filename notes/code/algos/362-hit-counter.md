## Number
362
## Tags
leetcode,design
### Name
Design Hit Counter
### Problem
`hit(timestamp)` records a hit; `getHits(timestamp)` returns the number of hits in the past 5 minutes (300 seconds). Timestamps are monotonically increasing.
### Solution
Deque of timestamps. On each query, pop expired entries from the front, then return the length.

```python
from collections import deque

class HitCounter:
    def __init__(self):
        self.hits = deque()

    def hit(self, timestamp):
        self.hits.append(timestamp)

    def getHits(self, timestamp):
        while self.hits and self.hits[0] <= timestamp - 300:
            self.hits.popleft()
        return len(self.hits)
```

Direct generalization of Logger Rate Limiter. The sliding-window-with-deque pattern is high-leverage — any "events in the last N seconds" question is this shape.
### Source
LeetCode
