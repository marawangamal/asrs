## Number
283
## Tags
leetcode
### Name
Move Zeroes
### Problem
Move all zeroes in an array to the end in-place, preserving the order of non-zero elements.
### Solution
Two-pointer same-direction. `write` tracks where the next non-zero goes; `read` scans. After the first pass, fill the remainder with zeroes.

```python
class Solution:
    def moveZeroes(self, nums):
        write = 0
        for read in range(len(nums)):
            if nums[read] != 0:
                nums[write] = nums[read]
                write += 1
        for i in range(write, len(nums)):
            nums[i] = 0
```

Or with a single swap-based pass:

```python
def moveZeroes(self, nums):
    write = 0
    for read in range(len(nums)):
        if nums[read] != 0:
            nums[write], nums[read] = nums[read], nums[write]
            write += 1
```

Same shape as problem 26 — same-direction two pointers with conditional advance.
### Source
LeetCode
