## Number
278
## Tags
leetcode
### Name
First Bad Version
### Problem
Given `n` versions and an API `isBadVersion(v)` (returns `True` if the version is bad; all versions after a bad one are also bad), find the first bad version with minimum API calls.
### Solution
Clean binary search template — find the leftmost `True`.

```python
class Solution:
    def firstBadVersion(self, n):
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if isBadVersion(mid):
                hi = mid           # mid might be the answer
            else:
                lo = mid + 1       # mid is definitely not the answer
        return lo
```

Two invariants worth internalizing: `lo <= answer <= hi` always holds, and `hi` is *exclusive* of "known-not-answer" while `lo` is *inclusive* of "could-be-answer." That distinction explains why one side is `mid` and the other is `mid + 1`.
### Source
LeetCode
