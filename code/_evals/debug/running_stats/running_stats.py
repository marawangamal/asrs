"""
Debug problem — RunningStats

The code below looks correct but has bugs — the tests in test_running_stats.py fail.
Read carefully, run the tests, fix the root cause. Do not rewrite from scratch.

`RunningStats` tracks running statistics over a stream of floats added one at a time.
- add(x)       — add a value
- mean()       — current mean
- variance()   — sample variance (denominator n-1)
- min(), max() — running min/max
- count()      — number of values added

Hint: 2 bugs, in different methods.
"""


class RunningStats:
    def __init__(self):
        self.n = 0
        self.mean_val = 0.0
        self.m2 = 0.0
        self.min_val = 0.0
        self.max_val = 0.0

    def add(self, x):
        self.n += 1
        delta = x - self.mean_val
        self.mean_val += delta / self.n
        delta2 = x - self.mean_val
        self.m2 += delta * delta2
        if x < self.min_val:
            self.min_val = x
        if x > self.max_val:
            self.max_val = x

    def mean(self):
        return self.mean_val

    def variance(self):
        if self.n < 2:
            return 0.0
        return self.m2 / self.n

    def min(self):
        return self.min_val

    def max(self):
        return self.max_val

    def count(self):
        return self.n
