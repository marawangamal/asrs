## Number
295
## Tags
leetcode,design
### Name
Find Median from Data Stream
### Problem
Support `addNum(num)` and `findMedian()`, both efficient as the stream grows.
### Solution
Two heaps: a max-heap holding the lower half, a min-heap holding the upper half. Keep their sizes within 1 of each other. The median is the top of the larger heap, or the average of both tops if they're equal size.

Python's `heapq` is a min-heap only, so the max-heap is faked by negating values.

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.lower = []   # max-heap (negated values)
        self.upper = []   # min-heap

    def addNum(self, num):
        # Push to lower, then move the largest of lower to upper
        heapq.heappush(self.lower, -num)
        heapq.heappush(self.upper, -heapq.heappop(self.lower))
        # Rebalance so |lower| >= |upper| and they differ by at most 1
        if len(self.upper) > len(self.lower):
            heapq.heappush(self.lower, -heapq.heappop(self.upper))

    def findMedian(self):
        if len(self.lower) > len(self.upper):
            return -self.lower[0]
        return (-self.lower[0] + self.upper[0]) / 2
```

If a level-5 problem asks for "running median," "running quantile," or "balance two sets around a midpoint," this is the structure.
### Source
LeetCode
