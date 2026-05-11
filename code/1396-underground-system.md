## Number
1396
## Tags
leetcode,design
### Name
Design Underground System
### Problem
Track passenger check-ins and check-outs across stations and report the average travel time between any two stations.
### Solution
The "track in-flight events, aggregate on completion" pattern: two dicts, one for currently-open trips, one for accumulated totals per route.

```python
class UndergroundSystem:
    def __init__(self):
        self.active = {}   # id -> (start_station, start_time)
        self.totals = {}   # (start, end) -> (total_time, count)

    def checkIn(self, id, stationName, t):
        self.active[id] = (stationName, t)

    def checkOut(self, id, stationName, t):
        start_station, start_t = self.active.pop(id)
        route = (start_station, stationName)
        total, count = self.totals.get(route, (0, 0))
        self.totals[route] = (total + (t - start_t), count + 1)

    def getAverageTime(self, startStation, endStation):
        total, count = self.totals[(startStation, endStation)]
        return total / count
```

`pop` on check-out automatically removes the in-flight entry. Storing accumulated `(total, count)` instead of a list of durations keeps `getAverageTime` O(1) and uses constant memory per route.
### Source
LeetCode
