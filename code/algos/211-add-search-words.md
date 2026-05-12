## Number
211
## Tags
leetcode,design
### Name
Design Add and Search Words Data Structure
### Problem
Support `addWord(word)` and `search(word)`, where `search` may contain `.` as a wildcard that matches any single character.
### Solution
Trie + DFS for the `.` wildcard. Each trie node has a `children` dict and an `is_end` flag.

```python
class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = Node()

    def addWord(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = Node()
            node = node.children[ch]
        node.is_end = True

    def search(self, word):
        def dfs(i, node):
            if i == len(word):
                return node.is_end
            ch = word[i]
            if ch == ".":
                return any(dfs(i + 1, child) for child in node.children.values())
            if ch not in node.children:
                return False
            return dfs(i + 1, node.children[ch])
        return dfs(0, self.root)
```

For a literal character, walk the trie normally. For `.`, recurse into every child. The base case is "consumed the whole word" — check `is_end` to distinguish "this is a real word" from "this is a prefix of one".
### Source
LeetCode
