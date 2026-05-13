"""
Debug problem — softmax & classification metrics

Common neural-net helpers. The code looks plausible but tests in
test_softmax_metrics.py fail. Read carefully, run the tests, fix the
root cause. Do not rewrite from scratch.

Hint: 1 bug per function. Look for: missing keepdims, missing
numerical-stability trick, swapped fancy-indexing axes, and which end
of `np.argsort` actually holds the "top" values.
"""

import numpy as np


def softmax(logits):
    """Stable softmax over the last axis. Input shape (..., C)."""
    shifted = logits - np.max(logits, axis=-1, keepdims=True)
    exp = np.exp(shifted)
    return exp / np.sum(exp, axis=-1, keepdims=True)


def log_softmax(logits):
    """Stable log-softmax over the last axis. Input shape (..., C)."""
    M = np.max(logits, axis=-1, keepdims=True)
    return logits - M - np.log(np.sum(np.exp(logits - M), axis=-1, keepdims=True))


def cross_entropy(logits, labels):
    """Mean cross-entropy over a batch.

    logits: (N, C) unnormalized scores.
    labels: (N,) int class indices in [0, C).
    Returns a scalar.
    """
    log_probs = log_softmax(logits)
    n = logits.shape[0]
    return -np.mean(log_probs[np.arange(n), labels])


def top_k_accuracy(logits, labels, k):
    """Fraction of samples whose true label is among the model's top-k predictions.

    logits: (N, C), labels: (N,) int.
    """
    sorted_idx = np.argsort(logits, axis=-1)
    topk = sorted_idx[:, -k:]  # (N, K)
    return np.mean(np.any(topk == labels[:, None], axis=-1))
