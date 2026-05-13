"""
Debug problem — histogram-based classification metrics

Compute confusion matrices and per-class metrics from integer-labeled
data. Tests in test_histogram_metrics.py fail.

Hint: 1 bug per function. The bugs cover np.bincount's `minlength`,
which axis to sum a confusion matrix over, what np.nonzero actually
returns, and the argument order of np.where.

Note: `per_class_recall` calls `confusion_matrix` internally, so its
test will also fail until `confusion_matrix` is fixed first.
"""

import numpy as np


def confusion_matrix(y_true, y_pred, num_classes):
    """Return a (C, C) confusion matrix where M[i, j] is the number of
    samples with true class i and predicted class j.

    y_true, y_pred: 1D integer arrays of class indices in [0, C).
    """
    # C=3
    # [0, 1], [0, 0] =mult+sum=> [0, 2, 0, 0] =bincount=> [3, 0, 1]
    idx = y_true * num_classes + y_pred
    counts = np.bincount(idx, minlength=num_classes**2)
    return counts.reshape(num_classes, num_classes)


def per_class_recall(y_true, y_pred, num_classes):
    """Per-class recall = TP / (TP + FN). Returns a (C,) array.

    Classes that never appear in y_true should map to 0.0.
    """
    cm = confusion_matrix(y_true, y_pred, num_classes)
    tp = np.diag(cm)
    totals = cm.sum(axis=1)
    return np.where(totals > 0, tp / np.maximum(totals, 1), 0.0)


def classes_present(labels):
    """Return the sorted distinct *positive* class values that appear in
    `labels`. Class 0 is treated as "absent" and excluded.

    Example: classes_present([1, 2, 0, 2, 5]) -> array([1, 2, 5]).
    """
    ids = np.nonzero(labels)[0]
    return sorted(list(set(labels[ids])))


def clip_to_range(x, lo, hi):
    """Element-wise clip: values below `lo` become `lo`, values above
    `hi` become `hi`. Returns a new array.
    """
    x = np.where(x < lo, lo, x)
    x = np.where(x > hi, hi, x)
    return x
