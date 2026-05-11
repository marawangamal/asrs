## Number
392
## Tags
leetcode
### Name
Is Subsequence
### Problem
Given two strings `s` and `t`, return whether `s` is a subsequence of `t` (chars of `s` appear in order within `t`, not necessarily contiguous).
### Solution
Subsequence-matching two-pointer pattern: pointer on the source (`t`) always advances; pointer on the target (`s`) advances only on a match.

```python
class Solution:
    def isSubsequence(self, s, t):
        i = 0
        for ch in t:
            if i < len(s) and s[i] == ch:
                i += 1
        return i == len(s)
```

O(|t|). The shape generalizes: any "does sequence A appear in order within sequence B?" problem decomposes to this. If many `s` queries against one large `t`, preprocess `t` into `dict[char -> sorted positions]` and binary-search per character.
### Source
LeetCode
