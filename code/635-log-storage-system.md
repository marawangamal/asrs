## Number
635
## Tags
leetcode,design
### Name
Design Log Storage System
### Problem
Store log entries with timestamps formatted as `Year:Month:Day:Hour:Minute:Second`. Retrieve all log IDs whose timestamps fall within a range at a given granularity (year, month, day, hour, minute, second).
### Solution
Store raw `(id, timestamp_string)` pairs. On retrieval, truncate both query bounds and each stored timestamp to the requested granularity, then filter.

```python
class LogSystem:
    GRAN = {"Year": 4, "Month": 7, "Day": 10,
            "Hour": 13, "Minute": 16, "Second": 19}

    def __init__(self):
        self.logs = []

    def put(self, id, timestamp):
        self.logs.append((id, timestamp))

    def retrieve(self, start, end, granularity):
        idx = self.GRAN[granularity]
        lo, hi = start[:idx], end[:idx]
        return [id for id, ts in self.logs if lo <= ts[:idx] <= hi]
```

The key insight is that the timestamp string is fixed-width and lexicographically sortable — so range comparison reduces to string comparison after truncating to a prefix length. No date parsing needed. Generalizes the "as of time T" pattern (problem 981) to range queries with variable granularity.
### Source
LeetCode
