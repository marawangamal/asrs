"""
Debug problem — regression metrics

MAE, R^2, and per-class MSE over a batch. Tests in
test_regression_metrics.py fail.

Hint: 1 bug per function. Look for:
  - the right reduction axis on a (N, T) array,
  - which mean R^2 actually uses for SS_tot,
  - the division-by-zero you get from np.bincount when a class is empty.
"""

import numpy as np


def per_target_mae(y_true, y_pred):
    """Mean absolute error per target column.

    y_true, y_pred: (N, T). Returns shape (T,).
    """
    return np.mean(np.abs(y_true - y_pred), axis=-1)


def r_squared(y_true, y_pred):
    """Coefficient of determination R^2 = 1 - SS_res / SS_tot.

    y_true, y_pred: 1D arrays of the same length.
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_pred)) ** 2)
    return 1 - ss_res / ss_tot


def per_class_mse(classes, y_true, y_pred, num_classes):
    """Per-class mean squared error.

    classes: (N,) int class ids in [0, num_classes).
    y_true, y_pred: (N,) floats.
    Returns a (num_classes,) array; classes with no samples map to 0.
    """
    sq = (y_true - y_pred) ** 2
    sums = np.bincount(classes, weights=sq, minlength=num_classes)
    counts = np.bincount(classes, minlength=num_classes)
    return sums / counts
