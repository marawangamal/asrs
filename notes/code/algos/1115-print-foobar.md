## Number
1115
## Tags
leetcode,design,concurrency
### Name
Print FooBar Alternately
### Problem
Two threads run `foo()` and `bar()`, each in a `for` loop of length `n`. Force the output to be `foobarfoobar...`.
### Solution
Classic two-semaphore ping-pong. Each semaphore is a single "token" passed back and forth. Foo's semaphore starts available, bar's starts blocked.

```python
from threading import Semaphore

class FooBar:
    def __init__(self, n):
        self.n = n
        self.foo_sem = Semaphore(1)   # starts available — foo goes first
        self.bar_sem = Semaphore(0)   # starts blocked — bar waits

    def foo(self, printFoo):
        for _ in range(self.n):
            self.foo_sem.acquire()
            printFoo()
            self.bar_sem.release()    # hand off to bar

    def bar(self, printBar):
        for _ in range(self.n):
            self.bar_sem.acquire()
            printBar()
            self.foo_sem.release()    # hand off to foo
```

The mental model: whoever holds the token prints, then hands the *other* token to the *other* thread. This shape is everywhere — any alternating producers/consumers problem decomposes to this.
### Source
LeetCode
