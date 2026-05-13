"""
Debug problem — tree functions (recursion)

Three recursive functions. They look reasonable but tests in test_tree_fns.py fail.
Find and fix.

Hint: 1 bug per function. Two are classic Python footguns; one is a typo-style mistake.
"""

from typing import NamedTuple


class TreeFile(NamedTuple):
    name: str
    size: int


class TreeDir(NamedTuple):
    name: str
    children: tuple


def tree_total_size(node, total=0):
    """Sum of all file sizes under this node."""
    if isinstance(node, TreeFile):
        return node.size
    for c in node.children:
        total += tree_total_size(c, total)
    return total


def tree_find_files(node, min_size, results=[]):
    """Names of files with size >= min_size."""
    if isinstance(node, TreeFile):
        if node.size >= min_size:
            results.append(node.name)
        return results
    for c in node.children:
        tree_find_files(c, min_size, results)
    return results


def _flatten(lst):
    flat = []
    for sublist in lst:
        for item in sublist:
            flat.append(item)
    return flat


def tree_files_at_depth(node, depth):
    """File names at exactly this depth. The input node is depth 0."""
    if isinstance(node, TreeFile):
        return [node.name] if depth == 0 else []
    if depth == 0:
        return []
    # breakpoint()
    return [n for c in node.children for n in tree_files_at_depth(c, depth - 1)]
    # nested = [tree_files_at_depth(c, depth - 1) for c in node.children]
    # return _flatten(nested)
