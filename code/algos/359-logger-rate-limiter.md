## Number
359
## Tags
leetcode,design
### Name
Logger Rate Limiter
### Problem
Implement `shouldPrintMessage(timestamp, message)` that returns `True` only if the same message has not been printed in the last 10 seconds.
### Solution
Simplest correct version: `dict[message -> last_timestamp]`.

```python
class Logger:
    def __init__(self):
        self.last = {}

    def shouldPrintMessage(self, timestamp, message):
        if message in self.last and timestamp - self.last[message] < 10:
            return False
        self.last[message] = timestamp
        return True
```

This grows unboundedly with unique messages. If a follow-up asks for bounded memory, switch to a sliding-window-with-deque:

```python
from collections import deque

class Logger:
    def __init__(self):
        self.queue = deque()
        self.recent = set()

    def shouldPrintMessage(self, timestamp, message):
        while self.queue and self.queue[0][0] <= timestamp - 10:
            _, msg = self.queue.popleft()
            self.recent.discard(msg)
        if message in self.recent:
            return False
        self.queue.append((timestamp, message))
        self.recent.add(message)
        return True
```

The sliding-window-with-deque pattern generalizes to any "events in the last N seconds" question.
### Source
LeetCode
