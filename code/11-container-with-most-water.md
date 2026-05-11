## Number
11
## Tags
leetcode
### Name
Container With Most Water
### Problem
Given `n` non-negative heights representing vertical lines on the x-axis, find two lines that together with the x-axis form a container holding the most water.
### Solution
Two-pointer opposite-ends. The area is `min(height[lo], height[hi]) * (hi - lo)`. Move the *shorter* pointer inward — moving the taller one can never increase the area.

```python
class Solution:
    def maxArea(self, height):
        lo, hi = 0, len(height) - 1
        best = 0
        while lo < hi:
            best = max(best, min(height[lo], height[hi]) * (hi - lo))
            if height[lo] < height[hi]:
                lo += 1
            else:
                hi -= 1
        return best
```

Intuition: the area is bounded by the shorter line. Moving the shorter pointer is the only move that could find a taller one and improve the area; moving the taller one only shrinks the width without raising the bound.
### Source
LeetCode
