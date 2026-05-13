import unittest

import numpy as np

from numpy_axis import (
    column_argmax,
    normalize_rows,
    pairwise_distance_squared,
    row_sums,
)


class TestNumpyDebug(unittest.TestCase):
    def test_row_sums(self):
        x = np.array([[1, 2, 3], [4, 5, 6]])
        np.testing.assert_array_equal(row_sums(x), [6, 15])

    def test_normalize_rows(self):
        x = np.array([[1.0, 1.0, 2.0], [4.0, 4.0, 2.0]])
        out = normalize_rows(x)
        np.testing.assert_allclose(out.sum(axis=1), [1.0, 1.0])
        np.testing.assert_allclose(out[0], [0.25, 0.25, 0.5])

    def test_column_argmax(self):
        x = np.array([[1, 2, 9], [4, 5, 6], [7, 8, 3]])
        np.testing.assert_array_equal(column_argmax(x), [2, 2, 0])

    def test_pairwise_distance_shape(self):
        a = np.array([[0.0, 0.0], [1.0, 0.0]])  # (2, 2)
        b = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # (3, 2)
        d = pairwise_distance_squared(a, b)
        self.assertEqual(d.shape, (2, 3))

    def test_pairwise_distance_values(self):
        a = np.array([[0.0, 0.0], [1.0, 0.0]])
        b = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
        d = pairwise_distance_squared(a, b)
        np.testing.assert_allclose(d, [[0, 1, 2], [1, 2, 1]])


if __name__ == "__main__":
    unittest.main()
