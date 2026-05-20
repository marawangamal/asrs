## Number
1166
## Tags
leetcode,design
### Name
Design File System
### Problem
Support `createPath(path, value)` (creates a path if its parent exists and the path doesn't) and `get(path)` (returns the value, or -1 if missing).
### Solution
The API only requires exact-path lookup and parent-existence check — no traversal — so a flat `dict[path -> value]` is enough. Don't build a tree if you don't need traversal.

```python
class FileSystem:
    def __init__(self):
        self.paths = {}

    def createPath(self, path, value):
        if path == "/" or path in self.paths:
            return False
        parent = path[:path.rfind("/")]
        if parent and parent not in self.paths:
            return False
        self.paths[path] = value
        return True

    def get(self, path):
        return self.paths.get(path, -1)
```

Key gotcha: the parent of `/a` is `""` (empty string), **not** `"/"`. `path[:path.rfind("/")]` correctly produces `""` for `/a` and `/a` for `/a/b`. Avoid `os.path.dirname` — its platform-specific semantics aren't guaranteed to match the problem's path semantics.

Switch to a trie/tree structure (see problem 588) only if `ls`, child enumeration, or subtree rename is also required.
### Source
LeetCode
