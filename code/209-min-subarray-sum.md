## Number
209
## Tags
leetcode
### Name
Minimum Size Subarray Sum
### Problem
Given an array of positive integers and a target, return the minimal length of a contiguous subarray whose sum is at least `target`. Return 0 if none exists.
### Solution
Variable-size sliding window. Expand `right` while adding to the sum; contract `left` while the sum is still ≥ target, recording the smallest valid window.

```python
class Solution:
    def minSubArrayLen(self, target, nums):
        left = 0
        total = 0
        best = float('inf')
        for right, x in enumerate(nums):
            total += x
            while total >= target:
                best = min(best, right - left + 1)
                total -= nums[left]
                left += 1
        return 0 if best == float('inf') else best
```

The pattern: expand right while invariant violated (sum < target); contract left while invariant satisfied (sum ≥ target), capturing the best length on the way. O(n).

Note: this pattern works only because all values are positive — that guarantees adding to the sum can only push it up and removing only push it down, so the window dynamics are monotone. For arrays with negatives, prefix sums + a different technique would be needed.
### Source
LeetCode
