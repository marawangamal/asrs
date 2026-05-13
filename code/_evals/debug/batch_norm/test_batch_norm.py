import unittest

import numpy as np

from batch_norm import (
    batch_norm,
    layer_norm,
    running_mean_update,
    standardize_per_channel,
)


class TestBatchNorm(unittest.TestCase):
    def test_columns_have_zero_mean_unit_var(self):
        rng = np.random.RandomState(0)
        x = rng.randn(50, 4) * 3.0 + 7.0
        out = batch_norm(x)
        self.assertEqual(out.shape, (50, 4))
        np.testing.assert_allclose(out.mean(axis=0), np.zeros(4), atol=1e-6)
        np.testing.assert_allclose(out.var(axis=0), np.ones(4), atol=1e-5)


class TestLayerNorm(unittest.TestCase):
    def test_rows_have_zero_mean(self):
        rng = np.random.RandomState(1)
        x = rng.randn(3, 8)
        out = layer_norm(x)
        np.testing.assert_allclose(out.mean(axis=-1), np.zeros(3), atol=1e-6)

    def test_stable_for_constant_row(self):
        # A row with zero variance must not produce NaN.
        x = np.array([[1.0, 1.0, 1.0], [2.0, 4.0, 6.0]])
        out = layer_norm(x)
        self.assertTrue(np.all(np.isfinite(out)))
        np.testing.assert_allclose(out[0], np.zeros(3))


class TestRunningMeanUpdate(unittest.TestCase):
    def test_momentum_one_replaces(self):
        # With m=1.0, output equals batch_mean (running is fully replaced).
        self.assertAlmostEqual(running_mean_update(0.0, 10.0, momentum=1.0), 10.0)

    def test_small_momentum_barely_moves(self):
        # m=0.1 means new = 0.9*old + 0.1*batch
        out = running_mean_update(0.0, 10.0, momentum=0.1)
        self.assertAlmostEqual(out, 1.0)


class TestStandardizePerChannel(unittest.TestCase):
    def test_shape_preserved(self):
        x = np.arange(2 * 3 * 4 * 5, dtype=float).reshape(2, 3, 4, 5)
        mean = np.array([1.0, 2.0, 3.0])
        std = np.array([1.0, 1.0, 1.0])
        out = standardize_per_channel(x, mean, std)
        self.assertEqual(out.shape, (2, 3, 4, 5))

    def test_each_channel_offset_by_its_mean(self):
        x = np.zeros((1, 3, 2, 2))
        mean = np.array([1.0, 2.0, 3.0])
        std = np.ones(3)
        out = standardize_per_channel(x, mean, std)
        np.testing.assert_allclose(out[0, 0], -1.0)
        np.testing.assert_allclose(out[0, 1], -2.0)
        np.testing.assert_allclose(out[0, 2], -3.0)


if __name__ == "__main__":
    unittest.main()
