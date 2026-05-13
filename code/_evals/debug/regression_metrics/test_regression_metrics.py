import unittest

import numpy as np

from regression_metrics import per_class_mse, per_target_mae, r_squared


class TestPerTargetMAE(unittest.TestCase):
    def test_shape(self):
        y_true = np.zeros((5, 3))
        y_pred = np.ones((5, 3))
        out = per_target_mae(y_true, y_pred)
        self.assertEqual(out.shape, (3,))

    def test_values(self):
        # Column 0 perfect, column 1 off by 2 everywhere, column 2 off by 0.5 avg.
        y_true = np.array(
            [
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
                [0.0, 0.0, 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        y_pred = np.array(
            [
                [0.0, 2.0, 0.0],
                [0.0, 2.0, 0.0],
                [0.0, 2.0, 0.0],
                [0.0, 2.0, 0.0],
            ]
        )
        np.testing.assert_allclose(per_target_mae(y_true, y_pred), [0.0, 2.0, 0.5])


class TestRSquared(unittest.TestCase):
    def test_perfect(self):
        y = np.array([1.0, 2.0, 3.0])
        self.assertAlmostEqual(r_squared(y, y), 1.0)

    def test_known(self):
        y_true = np.array([1.0, 2.0, 3.0])
        # SS_res = 3 * 0.5^2 = 0.75; SS_tot (around mean(y_true)=2) = 2.
        # R^2 = 1 - 0.75 / 2 = 0.625.
        y_pred = np.array([1.5, 2.5, 3.5])
        self.assertAlmostEqual(r_squared(y_true, y_pred), 0.625)


class TestPerClassMSE(unittest.TestCase):
    def test_basic(self):
        classes = np.array([0, 0, 1, 1])
        y_true = np.array([1.0, 2.0, 3.0, 4.0])
        y_pred = np.array([1.0, 4.0, 3.0, 6.0])
        # Class 0: sq errors [0, 4], mean 2.  Class 1: sq errors [0, 4], mean 2.
        np.testing.assert_allclose(
            per_class_mse(classes, y_true, y_pred, 2), [2.0, 2.0]
        )

    def test_empty_class_is_zero(self):
        # Class 1 has no samples — must return 0, not NaN.
        classes = np.array([0, 0])
        y_true = np.array([1.0, 2.0])
        y_pred = np.array([1.0, 2.0])
        np.testing.assert_allclose(
            per_class_mse(classes, y_true, y_pred, 2), [0.0, 0.0]
        )


if __name__ == "__main__":
    unittest.main()
