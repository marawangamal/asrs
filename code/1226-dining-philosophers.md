## Number
1226
## Tags
leetcode,design,concurrency
### Name
The Dining Philosophers
### Problem
Five philosophers around a table, five forks between them. Each must pick up both their left and right fork to eat. Design a discipline that prevents starvation and deadlock.
### Solution
**Resource ordering** is the canonical answer: always acquire the lower-numbered fork first. This breaks circular wait — the cycle "everyone holds one fork and waits for the next" can't form when no thread ever holds a higher-numbered fork while waiting for a lower-numbered one.

```python
from threading import Lock

class DiningPhilosophers:
    def __init__(self):
        self.forks = [Lock() for _ in range(5)]

    def wantsToEat(self, philosopher, pickLeft, pickRight, eat, putLeft, putRight):
        left = philosopher
        right = (philosopher + 1) % 5
        first, second = sorted([left, right])
        with self.forks[first], self.forks[second]:
            pickLeft()
            pickRight()
            eat()
            putLeft()
            putRight()
```

Alternative — limit concurrent diners with a semaphore (breaks "hold and wait" by capping how many can hold any fork at once):

```python
from threading import Lock, Semaphore

class DiningPhilosophers:
    def __init__(self):
        self.forks = [Lock() for _ in range(5)]
        self.diners = Semaphore(4)

    def wantsToEat(self, philosopher, pickLeft, pickRight, eat, putLeft, putRight):
        left, right = philosopher, (philosopher + 1) % 5
        with self.diners, self.forks[left], self.forks[right]:
            pickLeft(); pickRight(); eat(); putLeft(); putRight()
```

**The general principle:** if multiple threads need multiple locks, always acquire them in a globally consistent order. Sort by some stable identifier. This rule eliminates an entire class of deadlock bugs.
### Source
LeetCode
