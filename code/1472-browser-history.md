## Number
1472
## Tags
leetcode,design
### Name
Design Browser History
### Problem
Support `visit(url)` (clears forward history), `back(steps)`, and `forward(steps)`, each returning the current URL.
### Solution
List with a pointer (current index). `visit` truncates everything after the current position before appending.

```python
class BrowserHistory:
    def __init__(self, homepage):
        self.history = [homepage]
        self.curr = 0

    def visit(self, url):
        self.history = self.history[:self.curr + 1]
        self.history.append(url)
        self.curr += 1

    def back(self, steps):
        self.curr = max(0, self.curr - steps)
        return self.history[self.curr]

    def forward(self, steps):
        self.curr = min(len(self.history) - 1, self.curr + steps)
        return self.history[self.curr]
```

The gotcha is the visit-clears-forward semantics — make sure you truncate first, then append. The two-stack alternative (back-stack and forward-stack) also works but is more code.

Key practice: invariant maintenance. The invariant here is "`curr` is a valid index into `history` and `history[curr]` is the current page" — every method must preserve it.
### Source
LeetCode
