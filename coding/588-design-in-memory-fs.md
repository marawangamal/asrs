## Number
588
## Tags
leetcode,design
### Name
Design In-Memory File System
### Problem
Implement `ls(path)`, `mkdir(path)`, `addContentToFile(filePath, content)`, and `readContentFromFile(filePath)`. `ls` on a directory returns lexicographically sorted children; on a file, just the file name.
### Solution
A trie of nodes. Each node has a `children` dict (`name -> Node`) and optionally `content` (string). File vs directory is implicit from which field is populated.

```python
class Node:
    def __init__(self):
        self.children = {}      # name -> Node
        self.content = None     # None means directory; string means file

class FileSystem:
    def __init__(self):
        self.root = Node()

    def _walk(self, path, create=False):
        node = self.root
        if path == "/":
            return node
        for part in path.split("/")[1:]:
            if part not in node.children:
                if not create:
                    return None
                node.children[part] = Node()
            node = node.children[part]
        return node

    def ls(self, path):
        node = self._walk(path)
        if node.content is not None:
            return [path.split("/")[-1]]
        return sorted(node.children.keys())

    def mkdir(self, path):
        self._walk(path, create=True)

    def addContentToFile(self, filePath, content):
        node = self._walk(filePath, create=True)
        if node.content is None:
            node.content = ""
        node.content += content

    def readContentFromFile(self, filePath):
        return self._walk(filePath).content
```

Gotchas:
- `path.split("/")` produces a leading empty string for absolute paths; skip with `[1:]`.
- Use a `dict` for children (not `defaultdict(list)` + append) so repeated `mkdir` doesn't create duplicates.
- Sort on `ls` queries, not on insert — simpler and fast enough.
- `ls` on a file returns the basename only (`path.split("/")[-1]`), not the full path.
### Source
LeetCode
