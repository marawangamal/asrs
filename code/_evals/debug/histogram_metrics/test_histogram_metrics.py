import unittest

import numpy as np

from histogram_metrics import (
    classes_present,
    clip_to_range,
    confusion_matrix,
    per_class_recall,
)


class TestHistogramMetrics(unittest.TestCase):
    def test_confusion_matrix_basic(self):
        # No (true=2, pred=2) pair exists, so the largest used index is < C*C - 1.
        y_true = np.array([0, 0, 1, 2])
        y_pred = np.array([0, 1, 1, 0])
        cm = confusion_matrix(y_true, y_pred, 3)
        expected = np.array(
            [
                [1, 1, 0],
                [0, 1, 0],
                [1, 0, 0],
            ]
        )
        np.testing.assert_array_equal(cm, expected)

    def test_confusion_matrix_shape(self):
        # Even when no class appears at all, the shape must be (C, C).
        y_true = np.array([0, 0])
        y_pred = np.array([0, 0])
        self.assertEqual(confusion_matrix(y_true, y_pred, 4).shape, (4, 4))

    def test_per_class_recall(self):
        # True totals per class: 3, 2, 1.  Diag (TPs): 2, 1, 1.
        y_true = np.array([0, 0, 0, 1, 1, 2])
        y_pred = np.array([0, 0, 1, 1, 2, 2])
        expected = np.array([2 / 3, 1 / 2, 1.0])
        np.testing.assert_allclose(per_class_recall(y_true, y_pred, 3), expected)

    def test_per_class_recall_absent_class(self):
        y_true = np.array([0, 0, 1])
        y_pred = np.array([0, 1, 1])
        # Class 2 never appears in y_true → recall is 0 by convention.
        np.testing.assert_allclose(per_class_recall(y_true, y_pred, 3), [0.5, 1.0, 0.0])

    def test_classes_present(self):
        labels = np.array([1, 2, 0, 2, 5, 0, 1])
        np.testing.assert_array_equal(classes_present(labels), [1, 2, 5])

    def test_classes_present_all_zero(self):
        labels = np.array([0, 0, 0])
        np.testing.assert_array_equal(classes_present(labels), [])

    def test_clip_to_range(self):
        x = np.array([-1.0, 0.5, 2.0, 5.0, -3.0])
        np.testing.assert_array_equal(
            clip_to_range(x, 0.0, 3.0), [0.0, 0.5, 2.0, 3.0, 0.0]
        )


if __name__ == "__main__":
    unittest.main()
