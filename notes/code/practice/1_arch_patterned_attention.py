"""Interview exercise: build a vectorized attention mask.

Return a boolean mask with shape ``[H, T, T]``, where
``mask[h, q, k]`` is true when query position ``q`` in head ``h`` may attend
to key position ``k``.

Use a different causal pattern for alternating heads:

* Even heads (0, 2, ...): a query at position ``q`` may attend to key
  positions ``k`` when ``0 <= q - k < window_size``.
* Odd heads (1, 3, ...): a query at position ``q`` may attend to key
  positions ``k`` when ``q >= k`` and ``(q - k) % stride == 0``.

Example with ``T=6``, ``window_size=3``, and ``stride=2``:

```
even head, q=4 -> keys [2, 3, 4]
odd head,  q=4 -> keys [0, 2, 4]
```

Constraints:

* Do not use Python loops or comprehensions.
* Build the mask using tensor operations and broadcasting.
"""

import torch
from torch import Tensor


def patterned_attention_mask(
    num_heads: int,
    sequence_length: int,
    window_size: int,
    stride: int,
) -> Tensor:
    """Return the boolean attention mask with shape ``[H, T, T]``."""
    positions = torch.arange(sequence_length)
    q = positions[:, None]  # (T, 1)
    k = positions[None, :]  # (1, T)
    sliding_window_attn = torch.logical_and(
        0 <= (q - k), (q - k) < window_size
    )  # (T, T)
    strided_attn = torch.logical_and((q - k) % stride == 0, 0 <= (q - k))  # (T, T)

    # combine
    attn = torch.zeros(num_heads, sequence_length, sequence_length) == 1
    attn[::2, ...] = sliding_window_attn.unsqueeze(0)
    attn[1::2, ...] = strided_attn.unsqueeze(0)
    return attn
