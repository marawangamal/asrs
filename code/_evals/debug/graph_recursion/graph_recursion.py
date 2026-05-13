"""
Debug problem — recursion on graphs

Adjacency-dict graphs: {node: [neighbors, ...]}. Tests in
test_graph_recursion.py fail.

Hint: 1 bug per function. Watch for:
  - mutable default arguments,
  - whether `visited` is shared across the outer DFS loop,
  - the difference between "already visited" and "on the current
    DFS path" when detecting cycles.
"""


def has_path(graph, start, end, visited=None):
    """Return True iff there's a directed path from `start` to `end`."""
    if start == end:
        return True
    if visited is None:
        visited = set()
    visited.add(start)
    for nbr in graph.get(start, []):
        if nbr in visited:
            continue
        if has_path(graph, nbr, end, visited):
            return True
    return False


def count_components(graph):
    """Number of connected components in an undirected graph.
    Assume edges are present in both directions, so every node appears
    as a key.
    """
    count = 0

    def dfs(node, visited):
        visited.add(node)
        for nbr in graph.get(node, []):
            if nbr not in visited:
                dfs(nbr, visited)

    visited = set()
    for start in graph:
        if start not in visited:
            dfs(start, visited)
            count += 1
    return count


def has_cycle(graph):
    """True iff the directed graph contains a cycle."""
    visited = set()

    def dfs(node):
        if node in visited:
            return True
        for nbr in graph.get(node, []):
            visited.add(node)
            if dfs(nbr):
                return True
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    return False
