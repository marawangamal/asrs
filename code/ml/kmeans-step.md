## Tags
ml,numpy,kmeans,broadcasting
### Name
KMeans step / group-by aggregation via mask
### Problem
Given `points: (N, D)` and per-point cluster `assignments: (N,)` with values in `[0, K)`, compute new centroids — the mean of points in each cluster. Empty clusters should map to zero.

More generally: aggregate a `(N, D)` array into `(K, D)` by group, where the group ids are a 1-D int array.
### Solution
`np.bincount` is the natural tool, but its `weights=` arg is **1-D only**, so it can only sum scalars per group. For vector-valued aggregations you do **counts with `bincount`**, **sums with a per-group mask loop**:

```python
def update_centroids(points, assignments, K):
    # points (N, D), assignments (N,) in [0, K)
    N, D = points.shape
    counts = np.bincount(assignments, minlength=K)         # (K,)
    sums = np.zeros((K, D))
    for k in range(K):
        mask = assignments == k                            # (N,) bool
        sums[k] = points[mask].sum(axis=0)                 # (D,)
    # avoid 0/0 for empty clusters — 0 / 1 = 0
    safe = np.clip(counts, a_min=1, a_max=None)            # or np.maximum(counts, 1)
    return sums / safe[:, None]                            # (K, D)
```

Key ideas:
- **`minlength=K`** forces the output to size `K` even if some clusters never appear in `assignments`. Without it, trailing empty clusters disappear.
- **Empty cluster trick**: `np.clip(counts, a_min=1, a_max=None)` (or `np.maximum(counts, 1)`) turns `0 → 1` for division. Safe because the matching `sums` row is already all-zero, so `0/1 = 0`. Avoids a NaN-mask branch.
- **Why a Python loop is fine here**: `K` is typically small (≤ thousands) and the inner op (`points[mask].sum`) is vectorized.

Alternative one-liners when `D` is large or you can't afford the K-loop:

```python
# unbuffered scatter-add — handles N-D natively
np.add.at(sums, assignments, points)

# one-hot @ points — fully vectorized, O(N*K) memory
sums = np.eye(K)[assignments].T @ points
```

For the **assign** step (nearest centroid), pair this with broadcasting:

```python
def assign(points, centroids):
    # (N, D), (K, D) -> (N,)
    diff = points[:, None, :] - centroids[None, :, :]      # (N, K, D)
    return np.argmin((diff ** 2).sum(axis=-1), axis=1)     # (N,)
```

Gotchas:
- `np.zeros(K, D)` is wrong — `np.zeros` takes a **shape tuple**: `np.zeros((K, D))`. The second positional arg is `dtype`.
- `points[assignments]` is fancy indexing (reorders rows), not filtering — you want `points[assignments == k]`.
- `np.bincount(assignments, weights=points, ...)` raises `"object too deep for desired array"` — weights must be 1-D.
- `np.clip` needs both `a_min` and `a_max`; pass `a_max=None` to leave the upper end alone.
### Source
Interview practice (Problem 3 in `python/interview_practice.ipynb`). cuPyNumeric k-means example uses the same mask+`np.maximum(counts, 1)` pattern.
