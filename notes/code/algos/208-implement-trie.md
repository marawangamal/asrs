## Number
208
## Tags
leetcode,design
### Name
Implement Trie (Prefix Tree)
### Problem
Implement a trie supporting `insert(word)`, `search(word)` (exact match), and `startsWith(prefix)`.
### Solution
Tree of nodes, one per character. Each node has a `children` dict and an `is_end` flag distinguishing "this is a complete word" from "this is a prefix".

```python
class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
        node.is_end = True

    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
```

You probably won't be asked to implement a bare trie outright, but the structure shows up inside other problems (autocomplete, file systems, prefix matching, problem 211).
### Source
LeetCode
