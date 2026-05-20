## Number
35
## Tags
leetcode
### Name
Search Insert Position
### Problem
Given a sorted array and a target, return the index where the target is found, or the index where it would be inserted to keep the array sorted.
### Solution
Standard binary search. `bisect_left` from the standard library does this directly:

```python
from bisect import bisect_left

class Solution:
    def searchInsert(self, nums, target):
        return bisect_left(nums, target)
```

Manual binary search:

```python
class Solution:
    def searchInsert(self, nums, target):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo
```

Good 5-minute exercise to ground the `bisect` mental model.

`bisect_left` vs `bisect_right`: if the target exists in the array, `bisect_left` returns the existing index, `bisect_right` returns the index just after. So `arr[bisect_left(arr, x)] == x` if `x` is present, but `arr[bisect_right(arr, x) - 1] == x`.
### Source
LeetCode
