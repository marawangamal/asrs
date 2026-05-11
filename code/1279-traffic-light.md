## Number
1279
## Tags
leetcode,design,concurrency
### Name
Traffic Light Controlled Intersection
### Problem
Two roads cross at an intersection (a shared resource). Cars from each direction call `carArrived(...)`. Only one direction's green light can be active at a time; switch when a car arrives from the other direction.
### Solution
A mutex + a tiny state machine. The lock protects both the "current green direction" state and the act of passing a car through.

```python
from threading import Lock

class TrafficLight:
    def __init__(self):
        self.lock = Lock()
        self.green_road = 1   # which road currently has the green

    def carArrived(self, carId, roadId, direction, turnGreen, crossCar):
        with self.lock:
            if self.green_road != roadId:
                turnGreen()
                self.green_road = roadId
            crossCar()
```

Both the state check and the mutation must happen inside the same lock to avoid races (two cars from different roads concurrently observing "not green" and both calling `turnGreen`). Once you see "single shared resource + state machine," the answer is almost always one lock guarding everything.
### Source
LeetCode
