## Number
146
## Tags
leetcode,design
### Name
LRU Cache
### Problem
Design a cache with fixed capacity supporting `get(key)` and `put(key, value)` in O(1) average time. When capacity is exceeded, evict the least recently used key.
### Solution
The canonical "two data structures working together" problem: a hash map gives O(1) lookup, a doubly linked list gives O(1) reordering. Map keys to nodes; on every access, move the node to the head (MRU); on overflow, evict the node at the tail (LRU). Use dummy head/tail sentinels to remove every "empty list" / "single element" special case.

For a timed test, `collections.OrderedDict` does this for you:

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap:
            self.cache.popitem(last=False)
```

Hand-rolled version (worth doing once for fluency):

```python
class Node:
    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.map = {}
        self.head = Node()  # sentinel: head.next is MRU
        self.tail = Node()  # sentinel: tail.prev is LRU
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node):
        self._remove(node)
        self._add_to_head(node)

    def get(self, key):
        if key not in self.map:
            return -1
        node = self.map[key]
        self._move_to_head(node)
        return node.value

    def put(self, key, value):
        if key in self.map:
            node = self.map[key]
            node.value = value
            self._move_to_head(node)
            return
        node = Node(key, value)
        self.map[key] = node
        self._add_to_head(node)
        if len(self.map) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
```

Key gotchas: Node must store the key (so eviction can delete from the map); sentinels eliminate null checks; the order of the four pointer assignments in `_add_to_head` matters.
### Source
LeetCode
