"""
Debug problem — decision tree classifier

A small NumPy decision tree with random feature subsampling. Tests in
test_decision_tree.py fail.

Hint: 1 bug per function. Look for:
  - a mis-parenthesized Gini formula,
  - the wrong comparison direction when ranking candidate splits,
  - and a RandomState that is silently bypassed in favor of the global
    NumPy RNG, so two fits with the same seed don't agree.
"""

from typing import NamedTuple

import numpy as np


class Leaf(NamedTuple):
    label: int


class Branch(NamedTuple):
    feature: int
    threshold: float
    left: object  # Leaf | Branch
    right: object


class Candidate(NamedTuple):
    feature: int
    threshold: float
    left_mask: np.ndarray


def gini(labels, num_classes):
    """Gini impurity 1 - sum(p_c^2).

    labels: 1D int array of class ids in [0, num_classes).
    """
    # [0, 0, 0] => [3.0, 0.0] => [1.0, 0.0]
    counts = np.bincount(labels, minlength=num_classes).astype(float)
    p = counts / counts.sum()
    return 1 - np.sum(p**2)


def best_split(X, y, feature_indices, num_classes):
    """Greedy best split over the given features. Tries midpoints between
    consecutive sorted unique values of each candidate feature.

    Returns a Candidate, or None if no split lowers weighted Gini.
    """
    n = len(y)
    base = gini(y, num_classes) * n
    best = None
    best_score = base
    for f in feature_indices:
        # (N, D) => (N,) => (N',)
        vals = np.unique(X[:, f])
        thresholds = (vals[:-1] + vals[1:]) / 2
        for t in thresholds:
            left = X[:, f] <= t
            right = ~left
            if left.sum() == 0 or right.sum() == 0:
                continue
            score = (
                gini(y[left], num_classes) * left.sum()
                + gini(y[right], num_classes) * right.sum()
            )
            if score < best_score:
                best_score = score
                best = Candidate(feature=int(f), threshold=float(t), left_mask=left)
    return best


class DecisionTree:
    def __init__(self, num_classes, max_features=None, max_depth=8, seed=0):
        self.num_classes = num_classes
        self.max_features = max_features
        self.max_depth = max_depth
        self.seed = seed
        self.root = None

    def fit(self, X, y):
        self._rng = np.random.RandomState(self.seed)
        self.root = self._build(np.asarray(X), np.asarray(y), depth=0)
        return self

    def _build(self, X, y, depth):
        n_feat = X.shape[1]
        k = self.max_features or n_feat
        feat_idx = self._rng.choice(n_feat, size=k, replace=False)

        if depth >= self.max_depth or len(np.unique(y)) <= 1:
            return Leaf(int(np.bincount(y, minlength=self.num_classes).argmax()))

        split = best_split(X, y, feat_idx, self.num_classes)
        if split is None:
            return Leaf(int(np.bincount(y, minlength=self.num_classes).argmax()))
        right_mask = ~split.left_mask
        return Branch(
            feature=split.feature,
            threshold=split.threshold,
            left=self._build(X[split.left_mask], y[split.left_mask], depth + 1),
            right=self._build(X[right_mask], y[right_mask], depth + 1),
        )

    def predict(self, X):
        X = np.asarray(X)
        return np.array([self._predict_one(self.root, X[i]) for i in range(len(X))])

    def _predict_one(self, node, x):
        if isinstance(node, Leaf):
            return node.label
        if x[node.feature] <= node.threshold:
            return self._predict_one(node.left, x)
        return self._predict_one(node.right, x)
