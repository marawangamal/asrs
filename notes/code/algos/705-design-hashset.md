## Number
705
## Tags
leetcode,design
### Name
Design HashSet
### Problem
Implement a hash set (`add`, `remove`, `contains`) without using built-in hash structures.
### Solution
Trivial after 706. Array of buckets, each bucket a list of keys.

```python
class MyHashSet:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key):
        return self.buckets[key % self.size]

    def add(self, key):
        b = self._bucket(key)
        if key not in b:
            b.append(key)

    def remove(self, key):
        b = self._bucket(key)
        if key in b:
            b.remove(key)

    def contains(self, key):
        return key in self._bucket(key)
```

Skip unless you want a warmup for problem 706.
### Source
LeetCode
