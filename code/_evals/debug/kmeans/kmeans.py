"""
Debug problem — K-means clustering

A small K-means implementation. The four functions below look reasonable
but tests in test_kmeans.py fail.

Hint: 3 bugs total — one each in `init_centers`, `assign_labels`, and
`update_centers`. They cover:
  - np.random.RandomState (how `choice` is parameterized)
  - broadcasting / which axis is reduced
  - division by zero when a cluster is empty (use np.where to guard)

`kmeans` itself is fine; it just stitches the three together.
"""

from typing import NamedTuple

import numpy as np


class KMeansResult(NamedTuple):
    centers: np.ndarray  # shape (K, D)
    labels: np.ndarray   # shape (N,)
    n_iter: int


def init_centers(X, k, seed=0):
    """Initialize centers by picking `k` distinct rows of `X` uniformly
    at random. Returns a (k, D) float array (a copy)."""
    rng = np.random.RandomState(seed)
    n = X.shape[0]
    idx = rng.choice(n, size=k, replace=True)
    return X[idx].copy().astype(float)


def assign_labels(X, centers):
    """Assign each row of X to its nearest center under squared L2.

    X: (N, D), centers: (K, D). Returns (N,) int labels in [0, K).
    """
    diff = X[:, None, :] - centers[None, :, :]  # (N, K, D)
    sq_dist = (diff ** 2).sum(axis=-1)          # (N, K)
    return np.argmin(sq_dist, axis=0)


def update_centers(X, labels, k):
    """Recompute each center as the mean of its assigned rows of X.

    For empty clusters (no assigned points), the center should be all zeros.
    Returns a (k, D) float array.
    """
    n, d = X.shape
    counts = np.bincount(labels, minlength=k).astype(float)  # (k,)
    sums = np.zeros((k, d))
    for c in range(k):
        sums[c] = X[labels == c].sum(axis=0)
    return sums / counts[:, None]


def kmeans(X, k, n_iter, seed=0):
    """Run `n_iter` rounds of Lloyd's algorithm. Returns a KMeansResult
    whose `labels` are consistent with the returned `centers`, i.e.
    labels == assign_labels(X, centers).
    """
    centers = init_centers(X, k, seed=seed)
    for _ in range(n_iter):
        labels = assign_labels(X, centers)
        centers = update_centers(X, labels, k)
    return KMeansResult(centers=centers, labels=labels, n_iter=n_iter)
