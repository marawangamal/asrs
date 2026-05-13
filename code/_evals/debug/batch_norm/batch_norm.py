"""
Debug problem — batch / layer norm

NumPy broadcasting on the batch and channel axes. Tests in
test_batch_norm.py fail. Read carefully, fix the root cause.
Do not rewrite from scratch.

Hint: 1 bug per function. Look for: which axis the normalization
reduces over, a missing numerical-stability trick, a swapped
momentum update, and a broadcasting shape mismatch on a channel
axis.
"""

import numpy as np


def batch_norm(x, eps=1e-5):
    """Batch norm over the batch axis. x: (N, D). Each output column
    has zero mean and unit variance over the N samples in that column.
    """
    mean = x.mean(axis=0, keepdims=True)
    var = x.var(axis=0, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)


def layer_norm(x, eps=1e-5):
    """Layer norm over the feature axis. x: (N, D). Each row has zero
    mean and unit variance over its D features.
    """
    mean = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return (x - mean) / np.sqrt(var + eps)


def running_mean_update(running, batch_mean, momentum):
    """Update a running average. Convention:
        new_running = (1 - momentum) * running + momentum * batch_mean.
    Higher momentum -> faster adaptation to the new batch.
    """
    return (1 - momentum) * running + momentum * batch_mean


def standardize_per_channel(x, mean, std):
    """Subtract per-channel mean, divide by per-channel std.

    x: (N, C, H, W). mean, std: (C,). Returns (N, C, H, W).
    """
    targ_shape = (1, mean.shape[0], 1, 1)
    return (x - mean.reshape(*targ_shape)) / std.reshape(*targ_shape)
