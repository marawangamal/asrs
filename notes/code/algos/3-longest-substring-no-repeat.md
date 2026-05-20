## Number
3
## Tags
leetcode
### Name
Longest Substring Without Repeating Characters
### Problem
Given a string, return the length of the longest substring with no repeated characters.
### Solution
Variable-size sliding window. Expand `right` to grow the window; contract `left` while the invariant ("no duplicates in the window") is violated.

```python
class Solution:
    def lengthOfLongestSubstring(self, s):
        seen = {}            # char -> most recent index
        left = 0
        best = 0
        for right, ch in enumerate(s):
            if ch in seen and seen[ch] >= left:
                left = seen[ch] + 1
            seen[ch] = right
            best = max(best, right - left + 1)
        return best
```

The general variable-window pattern: expand `right`, contract `left` while invariant violated, record best window. O(n) — each character is visited at most twice.
### Source
LeetCode
