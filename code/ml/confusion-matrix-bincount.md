## Tags
ml,numpy,bincount,confusion-matrix
### Name
Confusion matrix via `bincount` + flat-index trick
### Problem
Given `y_true, y_pred: (N,)` int arrays with values in `[0, C)`, build the `(C, C)` confusion matrix `M` where `M[i, j]` = number of samples with true class `i` and predicted class `j`. No Python loops.
### Solution
Encode each `(true, pred)` pair as a unique flat index in `[0, C*C)`, tally with `bincount`, reshape back to `(C, C)`:

```python
def confusion_matrix(y_true, y_pred, num_classes):
    idx = y_true * num_classes + y_pred                       # (N,) in [0, C*C)
    counts = np.bincount(idx, minlength=num_classes ** 2)     # (C*C,)
    return counts.reshape(num_classes, num_classes)           # (C, C)
```

Why it works: row-major flattening of `(C, C)` puts cell `(i, j)` at flat index `i*C + j`. So `idx` is literally "which cell does this sample belong to," and `bincount` is a histogram over cells.

Example, C=3, `y_true=[0,1,2,1]`, `y_pred=[0,1,1,1]`:
- `idx = [0, 4, 7, 4]`
- `bincount(..., minlength=9) = [1,0,0,0,2,0,0,1,0]`
- reshape → `[[1,0,0],[0,2,0],[0,1,0]]`

Gotchas:
- **`minlength=C**2`, not `C`** — otherwise if the last cell `(C-1, C-1)` is empty, `counts` is shorter than `C*C` and `reshape(C, C)` raises.
- **Row = true, col = pred** is the convention here. `M.sum(axis=1)` = per-true totals (recall denominators); `M.sum(axis=0)` = per-pred totals (precision denominators). Swap `y_true`/`y_pred` in `idx` if you want the transpose.
- Generalizes to N-way joint histograms: for `K` int arrays each in `[0, C)`, use `idx = a0*C**(K-1) + a1*C**(K-2) + ... + a_{K-1}` and `bincount(idx, minlength=C**K).reshape((C,)*K)`.
### Source
Interview practice (`code/_evals/debug/histogram_metrics/`). Same trick generalizes any joint histogram over small-cardinality int arrays.
