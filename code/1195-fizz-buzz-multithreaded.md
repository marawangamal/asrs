## Number
1195
## Tags
leetcode,design,concurrency
### Name
Fizz Buzz Multithreaded
### Problem
Four threads coordinate to print FizzBuzz up to `n`: one prints "fizz" (multiples of 3 only), one "buzz" (multiples of 5 only), one "fizzbuzz" (multiples of 15), one numbers (otherwise).
### Solution
Four semaphores. A dispatcher could work, but cleaner is to let the "number" thread own the loop and signal the others — or use four semaphores with the parent loop dispatching.

Concise version using a `Condition` with a predicate:

```python
from threading import Condition

class FizzBuzz:
    def __init__(self, n):
        self.n = n
        self.curr = 1
        self.cond = Condition()

    def _matches(self, want):
        # want: "f", "b", "fb", or "n"
        if self.curr > self.n:
            return True   # let waiter wake up and exit
        m3, m5 = self.curr % 3 == 0, self.curr % 5 == 0
        return ((want == "fb" and m3 and m5)
             or (want == "f" and m3 and not m5)
             or (want == "b" and m5 and not m3)
             or (want == "n" and not m3 and not m5))

    def _run(self, want, action):
        while True:
            with self.cond:
                self.cond.wait_for(lambda: self._matches(want))
                if self.curr > self.n:
                    return
                if want == "n":
                    action(self.curr)
                else:
                    action()
                self.curr += 1
                self.cond.notify_all()

    def fizz(self, printFizz):       self._run("f",  printFizz)
    def buzz(self, printBuzz):       self._run("b",  printBuzz)
    def fizzbuzz(self, printFizzBuzz): self._run("fb", printFizzBuzz)
    def number(self, printNumber):   self._run("n",  printNumber)
```

The `Condition` + `wait_for(predicate)` pattern is the right tool when threads need to wake up only when state matches a predicate — it handles spurious wakeups automatically.
### Source
LeetCode
