import unittest

import numpy as np

from kmeans import (
    KMeansResult,
    assign_labels,
    init_centers,
    kmeans,
    update_centers,
)


class TestKMeans(unittest.TestCase):
    def test_init_centers_shape(self):
        X = np.arange(20, dtype=float).reshape(10, 2)
        c = init_centers(X, k=4, seed=0)
        self.assertEqual(c.shape, (4, 2))

    def test_init_centers_no_replacement(self):
        # Picking k > n distinct rows is impossible — should raise.
        X = np.arange(5, dtype=float).reshape(5, 1)
        with self.assertRaises(ValueError):
            init_centers(X, k=10, seed=0)

    def test_assign_labels(self):
        X = np.array(
            [
                [0.0, 0.0],
                [10.0, 10.0],
                [0.1, 0.0],
                [9.0, 11.0],
            ]
        )
        centers = np.array([[0.0, 0.0], [10.0, 10.0]])
        labels = assign_labels(X, centers)
        self.assertEqual(labels.shape, (4,))
        np.testing.assert_array_equal(labels, [0, 1, 0, 1])

    def test_update_centers_means(self):
        X = np.array(
            [
                [0.0, 0.0],
                [2.0, 0.0],
                [0.0, 4.0],
                [0.0, 6.0],
            ]
        )
        labels = np.array([0, 0, 1, 1])
        centers = update_centers(X, labels, k=2)
        np.testing.assert_allclose(centers, [[1.0, 0.0], [0.0, 5.0]])

    def test_update_centers_empty_cluster_stays_zero(self):
        X = np.array([[0.0, 0.0], [2.0, 0.0]])
        labels = np.array([0, 0])
        centers = update_centers(X, labels, k=2)
        # Cluster 1 has no members → center should be all zeros, not NaN.
        np.testing.assert_allclose(centers, [[1.0, 0.0], [0.0, 0.0]])

    def test_kmeans_returns_consistent_labels(self):
        # Three well-separated clusters; after enough iterations, labels
        # must be the argmin of distances to the returned centers.
        rng = np.random.RandomState(42)
        a = rng.randn(30, 2) + np.array([0.0, 0.0])
        b = rng.randn(30, 2) + np.array([10.0, 0.0])
        c = rng.randn(30, 2) + np.array([5.0, 10.0])
        X = np.vstack([a, b, c])

        result = kmeans(X, k=3, n_iter=20, seed=0)
        self.assertIsInstance(result, KMeansResult)
        self.assertEqual(result.centers.shape, (3, 2))
        self.assertEqual(result.labels.shape, (90,))
        self.assertEqual(result.n_iter, 20)

        consistent_labels = np.argmin(
            ((X[:, None, :] - result.centers[None, :, :]) ** 2).sum(axis=-1),
            axis=1,
        )
        np.testing.assert_array_equal(result.labels, consistent_labels)

        # All points from the same input cluster should land in one output cluster.
        for start in (0, 30, 60):
            self.assertEqual(len(np.unique(result.labels[start : start + 30])), 1)


if __name__ == "__main__":
    unittest.main()
