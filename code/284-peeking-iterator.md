## Number
284
## Tags
leetcode,design
### Name
Peeking Iterator
### Problem
Given an existing iterator with `next()` and `hasNext()`, design a wrapper that also supports `peek()` — returns the next element without advancing.
### Solution
Cache one element ahead. On construction (and after every `next`), pull the next element from the underlying iterator and stash it.

```python
class PeekingIterator:
    def __init__(self, iterator):
        self.it = iterator
        self._peeked = self.it.next() if self.it.hasNext() else None
        self._has = self._peeked is not None or self.it.hasNext()

    def peek(self):
        return self._peeked

    def next(self):
        val = self._peeked
        if self.it.hasNext():
            self._peeked = self.it.next()
        else:
            self._peeked = None
            self._has = False
        return val

    def hasNext(self):
        return self._peeked is not None or self._has
```

The "cache one element ahead" pattern is the general approach for adding `peek` to any forward-only iterator. Same idea applies to lookahead parsers.
### Source
LeetCode
