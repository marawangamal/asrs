## Number
1116
## Tags
leetcode,design,concurrency
### Name
Print Zero Even Odd
### Problem
Three threads coordinate to print `0102030405...` up to `n`. One thread prints 0 before every number, two others alternate even/odd.
### Solution
Three semaphores, ping-ponging in a 0 -> odd/even -> 0 cycle. Zero's semaphore starts available; odd and even start blocked.

```python
from threading import Semaphore

class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.zero_sem = Semaphore(1)
        self.odd_sem = Semaphore(0)
        self.even_sem = Semaphore(0)

    def zero(self, printNumber):
        for i in range(1, self.n + 1):
            self.zero_sem.acquire()
            printNumber(0)
            if i % 2 == 1:
                self.odd_sem.release()
            else:
                self.even_sem.release()

    def odd(self, printNumber):
        for i in range(1, self.n + 1, 2):
            self.odd_sem.acquire()
            printNumber(i)
            self.zero_sem.release()

    def even(self, printNumber):
        for i in range(2, self.n + 1, 2):
            self.even_sem.acquire()
            printNumber(i)
            self.zero_sem.release()
```

Solidifies the alternation pattern from FooBar but with three participants. The key is that zero acts as the dispatcher — after printing 0, it decides which of even/odd to wake based on the parity of the next number.
### Source
LeetCode
