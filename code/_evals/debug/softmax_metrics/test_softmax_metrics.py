import unittest

import numpy as np

from softmax_metrics import (
    cross_entropy,
    log_softmax,
    softmax,
    top_k_accuracy,
)


class TestSoftmaxMetrics(unittest.TestCase):
    def test_softmax_2d_shape_and_rows_sum_to_one(self):
        x = np.array([[1.0, 2.0, 3.0], [1.0, 1.0, 1.0]])
        out = softmax(x)
        self.assertEqual(out.shape, (2, 3))
        np.testing.assert_allclose(out.sum(axis=-1), [1.0, 1.0])
        np.testing.assert_allclose(out[1], [1 / 3, 1 / 3, 1 / 3])

    def test_softmax_3d(self):
        rng = np.random.RandomState(0)
        x = rng.randn(2, 4, 5)
        out = softmax(x)
        self.assertEqual(out.shape, (2, 4, 5))
        np.testing.assert_allclose(out.sum(axis=-1), np.ones((2, 4)))

    def test_log_softmax_is_stable_for_large_logits(self):
        # Large logits would overflow exp() without subtracting the max first.
        x = np.array([[1000.0, 1000.0, 1001.0]])
        out = log_softmax(x)
        self.assertTrue(np.all(np.isfinite(out)))
        np.testing.assert_allclose(np.exp(out).sum(axis=-1), [1.0])

    def test_cross_entropy(self):
        # Asymmetric logits + non-identity labels so a swapped fancy-index
        # gives a different value.
        logits = np.array(
            [
                [1.0, 2.0, 3.0],
                [1.0, 3.0, 2.0],
                [3.0, 1.0, 2.0],
            ]
        )
        labels = np.array([2, 0, 1])
        # Every row is a permutation of {1,2,3}, so log_sum_exp is the same.
        z = np.log(np.exp(1) + np.exp(2) + np.exp(3))
        # Selected logits: row0[2]=3, row1[0]=1, row2[1]=1.
        expected = -((3 - z) + (1 - z) + (1 - z)) / 3
        self.assertAlmostEqual(cross_entropy(logits, labels), expected, places=6)

    def test_top_k_accuracy(self):
        logits = np.array(
            [
                [0.1, 0.5, 0.4],  # ranking: 1 > 2 > 0
                [0.9, 0.05, 0.6],  # ranking: 0 > 2 > 1
                [0.2, 0.7, 0.1],  # ranking: 1 > 0 > 2
            ]
        )
        labels = np.array([1, 2, 0])
        # top-1 predictions are [1, 0, 1]; only sample 0 matches its label
        self.assertAlmostEqual(top_k_accuracy(logits, labels, 1), 1 / 3)
        # top-2 sets are {1,2}, {0,2}, {1,0}; every label is contained
        self.assertAlmostEqual(top_k_accuracy(logits, labels, 2), 1.0)


if __name__ == "__main__":
    unittest.main()
