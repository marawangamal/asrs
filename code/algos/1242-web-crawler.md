## Number
1242
## Tags
leetcode,design,concurrency
### Name
Web Crawler Multithreaded
### Problem
Given a `startUrl` and an `HtmlParser` with `getUrls(url)`, crawl all URLs reachable from `startUrl` that share the same hostname. Must be parallelized.
### Solution
Single-threaded version is a standard BFS with a visited set, filtering by hostname:

```python
from collections import deque
from urllib.parse import urlparse

class Solution:
    def crawl(self, startUrl, htmlParser):
        host = urlparse(startUrl).hostname
        visited = {startUrl}
        queue = deque([startUrl])
        while queue:
            url = queue.popleft()
            for nxt in htmlParser.getUrls(url):
                if nxt not in visited and urlparse(nxt).hostname == host:
                    visited.add(nxt)
                    queue.append(nxt)
        return list(visited)
```

Multithreaded version uses `ThreadPoolExecutor` and `as_completed`. Submit each `getUrls` call as a future; drain completed futures and submit new ones for newly discovered same-host URLs.

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

class Solution:
    def crawl(self, startUrl, htmlParser):
        host = urlparse(startUrl).hostname
        visited = {startUrl}

        with ThreadPoolExecutor(max_workers=16) as ex:
            futures = {ex.submit(htmlParser.getUrls, startUrl)}
            while futures:
                done, futures = set(), futures
                for f in as_completed(list(futures)):
                    futures.discard(f)
                    for nxt in f.result():
                        if nxt not in visited and urlparse(nxt).hostname == host:
                            visited.add(nxt)
                            futures.add(ex.submit(htmlParser.getUrls, nxt))
                    break  # re-enter loop to add newly-submitted futures
        return list(visited)
```

This problem was asked in an Anthropic virtual onsite (the candidate was asked for both single- and multi-threaded versions). It's the closest LeetCode problem in spirit to what real concurrency screens ask: a bounded worker pool doing concurrent traversal with shared state (the visited set).
### Source
LeetCode + Anthropic VO Q1
