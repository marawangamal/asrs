## Number
692
## Tags
leetcode
### Name
Top K Frequent Words
### Problem
Given a list of words, return the `k` most frequent. Ties are broken by lexicographic order.
### Solution
Count, then sort with a multi-key sort: descending count, ascending word.

```python
from collections import Counter

class Solution:
    def topKFrequent(self, words, k):
        counts = Counter(words)
        return sorted(counts, key=lambda w: (-counts[w], w))[:k]
```

The multi-key sort trick: `key=lambda w: (-counts[w], w)`. Python sorts tuples lexicographically, so the first field (negated count) sorts descending and the second (word) sorts ascending — exactly what's needed for "top K with tie-breaking."

For very large input, a min-heap of size `k` is asymptotically better (O(n log k) instead of O(n log n)) but the sort-on-query version is cleaner and almost always fast enough.
### Source
LeetCode
