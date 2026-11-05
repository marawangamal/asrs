"""Interview exercise: implement rotary position embeddings (RoPE).

Implement ``apply_rope`` for a tensor ``x`` with shape ``[B, H, T, D]``.
``cos`` and ``sin`` have shape ``[T, D // 2]`` and contain the rotation
values for each adjacent feature pair: ``(0, 1), (2, 3), ...``.

Return a tensor with the same shape, dtype, and device as ``x``. Assume ``D``
is even. Do not use Python loops over batches, heads, tokens, or dimensions.
"""

import torch


def apply_rope(x: torch.Tensor, cos: torch.Tensor, sin: torch.Tensor) -> torch.Tensor:
    """Apply rotary position embeddings and return shape ``[B, H, T, D]``."""
    B, H, T, D = x.shape
    c = cos.reshape(1, 1, T, -1)
    s = sin.reshape(1, 1, T, -1)
    x_even = c * x[..., 0::2] - s * x[..., 1::2]  # (B, D, T, D//2)
    x_odd = s * x[..., 0::2] + c * x[..., 1::2]  # (B, D, T, D//2)
    return torch.stack((x_even, x_odd), dim=-1).reshape(B, H, T, D)
