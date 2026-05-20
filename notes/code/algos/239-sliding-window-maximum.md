## Number
239
## Tags
leetcode
### Name
Sliding Window Maximum
### Problem
Given an array `nums` and window size `k`, return an array of the maximum value in each sliding window of size `k`.
### Solution
Monotonic deque holding indices, kept in decreasing order of their values. The front is always the max of the current window.

```python
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums, k):
        dq = deque()  # stores indices; values at those indices are decreasing
        result = []
        for i, x in enumerate(nums):
            # drop indices outside the window
            while dq and dq[0] <= i - k:
                dq.popleft()
            # maintain decreasing order
            while dq and nums[dq[-1]] < x:
                dq.pop()
            dq.append(i)
            if i >= k - 1:
                result.append(nums[dq[0]])
        return result
```

O(n) — each index is pushed and popped at most once. The monotonic-deque technique generalizes to many "max/min in a moving window" problems.
### Source
LeetCode
