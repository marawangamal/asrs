## Number
933
## Tags
leetcode,design
### Name
Number of Recent Calls
### Problem
Implement a counter where `ping(t)` adds a request at time `t` (strictly increasing) and returns the number of pings in `(t - 3000, t]`.
### Solution
Deque of timestamps; pop expired from the front on each call.

```python
from collections import deque

class RecentCounter:
    def __init__(self):
        self.q = deque()

    def ping(self, t):
        self.q.append(t)
        while self.q[0] < t - 3000:
            self.q.popleft()
        return len(self.q)
```

Effectively identical in shape to Hit Counter (362). The sliding-window-with-deque pattern is the answer to any "events in the last N units of time" question.
### Source
LeetCode
