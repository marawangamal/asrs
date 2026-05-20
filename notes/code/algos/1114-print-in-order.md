## Number
1114
## Tags
leetcode,design,concurrency
### Name
Print in Order
### Problem
Three threads call `first()`, `second()`, `third()` in arbitrary order. Force the output to be `firstsecondthird`.
### Solution
The "hello world" of synchronization. Solve with two `Event`s (or two `Lock`s held initially, or two `Semaphore(0)`s).

```python
from threading import Event

class Foo:
    def __init__(self):
        self.done_first = Event()
        self.done_second = Event()

    def first(self, printFirst):
        printFirst()
        self.done_first.set()

    def second(self, printSecond):
        self.done_first.wait()
        printSecond()
        self.done_second.set()

    def third(self, printThird):
        self.done_second.wait()
        printThird()
```

Worth solving three different ways (Event, Lock, Semaphore) — builds intuition for what each primitive is. The shape: each thread waits for a signal, prints, then signals the next thread.
### Source
LeetCode
