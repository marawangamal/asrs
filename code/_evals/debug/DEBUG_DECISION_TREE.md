# Debugging decision tree

Pre-test heuristic for the `_evals/debug/*` problems. Read the failure mode
first — don't change code until you know which branch you're on.

## 1. Categorize the failure

```
ValueError: could not broadcast shapes (...)   -> A (axis/keepdims)
RuntimeWarning: invalid value / NaN in output  -> B (div by zero / overflow)
AssertionError, shapes match, values wrong     -> C (value-correctness)
AssertionError, shape mismatch                 -> A
KeyError, IndexError                           -> D (collection access)
RecursionError / hangs                         -> E (base case)
Passes once, fails on rerun                    -> F (shared state)
```

## A. Broadcasting / shape

- Wrong `axis=` on a reduction. `mean(x, axis=-1)` averages features,
  not batch — flip to `axis=0` if you wanted the batch axis.
- Missing `keepdims=True` on a reduction you're about to subtract from
  the original. `(N, D) - (D,)` works; `(N, C, H, W) - (C,)` does not.
- Subtracting `(C,)` from `(N, C, H, W)` — reshape to `(C, 1, 1)` (or
  `mean[:, None, None]`) so it aligns from the right.
- `np.argsort(x)[:, -k:]` is top-k; `[:, :k]` is bottom-k.

## B. NaN / inf / divide-by-zero

- Empty bucket in `np.bincount` -> `0 / 0`. Guard with
  `np.where(counts > 0, sums / np.maximum(counts, 1), 0.0)`.
- `sqrt(var)` with `var = 0` -> 0 -> later division by 0. Use
  `sqrt(var + eps)`.
- `exp(large_logit)` overflows. Subtract
  `max(logits, axis=-1, keepdims=True)` first.
- Don't compose `log(softmax(x))`; use a stable `log_softmax`.

## C. Right shape, wrong values

- `np.where(cond, a, b)` — `cond` is first; the value-when-True is
  second. Easy to swap.
- Fancy indexing axes: `log_probs[np.arange(n), labels]`, not
  `log_probs[labels, np.arange(n)]`.
- `np.bincount(idx)` without `minlength=` returns a length determined
  by the max value, which is shorter than `num_classes` when the top
  classes don't appear.
- `np.nonzero(x)` returns a tuple of arrays (one per dim). For 1D,
  unwrap with `np.nonzero(x)[0]`.
- `argmin` / `argmax` reduce along the axis you pass; pair `(N, K)`
  distances with `axis=1`, not `axis=0`.
- R^2: `SS_tot = sum((y_true - mean(y_true))^2)` — mean of truth, not
  of prediction.
- `running = (1 - m) * running + m * batch` — small momentum means slow
  adaptation. Swapping the two terms inverts that.

## D. KeyError / IndexError

- Dict lookup on user input: use `.get(key, default)`.
- Map built from a list `kept` with `enumerate(kept)` gives ids
  starting at 0; if UNK is supposed to be at 0 *and* prepended to the
  id-to-token list, every other id shifts by 1.
- Confusing `id_to_token[i]` vs `token_to_id[t]` — verify which
  direction you're querying.

## E. Recursion bugs

- Missing base case for empty input (`None`, `[]`, `i == len(s)`).
- Off-by-one in index advance: parsing digits, skipping `]`, etc.
- `min` vs `max` in tree-depth recursions.
- Backtracking state: append -> recurse -> **pop**;
  add -> recurse -> **remove**. Missing the undo is the bug.

## F. State that persists across calls

- `def f(x, acc=[])` — `acc` is the *same list* on every call. Use
  `acc=None` and `if acc is None: acc = []`.
- `def f(x, visited=set())` — same trap with a set.
- DFS where `visited` is reset *inside* the outer loop, so each
  starting node counts as a new component.
- DFS where `visited` and "on the current path" are the same set, so a
  diamond DAG is reported as a cycle. Use two separate sets.

## G. RNG

- `np.random.RandomState(seed)` — seed each test that needs
  determinism.
- `.choice(n, size=k, replace=False)` raises `ValueError` if `k > n` —
  usually the right behavior, not a bug.

## Where to look first per problem

| Folder                                                    | Likely category |
| --------------------------------------------------------- | --------------- |
| `numpy_axis`, `batch_norm`                                | A               |
| `softmax_metrics`                                         | A, B, C         |
| `histogram_metrics`, `regression_metrics`                 | B, C            |
| `kmeans`                                                  | A, B, G         |
| `running_stats`                                           | B + init values |
| `tree_fns`, `recursion_easy`/`_medium`/`_hard`            | E, F            |
| `graph_recursion`                                         | E, F            |
| `vocab`                                                   | C, D            |
