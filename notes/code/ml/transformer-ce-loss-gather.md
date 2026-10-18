## Tags
ml,pytorch,transformer,cross-entropy,gather,indexing,shapes
### Name
Transformer loss — gathering target logprobs from a (B, T, V) tensor
### Problem
A transformer forward pass gives these

log_probs.shape       # [B, T-1, V]
target_ids.shape      # [B, T-1]

At every batch and time position, we want one value from the vocabulary dimension.


### Solution
```sh
# First, add a vocabulary-axis dimension to the target IDs:
indices = target_ids.unsqueeze(-1)
indices.shape  # [B, T-1, 1]

# Second, gather along the vocabulary axis:
selected = torch.gather(
    input=log_probs,
    dim=-1,
    index=indices,
)

selected.shape  # [B, T-1, 1]
```

Another way to think about it is as follows, if we have a tensor of size D1xD2xD3, we can do reductions in the 2nd dim
`tens.mean(dim=1)`, or tensor.gather(dim=1, indices=ids). 

...

A transformer forward pass returns `logits: (B, L, V)`. The targets are `y: (B, L)` of token ids in `[0, V)`. Compute the mean cross-entropy loss.

The whole exercise is the **gather**: you need one scalar per `(b, l)` position — the logprob of the true token — pulled out of a `V`-sized axis. Write it without a Python loop.
### Solution
Two routes. Either flatten `(B, L)` into one batch axis and let the library do it, or keep the shape and gather along the vocab axis. Know both — the second is what interviewers are actually asking for, and it's the only one that gives you per-token loss.

```python
import torch
import torch.nn.functional as F

B, L, V = 2, 5, 100
logits = model(x)                    # (B, L, V)
y      = targets                     # (B, L), dtype long

# --- Route 1: flatten, let F.cross_entropy do the gather ---
loss = F.cross_entropy(
    logits.reshape(-1, V),           # (B*L, V)
    y.reshape(-1),                   # (B*L,)
)                                    # scalar, mean over B*L

# --- Route 2: manual gather, keeps (B, L) shape ---
logp = logits.log_softmax(dim=-1)                    # (B, L, V)
tok  = logp.gather(-1, y.unsqueeze(-1)).squeeze(-1)  # (B, L)
loss = -tok.mean()
```

`gather` is the crux: `src.gather(dim, index)` requires `index` to have the **same ndim as `src`**, matching in every axis except `dim`. Hence `y.unsqueeze(-1)` → `(B, L, 1)`, gather along `dim=-1` → output `(B, L, 1)`, then `squeeze(-1)` → `(B, L)`. Output shape always equals `index` shape, not `src` shape.

Equivalents worth recognizing:

```python
# NumPy has no gather — it's take_along_axis
tok = np.take_along_axis(logp, y[..., None], axis=-1)[..., 0]   # (B, L)

# Pure fancy indexing (paired int arrays, one per axis)
bi = torch.arange(B)[:, None]        # (B, 1)
li = torch.arange(L)[None, :]        # (1, L)
tok = logp[bi, li, y]                # (B, L) — broadcasts to (B, L)

# Flattened version of the same idea
tok = logp.reshape(-1, V)[torch.arange(B * L), y.reshape(-1)]    # (B*L,)
```

Gotchas:
- **`index` must be `long`** (`int64`). An `int32` or float index is a hard `RuntimeError`, not a silent cast.
- **Forgetting `unsqueeze`** → `Index tensor must have the same number of dimensions as input tensor`. Forgetting `squeeze` leaves a stray trailing 1 that broadcasts wrong later (a `(B, L, 1)` loss silently averaged against a `(B, L)` mask gives `(B, L, B, L)`... or a wrong scalar).
- **`log_softmax(-1)`, not `log(softmax(-1))`** — the fused version is numerically stable. And `F.cross_entropy` takes **raw logits**; passing it logprobs applies softmax twice.
- **`reshape`, not `view`**, if you ever `permute` first — post-permute tensors aren't contiguous and `view` throws.
- **`F.cross_entropy` on a 3-D input wants `(B, V, L)`**, not `(B, L, V)` — channel axis second. Flattening to `(B*L, V)` sidesteps the `permute` entirely and is the safer habit.
- **Causal LM shift**: if `y` *is* the input sequence, you must shift — `logits[:, :-1]` against `y[:, 1:]`. Predicting position `l` from position `l` is the classic off-by-one that shows up as a suspiciously tiny loss.
- **Padding**: `F.cross_entropy(..., ignore_index=pad_id)` excludes those positions from *both* numerator and denominator. On the manual route you must do it yourself — `(tok * mask).sum() / mask.sum()`, **not** `.mean()`, or you divide by the padded count.
- **Sanity check**: an untrained model should give `loss ≈ log(V)` (≈ 10.8 for `V = 50k`). Way below that at step 0 means label leakage or a bad shift.
### Source
Interview practice — transformer training-loop pattern. Same paired-index rule as `code/ml/fancy-indexing-shapes.md` (Q2), applied one axis deeper.
