## Tags
ml,numpy,indexing,broadcasting,shapes
### Name
Fancy indexing — shape quizzes for (N, C) arrays
### Problem
Given `x = np.arange(20).reshape(4, 5)`, `labels = np.array([2, 0, 4, 1])`, and `rows = np.arange(4)`, predict the shape (and contents where relevant) of each expression below before peeking. Three modes: slice + array, paired arrays, broadcast arrays.

```python
x = np.arange(20).reshape(4, 5)
# [[ 0  1  2  3  4]
#  [ 5  6  7  8  9]
#  [10 11 12 13 14]
#  [15 16 17 18 19]]
labels = np.array([2, 0, 4, 1])
rows   = np.arange(4)
```
### Solution
**Mental model:** slices keep an axis, integer arrays consume it. When multiple integer arrays appear, they are **paired elementwise** and must broadcast — the result has the broadcast shape.

**Q1.** `x[:, labels]` — shape?

```
shape (4, 4)
```
`:` keeps axis 0 (size 4); the length-4 int array replaces axis 1. Picks columns `[2, 0, 4, 1]` for every row.

**Q2.** `x[rows, labels]` — shape and contents?

```
shape (4,)
elements: [x[0,2], x[1,0], x[2,4], x[3,1]]
        = [2, 5, 14, 16]
```
Two integer arrays of the same shape → zipped, **not** cross-product. This is the "gather one per row" pattern used in cross-entropy: `log_probs[np.arange(n), labels]`. Swapping to `x[labels, rows]` indexes different elements (and can `IndexError` if any label ≥ N) — the order of the indices follows axis order, always.

**Q3.** `x[rows[:, None], labels[None, :]]` — shape, and how does it differ from Q2?

```
shape (4, 4)
element [i, j] = x[rows[i], labels[j]]   # full cross-product
```
Index arrays of shapes `(4, 1)` and `(1, 4)` broadcast to `(4, 4)`, producing a **grid** instead of paired pairs. `np.ix_(rows, labels)` is sugar for the same thing.

Gotchas:
- **Paired vs grid is purely about broadcasting shape**, not about which arrays you pass. Same-shape index arrays → paired; broadcasted shapes → grid.
- **`np.argsort` is ascending** — the "top-k" lives at the end: `np.argsort(x, axis=1)[:, -k:]`, not `[:, :k]`.
- For higher-rank tensors where computing the companion `arange` is annoying, prefer `np.take_along_axis(x, idx, axis=...)` (PyTorch: `x.gather(dim, idx)`).
- Mixing a slice with one integer array (Q1) keeps the slice axis; mixing a slice with two integer arrays applies the *paired/broadcast* rule to the array axes and the slice stays put.
### Source
Interview practice — debugging `code/_evals/debug/softmax_metrics/softmax_metrics.py`, where `log_probs[labels, np.arange(n)]` (swapped axes) was the cross-entropy bug.
