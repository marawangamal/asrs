## Number
167
## Tags
leetcode
### Name
Two Sum II - Input Array Is Sorted
### Problem
Given a 1-indexed sorted array and a target, return the 1-based indices of two numbers that sum to the target.
### Solution
Two-pointer **opposite-ends** pattern. Move whichever pointer would change the sum toward the target.

```python
class Solution:
    def twoSum(self, numbers, target):
        lo, hi = 0, len(numbers) - 1
        while lo < hi:
            s = numbers[lo] + numbers[hi]
            if s == target:
                return [lo + 1, hi + 1]
            elif s < target:
                lo += 1
            else:
                hi -= 1
```

The general rule for opposite-ends pointers: **move whichever pointer constrains the answer**. If the sum is too small, increasing `lo` increases it; if too big, decreasing `hi` decreases it. O(n) time, O(1) space.
### Source
LeetCode
