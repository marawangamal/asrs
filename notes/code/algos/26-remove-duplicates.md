## Number
26
## Tags
leetcode
### Name
Remove Duplicates from Sorted Array
### Problem
Given a sorted array, remove duplicates in-place so each element appears once. Return the new length; the first `k` elements of the array should contain the unique values.
### Solution
Two-pointer same-direction pattern. `write` is where we'll place the next unique value; `read` scans forward. Advance `write` only when we see a new value.

```python
class Solution:
    def removeDuplicates(self, nums):
        if not nums:
            return 0
        write = 1
        for read in range(1, len(nums)):
            if nums[read] != nums[read - 1]:
                nums[write] = nums[read]
                write += 1
        return write
```

The general shape: **one pointer reads, one pointer writes; advance write only on condition**. Applies to "Move Zeroes" (283) and similar in-place compaction problems.
### Source
LeetCode
