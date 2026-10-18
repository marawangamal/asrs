## Tags
ml,pytorch,transformer,autoregressive,masking,log-probs,rlhf
### Name
Anatomy of one LM training example — shift, gather, completion mask
### Problem
Given `input_ids: (B, L)` and a `completion_mask: (B, L)` (1 on completion tokens, 0 on prompt and padding), produce the per-sequence log-probability `seq_log_probs: (B,)` that the model assigns to the completion.

This is the boilerplate at the top of every LM training / RLHF objective. Write it end to end and be able to justify each shape change.
### Solution
Six lines. Every one of them is a shape transformation, and the whole thing hinges on the **one-token shift** — position `t`'s logits predict token `t+1`, so labels are just the inputs slid left by one.

```python
logits = model(input_ids).logits            # (B, L, V): score for every vocab token, at every position
logits = logits[:, :-1, :]                  # drop last position — its prediction has no next token to score
labels = input_ids[:, 1:]                   # target at each position is the actual next token (the shift)
completion_mask = completion_mask[:, 1:]    # shift the mask the same way so it lines up with labels

log_probs = logits.log_softmax(dim=-1)      # (B, L-1, V) — normalized over the vocab axis
token_log_probs = log_probs.gather(-1, labels.unsqueeze(-1)).squeeze(-1)   # (B, L-1)
seq_log_probs = (token_log_probs * completion_mask).sum(dim=-1)            # (B,)
```

Then `(-seq_log_probs).mean().backward()`. Autodiff turns the sum of per-token log-probs into the corresponding sum of per-token gradients — there is nothing special to do for sequences; the sum *is* the reduction.

Why each step:
- **`logits[:, :-1]` / `input_ids[:, 1:]`** — the autoregressive step made literal. Both slices lose one position, so the two `(B, L-1)` things align elementwise. Slice only one of them and you are off by one everywhere.
- **`log_softmax(-1)`** over the **vocab** axis, not the length axis. Fused, so numerically stable; `log(softmax(x))` is not.
- **`gather(-1, labels.unsqueeze(-1)).squeeze(-1)`** — pull the one true-token score out of the `V` axis. `gather` needs `index` to have the same ndim as the source, matching on every axis except `dim`, hence the unsqueeze/squeeze sandwich. Output shape = index shape.
- **`* completion_mask` then `.sum(-1)`** — zeroing before summing is what excludes prompt and pad tokens. Masked positions contribute exactly 0 to the value *and* 0 to the gradient.

Gotchas:
- **Shift the mask too.** Forgetting `completion_mask[:, 1:]` is the subtle bug: shapes still broadcast if you sliced nothing else, or you silently score with the mask off by one — one prompt token leaks in, one completion token drops out.
- **`.sum()` vs `.mean()` matters.** Sum = sequence log-prob (what you want for RL / likelihood objectives). For a *loss* you usually want a token mean, and it must be `masked_sum / completion_mask.sum()`, never `.mean()` — `.mean()` divides by `L-1` including pad, so loss shrinks as you pad more.
- **Sum vs length-normalized sum is a real modelling choice** — summing biases toward short completions in RL objectives; dividing by mask sum removes the length term. Pick deliberately.
- **`labels` must be `long`**; `gather` will not cast for you.
- **`ignore_index=-100`** is the `F.cross_entropy` route to the same masking — set masked labels to `-100` instead of multiplying. Don't do both; `-100` is an invalid gather index and will throw.
- **Memory**: `log_softmax` materializes a second `(B, L-1, V)` float tensor. At `V ≈ 128k` that dominates activation memory — real trainers fuse the gather into the softmax (chunked / `linear_cross_entropy`) rather than storing full log-probs.
- **Sanity check**: untrained, `token_log_probs ≈ -log(V)`, so `seq_log_probs ≈ -(#completion tokens) * log(V)`.
### Source
Interview practice — GRPO / RLHF log-prob boilerplate (`code/_practice/debug/grpo_debug.py`). The gather mechanics in isolation are in `code/ml/transformer-ce-loss-gather.md`.
