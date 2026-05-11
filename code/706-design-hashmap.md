## Number
706
## Tags
leetcode,design
### Name
Design HashMap
### Problem
Implement a hash map (`put`, `get`, `remove`) without using built-in hash table libraries.
### Solution
This is the "build the primitive" problem. Array of buckets, each bucket is a list of `(key, value)` pairs. Hash function is `key % size`; resolve collisions by chaining.

```python
class MyHashMap:
    def __init__(self):
        self.size = 1000
        self.buckets = [[] for _ in range(self.size)]

    def _bucket(self, key):
        return self.buckets[key % self.size]

    def put(self, key, value):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b[i] = (key, value)
                return
        b.append((key, value))

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return -1

    def remove(self, key):
        b = self._bucket(key)
        for i, (k, _) in enumerate(b):
            if k == key:
                b.pop(i)
                return
```

The real lesson: don't reimplement this in actual test problems — Python's `dict` is already a hash table.
### Source
LeetCode
