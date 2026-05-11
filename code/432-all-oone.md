## Number
432
## Tags
leetcode,design
### Name
All O`one Data Structure
### Problem
Design a data structure that stores string keys associated with positive integer counts, supporting all of the following in O(1) time:
- `inc(key)`: increment `key`'s count by 1. If `key` doesn't exist, insert it with count 1.
- `dec(key)`: decrement `key`'s count by 1. If the count becomes 0, remove the key. It is guaranteed `key` exists when `dec` is called.
- `getMaxKey()`: return any key with the maximum count, or `""` if empty.
- `getMinKey()`: return any key with the minimum count, or `""` if empty.
### Solution
The LRU pattern applied to a different problem: hash map + doubly linked list of *count-buckets*. Each bucket holds the set of keys with that count, and buckets are kept sorted by count via the linked list.

- `key -> bucket_node` lookup
- Doubly linked list of buckets, each bucket has `count` and `keys` (a set)
- `getMaxKey` returns any key from the bucket at the tail; `getMinKey` from the head

On `inc(key)`: look up the key's current bucket, move it to the bucket with `count+1` (creating the bucket if it doesn't exist and inserting it after the current bucket). Symmetric for `dec`. If a bucket becomes empty, unlink it.

```python
class Bucket:
    def __init__(self, count):
        self.count = count
        self.keys = set()
        self.prev = self.next = None

class AllOne:
    def __init__(self):
        self.head = Bucket(0)   # sentinel
        self.tail = Bucket(0)   # sentinel
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_to_bucket = {}

    def _insert_after(self, prev, count):
        b = Bucket(count)
        b.prev = prev
        b.next = prev.next
        prev.next.prev = b
        prev.next = b
        return b

    def _remove(self, b):
        b.prev.next = b.next
        b.next.prev = b.prev

    def inc(self, key):
        if key in self.key_to_bucket:
            curr = self.key_to_bucket[key]
            new_count = curr.count + 1
            nxt = curr.next if curr.next.count == new_count else self._insert_after(curr, new_count)
        else:
            nxt = self.head.next if self.head.next.count == 1 else self._insert_after(self.head, 1)
            curr = None
        nxt.keys.add(key)
        self.key_to_bucket[key] = nxt
        if curr:
            curr.keys.discard(key)
            if not curr.keys:
                self._remove(curr)

    def dec(self, key):
        curr = self.key_to_bucket[key]
        new_count = curr.count - 1
        if new_count == 0:
            del self.key_to_bucket[key]
        else:
            prev = curr.prev if curr.prev.count == new_count else self._insert_after(curr.prev, new_count)
            prev.keys.add(key)
            self.key_to_bucket[key] = prev
        curr.keys.discard(key)
        if not curr.keys:
            self._remove(curr)

    def getMaxKey(self):
        return next(iter(self.tail.prev.keys)) if self.tail.prev is not self.head else ""

    def getMinKey(self):
        return next(iter(self.head.next.keys)) if self.head.next is not self.tail else ""
```

Hard. The lesson: when you need O(1) min/max under updates and the values are integer counts, bucket by count and linked-list the buckets.
### Source
LeetCode
