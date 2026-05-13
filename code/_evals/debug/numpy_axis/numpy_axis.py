"""
Debug problem — NumPy axis and broadcasting

Four small NumPy functions, all subtly wrong. Failure modes range from wrong
values to shape mismatches to outright broadcast crashes.

Hint: 1 bug per function. Every bug is about an axis argument, missing
`keepdims`, or swapped broadcasting dimensions.
"""

import numpy as np


def row_sums(x):
    """Sum each row of a 2D array. Input (N, D), output (N,)."""
    return np.sum(x, axis=-1)


def normalize_rows(x):
    """Scale each row so it sums to 1. Input (N, D), output (N, D)."""
    return x / np.sum(x, axis=1, keepdims=True)


def column_argmax(x):
    """Index of largest value in each column. Output (D,) for input (N, D)."""
    return np.argmax(x, axis=0)


def pairwise_distance_squared(a, b):
    """a: (N, D), b: (M, D). Return (N, M) array of squared Euclidean distances."""
    diff = a[:, None, :] - b[None, :, :]
    return np.sum(diff**2, axis=-1)
