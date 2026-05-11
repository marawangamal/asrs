## Number
1117
## Tags
leetcode,design,concurrency
### Name
Building H2O
### Problem
Threads representing H and O atoms call `hydrogen()` or `oxygen()`. They must group themselves into water molecules: 2 H + 1 O proceed together; no H or O may continue past its bonding point until a full molecule is assembled.
### Solution
Use a `Barrier(3)` for the per-molecule sync, plus two semaphores to gate how many H's and O's can enter at a time.

```python
from threading import Semaphore, Barrier

class H2O:
    def __init__(self):
        self.h_sem = Semaphore(2)        # at most 2 H in flight
        self.o_sem = Semaphore(1)        # at most 1 O in flight
        self.barrier = Barrier(3)        # wait for 2 H + 1 O

    def hydrogen(self, releaseHydrogen):
        self.h_sem.acquire()
        self.barrier.wait()
        releaseHydrogen()
        self.h_sem.release()

    def oxygen(self, releaseOxygen):
        self.o_sem.acquire()
        self.barrier.wait()
        releaseOxygen()
        self.o_sem.release()
```

The semaphores ensure the right counts; the barrier ensures all three are present before any releases. `Barrier.wait()` blocks until exactly 3 threads have arrived, then all three proceed simultaneously.

Excellent problem to practice the `Barrier` primitive. Re-solving without `Barrier` (using two semaphores ping-ponging) is a great follow-up exercise.
### Source
LeetCode
