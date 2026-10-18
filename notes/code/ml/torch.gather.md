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

### Source
Interview practice — transformer training-loop pattern. Same paired-index rule as `code/ml/fancy-indexing-shapes.md` (Q2), applied one axis deeper.
