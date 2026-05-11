## Number
Pattern: Two pointers (Easy)
## Tags
grokking
### Name
Pair with Target Sum
### Problem
Given an array of numbers sorted in ascending order and a target sum, find a pair in the array whose sum is equal to the given target. Return the indices of the two numbers such that they add up to the target. If no such pair exists, return `[-1, -1]`.
### Solution
Opposite-ends two pointers. Because the array is sorted, the sum strictly increases as `i` moves right and strictly decreases as `j` moves left — so at each step you can move whichever pointer pushes the sum in the right direction.

```python
class Solution:
    def search(self, arr, target_sum):
        i, j = 0, len(arr) - 1
        while i != j:
            curr_sum = arr[i] + arr[j]
            if curr_sum == target_sum:
                return [i, j]
            elif curr_sum < target_sum:
                i += 1
            else:
                j -= 1
        return [-1, -1]
```

O(n) time, O(1) space. General rule for opposite-ends two pointers: **move whichever pointer constrains the answer** — sum too low → move the low pointer up; sum too high → move the high pointer down.
### Source
Grokking the Coding Interview
