import unittest

import numpy as np

from decision_tree import DecisionTree, best_split, gini


class TestGini(unittest.TestCase):
    def test_pure(self):
        # All one class -> impurity 0.
        self.assertAlmostEqual(gini(np.array([0, 0, 0]), 2), 0.0)

    def test_balanced_two_class(self):
        # 1 - (0.5^2 + 0.5^2) = 0.5
        self.assertAlmostEqual(gini(np.array([0, 0, 1, 1]), 2), 0.5)

    def test_three_class_uniform(self):
        # 1 - 3 * (1/3)^2 = 2/3
        self.assertAlmostEqual(gini(np.array([0, 1, 2]), 3), 2 / 3)


class TestBestSplit(unittest.TestCase):
    def test_finds_split_on_separable_1d(self):
        X = np.array([[0.0], [1.0], [2.0], [3.0]])
        y = np.array([0, 0, 1, 1])
        s = best_split(X, y, [0], num_classes=2)
        self.assertIsNotNone(s)
        self.assertEqual(s.feature, 0)
        self.assertTrue(1.0 < s.threshold < 2.0)

    def test_no_improvement_returns_none(self):
        # All same label -> no split can improve.
        X = np.array([[0.0], [1.0], [2.0]])
        y = np.array([1, 1, 1])
        self.assertIsNone(best_split(X, y, [0], num_classes=2))


class TestDecisionTree(unittest.TestCase):
    def test_fit_predict_separable(self):
        rng = np.random.RandomState(0)
        X = rng.randn(60, 2)
        y = (X[:, 0] > 0).astype(int)
        tree = DecisionTree(num_classes=2, max_depth=4, seed=0).fit(X, y)
        preds = tree.predict(X)
        self.assertGreaterEqual((preds == y).mean(), 0.95)

    def test_predictions_deterministic_across_two_fits(self):
        # Two trees with the same seed, fit on the same data, must agree —
        # even when the global NumPy RNG state has advanced between fits.
        # Predict on held-out points so different tree topologies surface
        # as different predictions (the training set memorizes either way).
        rng = np.random.RandomState(0)
        X = rng.randn(80, 4)
        y = (X[:, 0] + X[:, 1] > 0).astype(int)
        X_test = rng.randn(200, 4)

        t1 = DecisionTree(num_classes=2, max_features=2, max_depth=3, seed=42).fit(X, y)
        _ = np.random.rand(100)  # perturb the global NumPy RNG between fits
        t2 = DecisionTree(num_classes=2, max_features=2, max_depth=3, seed=42).fit(X, y)

        np.testing.assert_array_equal(t1.predict(X_test), t2.predict(X_test))


if __name__ == "__main__":
    unittest.main()
