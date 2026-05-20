## Number
460
## Tags
leetcode,design
### Name
LFU Cache
### Problem
Like LRU (146), but on overflow, evict the *least frequently used* key. Ties on frequency break to LRU within that frequency.
### Solution
LRU's harder cousin. Two hash maps + a dict of doubly linked lists, one list per frequency bucket. Track the current minimum frequency.

The structure:
- `key_to_node`: key -> Node (with `key`, `val`, `freq`)
- `freq_to_list`: freq -> doubly linked list of nodes at that frequency
- `min_freq`: the smallest frequency currently in use

On `get`/`put` of an existing key: remove from its current freq list, increment freq, add to the new freq list. If the old list at `min_freq` is now empty and it was at `min_freq`, increment `min_freq`. On eviction: remove the tail of `freq_to_list[min_freq]`.

```python
from collections import OrderedDict, defaultdict

class LFUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.min_freq = 0
        self.key_to_val = {}
        self.key_to_freq = {}
        self.freq_to_keys = defaultdict(OrderedDict)  # ordered for LRU tiebreak

    def _touch(self, key):
        f = self.key_to_freq[key]
        del self.freq_to_keys[f][key]
        if not self.freq_to_keys[f]:
            del self.freq_to_keys[f]
            if self.min_freq == f:
                self.min_freq = f + 1
        self.key_to_freq[key] = f + 1
        self.freq_to_keys[f + 1][key] = None

    def get(self, key):
        if key not in self.key_to_val:
            return -1
        self._touch(key)
        return self.key_to_val[key]

    def put(self, key, value):
        if self.cap == 0:
            return
        if key in self.key_to_val:
            self.key_to_val[key] = value
            self._touch(key)
            return
        if len(self.key_to_val) >= self.cap:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val[evict_key]
            del self.key_to_freq[evict_key]
        self.key_to_val[key] = value
        self.key_to_freq[key] = 1
        self.freq_to_keys[1][key] = None
        self.min_freq = 1
```

Genuinely hard — only worth grinding if you've already internalized 146 and want to push further.
### Source
LeetCode
