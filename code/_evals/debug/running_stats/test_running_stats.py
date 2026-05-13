import unittest

from running_stats import RunningStats


class TestRunningStats(unittest.TestCase):
    def test_count_empty(self):
        s = RunningStats()
        self.assertEqual(s.count(), 0)

    def test_mean(self):
        s = RunningStats()
        for x in [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]:
            s.add(x)
        self.assertAlmostEqual(s.mean(), 5.0)
        self.assertEqual(s.count(), 8)

    def test_variance_sample(self):
        # Sample variance of [2,4,4,4,5,5,7,9] is 32/7
        s = RunningStats()
        for x in [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]:
            s.add(x)
        self.assertAlmostEqual(s.variance(), 32 / 7)

    def test_min_all_positive(self):
        s = RunningStats()
        for x in [5.0, 3.0, 8.0, 2.0, 7.0]:
            s.add(x)
        self.assertAlmostEqual(s.min(), 2.0)

    def test_max_all_negative(self):
        s = RunningStats()
        for x in [-5.0, -3.0, -8.0, -2.0, -7.0]:
            s.add(x)
        self.assertAlmostEqual(s.max(), -2.0)


if __name__ == "__main__":
    unittest.main()
