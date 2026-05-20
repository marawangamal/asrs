## Number
1244
## Tags
leetcode,design
### Name
Design A Leaderboard
### Problem
Support `addScore(playerId, score)` (adds to a player's score), `top(K)` (sum of top K scores), and `reset(playerId)` (sets player's score to 0).
### Solution
The pure "top N by metric" pattern. For a timed test, sort-on-query is almost always fast enough and far less buggy than maintaining a sorted structure.

```python
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def addScore(self, playerId, score):
        self.scores[playerId] = self.scores.get(playerId, 0) + score

    def top(self, K):
        return sum(sorted(self.scores.values(), reverse=True)[:K])

    def reset(self, playerId):
        self.scores[playerId] = 0
```

Rule of thumb: always start with sort-on-query. Only swap to a `SortedList` (from `sortedcontainers`) or a heap if profiling proves it's needed — premature optimization here causes bugs and costs levels on a timed test.

For "top K by value, ties broken by key":
```python
sorted(items.items(), key=lambda kv: (-kv[1], kv[0]))[:K]
```
### Source
LeetCode
