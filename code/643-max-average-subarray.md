## Number
643
## Tags
leetcode
### Name
Maximum Average Subarray I
### Problem
Given an array `nums` and integer `k`, find the contiguous subarray of length `k` with the maximum average.
### Solution
Fixed-size sliding window. Compute the first window's sum, then slide: add the new element, remove the old.

```python
class Solution:
    def findMaxAverage(self, nums, k):
        s = sum(nums[:k])
        best = s
        for i in range(k, len(nums)):
            s += nums[i] - nums[i - k]
            best = max(best, s)
        return best / k
```

The pattern: maintain a running sum over a window of fixed size `k`; on each slide, do `+= new -= old`. O(n).
### Source
LeetCode
